#!/usr/bin/env python3
"""Validate BrickMorph model JSON and write an honest qualitySelfCheck."""

from __future__ import annotations

import argparse
import json
import math
import sys
from collections import defaultdict
from pathlib import Path
from typing import Any


ALLOWED_TYPES = {"box", "ellipsoid", "cylinder", "cone", "capsule", "torus", "frustum"}
ALLOWED_AXES = {"x", "y", "z"}
ALLOWED_CLASSES = {"humanoid_robot", "vehicle", "creature", "building", "object"}
HAND_CORE_TOKENS = {"hand", "fist", "palm", "grip", "gripper"}
HAND_DIGIT_TOKENS = {"thumb", "finger", "fingers", "knuckle", "knuckles", "claw", "jaw"}
HAND_TOKENS = HAND_CORE_TOKENS | HAND_DIGIT_TOKENS
ROUND_WHOLE_HAND_TYPES = {"ellipsoid", "capsule"}


class ModelError(ValueError):
    pass


def number(value: Any, label: str, *, minimum: float | None = None, maximum: float | None = None) -> float:
    if isinstance(value, bool) or not isinstance(value, (int, float)) or not math.isfinite(value):
        raise ModelError(f"{label} must be a finite number")
    result = float(value)
    if minimum is not None and result < minimum:
        raise ModelError(f"{label} must be >= {minimum:g}")
    if maximum is not None and result > maximum:
        raise ModelError(f"{label} must be <= {maximum:g}")
    return result


def vector(value: Any, length: int, label: str, *, minimum: float | None = None) -> list[float]:
    if not isinstance(value, list) or len(value) != length:
        raise ModelError(f"{label} must contain exactly {length} numbers")
    return [number(item, f"{label}[{index}]", minimum=minimum, maximum=240) for index, item in enumerate(value)]


def primitive_volume(primitive: dict[str, Any]) -> float:
    kind = primitive["type"]
    if kind == "box":
        return math.prod(primitive["size"])
    if kind == "ellipsoid":
        return math.pi / 6 * math.prod(primitive["size"])
    if kind == "cylinder":
        return math.pi * primitive["radius"] ** 2 * primitive["height"]
    if kind == "cone":
        top = primitive["radiusTop"]
        bottom = primitive["radiusBottom"]
        return math.pi * primitive["height"] / 3 * (top * top + top * bottom + bottom * bottom)
    if kind == "capsule":
        length = math.dist(primitive["start"], primitive["end"])
        radius = primitive["radius"]
        return math.pi * radius * radius * length + 4 / 3 * math.pi * radius**3
    if kind == "torus":
        return 2 * math.pi**2 * primitive["majorRadius"] * primitive["minorRadius"] ** 2
    bottom_area = math.prod(primitive["bottomSize"])
    top_area = math.prod(primitive["topSize"])
    return primitive["height"] / 3 * (bottom_area + top_area + math.sqrt(bottom_area * top_area))


def part_tokens(part: str) -> set[str]:
    normalized = part.casefold().replace("-", "_").replace(" ", "_")
    return {token for token in normalized.split("_") if token}


def assess_hand_articulation(primitives: list[dict[str, Any]]) -> tuple[dict[str, Any], list[str]]:
    hand_primitives: list[tuple[dict[str, Any], set[str]]] = []
    wrist_primitives: list[tuple[dict[str, Any], set[str]]] = []
    for primitive in primitives:
        if primitive["op"] != "add":
            continue
        tokens = part_tokens(primitive.get("part", ""))
        if tokens & HAND_TOKENS:
            hand_primitives.append((primitive, tokens))
        elif "wrist" in tokens:
            wrist_primitives.append((primitive, tokens))

    side_parts: dict[str, list[tuple[dict[str, Any], set[str]]]] = {"left": [], "right": []}
    unscoped = []
    for primitive, tokens in hand_primitives:
        sides = [side for side in side_parts if side in tokens]
        if len(sides) == 1:
            side_parts[sides[0]].append((primitive, tokens))
        else:
            unscoped.append(primitive.get("part", ""))
    for primitive, tokens in wrist_primitives:
        for side in side_parts:
            if side in tokens and side_parts[side]:
                side_parts[side].append((primitive, tokens))

    articulated_sides = []
    unarticulated_sides = []
    for side, entries in side_parts.items():
        if not entries:
            continue
        unique_parts = {primitive.get("part", "").casefold() for primitive, _ in entries}
        has_core = any(tokens & HAND_CORE_TOKENS for _, tokens in entries)
        has_digit = any(tokens & HAND_DIGIT_TOKENS for _, tokens in entries)
        if len(unique_parts) >= 3 and has_core and has_digit:
            articulated_sides.append(side)
        else:
            unarticulated_sides.append(side)

    round_whole_hands = [
        primitive.get("part", "")
        for primitive, tokens in hand_primitives
        if primitive["type"] in ROUND_WHOLE_HAND_TYPES and tokens & {"hand", "fist"}
    ]
    metrics = {
        "handPartCount": len(hand_primitives) + sum(
            1 for _, tokens in wrist_primitives if any(side in tokens and side_parts[side] for side in side_parts)
        ),
        "articulatedHandSideCount": len(articulated_sides),
        "unarticulatedHandSideCount": len(unarticulated_sides),
        "roundWholeHandCount": len(round_whole_hands),
    }
    issues = []
    if unscoped:
        issues.append("hand-related part names must include left or right side prefixes")
    if unarticulated_sides:
        joined = ", ".join(unarticulated_sides)
        issues.append(f"hand articulation is incomplete for: {joined}; add palm/fist core, thumb, digit/knuckle blocks, and wrist")
    if round_whole_hands:
        joined = ", ".join(round_whole_hands)
        issues.append(f"featureless round hand/fist primitives are not allowed: {joined}")
    return metrics, issues


def validate_primitive(source: Any, index: int, palette_count: int) -> dict[str, Any]:
    label = f"primitives[{index}]"
    if not isinstance(source, dict):
        raise ModelError(f"{label} must be an object")
    kind = source.get("type")
    if kind not in ALLOWED_TYPES:
        raise ModelError(f"{label}.type must be one of {sorted(ALLOWED_TYPES)}")
    if source.get("op") not in {"add", "subtract"}:
        raise ModelError(f"{label}.op must be add or subtract")
    material = source.get("material")
    if isinstance(material, bool) or not isinstance(material, int) or not 0 <= material < palette_count:
        raise ModelError(f"{label}.material must be a valid integer palette index")
    part = source.get("part", "")
    if not isinstance(part, str):
        raise ModelError(f"{label}.part must be a string")

    if kind == "capsule":
        vector(source.get("start"), 3, f"{label}.start")
        vector(source.get("end"), 3, f"{label}.end")
        number(source.get("radius"), f"{label}.radius", minimum=1e-9, maximum=120)
    else:
        vector(source.get("center"), 3, f"{label}.center")
        vector(source.get("rotation", [0, 0, 0]), 3, f"{label}.rotation")
        if kind in {"box", "ellipsoid"}:
            vector(source.get("size"), 3, f"{label}.size", minimum=1e-9)
        elif kind == "cylinder":
            number(source.get("radius"), f"{label}.radius", minimum=1e-9, maximum=120)
            number(source.get("height"), f"{label}.height", minimum=1e-9, maximum=240)
        elif kind == "cone":
            number(source.get("radiusTop"), f"{label}.radiusTop", minimum=0, maximum=120)
            number(source.get("radiusBottom"), f"{label}.radiusBottom", minimum=1e-9, maximum=120)
            number(source.get("height"), f"{label}.height", minimum=1e-9, maximum=240)
        elif kind == "torus":
            major = number(source.get("majorRadius"), f"{label}.majorRadius", minimum=1e-9, maximum=120)
            minor = number(source.get("minorRadius"), f"{label}.minorRadius", minimum=1e-9, maximum=60)
            if minor >= major:
                raise ModelError(f"{label}.minorRadius must be smaller than majorRadius")
        elif kind == "frustum":
            vector(source.get("bottomSize"), 2, f"{label}.bottomSize", minimum=1e-9)
            vector(source.get("topSize"), 2, f"{label}.topSize", minimum=0)
            number(source.get("height"), f"{label}.height", minimum=1e-9, maximum=240)
        if kind in {"cylinder", "cone", "torus"} and source.get("axis") not in ALLOWED_AXES:
            raise ModelError(f"{label}.axis must be x, y, or z")
    return source


def validate_schema(model: Any) -> list[dict[str, Any]]:
    if not isinstance(model, dict):
        raise ModelError("root value must be an object")
    if model.get("version") != "1.0":
        raise ModelError('version must be "1.0"')
    palette = model.get("palette")
    if not isinstance(palette, list) or not 1 <= len(palette) <= 12:
        raise ModelError("palette must contain 1 to 12 colors")
    for index, color in enumerate(palette):
        if not isinstance(color, str) or len(color) != 7 or color[0] != "#":
            raise ModelError(f"palette[{index}] must use #RRGGBB")
        try:
            int(color[1:], 16)
        except ValueError as error:
            raise ModelError(f"palette[{index}] must use #RRGGBB") from error
    subject_class = model.get("subjectClass")
    if subject_class not in ALLOWED_CLASSES:
        raise ModelError(f"subjectClass must be one of {sorted(ALLOWED_CLASSES)}")
    primitives = model.get("primitives")
    if not isinstance(primitives, list) or not 1 <= len(primitives) <= 80:
        raise ModelError("primitives must contain 1 to 80 entries")
    validated = [validate_primitive(item, index, len(palette)) for index, item in enumerate(primitives)]
    if not any(item["op"] == "add" for item in validated):
        raise ModelError("at least one primitive must use op=add")
    landmarks = model.get("landmarks")
    if not isinstance(landmarks, list) or any(not isinstance(item, str) or not item.strip() for item in landmarks):
        raise ModelError("landmarks must be an array of non-empty strings")
    if model.get("requestedBrickCount") != 16000:
        raise ModelError("requestedBrickCount must be 16000 for BrickMorph top-detail compatibility")
    return validated


def validate_explicit_schema(model: Any) -> list[list[float | int]]:
    if not isinstance(model, dict):
        raise ModelError("root value must be an object")
    if model.get("version") != "1.0":
        raise ModelError('version must be "1.0"')
    if model.get("format") != "explicit-bricks-v1":
        raise ModelError('format must be "explicit-bricks-v1"')
    palette = model.get("palette")
    if not isinstance(palette, list) or not 1 <= len(palette) <= 12:
        raise ModelError("palette must contain 1 to 12 colors")
    for index, color in enumerate(palette):
        if not isinstance(color, str) or len(color) != 7 or color[0] != "#":
            raise ModelError(f"palette[{index}] must use #RRGGBB")
        try:
            int(color[1:], 16)
        except ValueError as error:
            raise ModelError(f"palette[{index}] must use #RRGGBB") from error
    if model.get("subjectClass") not in ALLOWED_CLASSES:
        raise ModelError(f"subjectClass must be one of {sorted(ALLOWED_CLASSES)}")
    source = model.get("bricks")
    if not isinstance(source, list) or not 1 <= len(source) <= 150_000:
        raise ModelError("bricks must contain 1 to 150000 entries")
    validated: list[list[float | int]] = []
    occupied: set[tuple[float, float, float]] = set()
    for index, item in enumerate(source):
        if not isinstance(item, list) or len(item) != 4:
            raise ModelError(f"bricks[{index}] must be [x, y, z, material]")
        position = [number(item[axis], f"bricks[{index}][{axis}]") for axis in range(3)]
        if any(abs(value) > 240 for value in position):
            raise ModelError(f"bricks[{index}] coordinate magnitude must be <= 240")
        material = item[3]
        if isinstance(material, bool) or not isinstance(material, int) or not 0 <= material < len(palette):
            raise ModelError(f"bricks[{index}][3] must be a valid material index")
        key = tuple(position)
        if key in occupied:
            raise ModelError(f"duplicate brick coordinate at bricks[{index}]")
        occupied.add(key)
        validated.append([*position, material])
    landmarks = model.get("landmarks")
    if not isinstance(landmarks, list) or any(not isinstance(item, str) or not item.strip() for item in landmarks):
        raise ModelError("landmarks must be an array of non-empty strings")
    if model.get("requestedBrickCount") != len(validated):
        raise ModelError("requestedBrickCount must equal the explicit bricks length")
    return validated


def assess(model: dict[str, Any], primitives: list[dict[str, Any]]) -> tuple[dict[str, Any], list[str]]:
    added = [item for item in primitives if item["op"] == "add"]
    primitive_count = len(primitives)
    box_ratio = sum(item["type"] == "box" for item in primitives) / primitive_count
    rotated_count = sum(
        item["type"] != "capsule" and any(abs(value) >= 1 for value in item.get("rotation", []))
        for item in primitives
    )
    subtract_count = primitive_count - len(added)
    material_count = len({item["material"] for item in added})
    volumes = sorted((primitive_volume(item) for item in added), reverse=True)
    total_volume = sum(volumes) or 1
    top_three_ratio = sum(volumes[:3]) / total_volume
    material_volumes: dict[int, float] = defaultdict(float)
    for item in added:
        material_volumes[item["material"]] += primitive_volume(item)
    dominant_ratio = max(material_volumes.values(), default=0) / total_volume
    named_parts = [item.get("part", "").strip() for item in primitives if item.get("part", "").strip()]
    unique_parts = len({item.casefold() for item in named_parts})
    named_ratio = len(named_parts) / primitive_count
    landmarks = model.get("landmarks", [])
    geometry_count = len({item["type"] for item in primitives})
    hand_metrics, hand_issues = assess_hand_articulation(primitives)

    metrics = {
        "primitiveCount": primitive_count,
        "geometryTypeCount": geometry_count,
        "boxRatio": round(box_ratio, 6),
        "rotatedCount": rotated_count,
        "subtractCount": subtract_count,
        "materialCount": material_count,
        "topThreeVolumeRatio": round(top_three_ratio, 6),
        "dominantMaterialRatio": round(dominant_ratio, 6),
        "landmarkCount": len(landmarks),
        "namedPartRatio": round(named_ratio, 6),
        "uniquePartCount": unique_parts,
        **hand_metrics,
    }

    required_rotated = max(10, math.ceil(primitive_count * 0.22))
    issues = []
    if primitive_count < 48:
        issues.append(f"primitiveCount {primitive_count} is below 48")
    if geometry_count < 5:
        issues.append(f"geometryTypeCount {geometry_count} is below 5")
    if box_ratio > 0.62:
        issues.append(f"boxRatio {box_ratio:.1%} exceeds 62%")
    if rotated_count < required_rotated:
        issues.append(f"rotatedCount {rotated_count} is below {required_rotated}")
    if subtract_count < 2:
        issues.append(f"subtractCount {subtract_count} is below 2")
    if material_count < 4:
        issues.append(f"materialCount {material_count} is below 4")
    if top_three_ratio > 0.58:
        issues.append(f"topThreeVolumeRatio {top_three_ratio:.1%} exceeds 58%")
    if dominant_ratio > 0.72:
        issues.append(f"dominantMaterialRatio {dominant_ratio:.1%} exceeds 72%")
    if len(landmarks) < 6:
        issues.append(f"landmarkCount {len(landmarks)} is below 6")
    if named_ratio < 0.90:
        issues.append(f"namedPartRatio {named_ratio:.1%} is below 90%")
    if unique_parts < 10:
        issues.append(f"uniquePartCount {unique_parts} is below 10")
    if model.get("subjectClass") == "humanoid_robot":
        landmark_tokens = set().union(*(part_tokens(item) for item in landmarks)) if landmarks else set()
        if landmark_tokens & HAND_TOKENS and hand_metrics["handPartCount"] == 0:
            issues.append("landmarks mention hands or fists, but no semantic hand primitives were found")
        issues.extend(hand_issues)
    return metrics, issues


def assess_explicit(model: dict[str, Any], bricks: list[list[float | int]]) -> tuple[dict[str, Any], list[str]]:
    material_count = len({int(item[3]) for item in bricks})
    spans = []
    for axis in range(3):
        values = [float(item[axis]) for item in bricks]
        spans.append(max(values) - min(values))
    landmarks = model.get("landmarks", [])
    metrics = {
        "format": "explicit-bricks-v1",
        "brickCount": len(bricks),
        "primitiveCount": 0,
        "geometryTypeCount": 0,
        "boxRatio": 0,
        "rotatedCount": 0,
        "subtractCount": 0,
        "materialCount": material_count,
        "topThreeVolumeRatio": 0,
        "dominantMaterialRatio": 0,
        "landmarkCount": len(landmarks),
        "namedPartRatio": 1,
        "uniquePartCount": len(landmarks),
        "boundsSpan": [round(value, 6) for value in spans],
    }
    issues = []
    if len(bricks) < 1000:
        issues.append(f"brickCount {len(bricks)} is below 1000 for explicit high-detail mode")
    if material_count < 4:
        issues.append(f"materialCount {material_count} is below 4")
    if len(landmarks) < 6:
        issues.append(f"landmarkCount {len(landmarks)} is below 6")
    if any(value < 2 for value in spans):
        issues.append("explicit brick bounds must span at least 2 units on every axis")
    return metrics, issues


def self_check(metrics: dict[str, Any], issues: list[str]) -> dict[str, Any]:
    return {**metrics, "passed": not issues}


def check_model(path: Path, *, write: bool, as_json: bool) -> int:
    try:
        model = json.loads(path.read_text(encoding="utf-8"))
        if model.get("format") == "explicit-bricks-v1":
            bricks = validate_explicit_schema(model)
            metrics, issues = assess_explicit(model, bricks)
        else:
            primitives = validate_schema(model)
            metrics, issues = assess(model, primitives)
    except (OSError, json.JSONDecodeError, ModelError) as error:
        if as_json:
            print(json.dumps({"valid": False, "issues": [str(error)]}, ensure_ascii=False))
        else:
            print(f"FAIL {path}: {error}", file=sys.stderr)
        return 1

    if write:
        model["qualitySelfCheck"] = self_check(metrics, issues)
        path.write_text(json.dumps(model, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    payload = {"valid": not issues, "path": str(path), "metrics": metrics, "issues": issues}
    if as_json:
        print(json.dumps(payload, ensure_ascii=False, indent=2))
    else:
        status = "PASS" if not issues else "FAIL"
        print(f"{status} {path}")
        if metrics.get("format") == "explicit-bricks-v1":
            print(
                f"  format=explicit-bricks-v1 bricks={metrics['brickCount']} "
                f"materials={metrics['materialCount']} bounds-span={metrics['boundsSpan']} "
                f"landmarks={metrics['landmarkCount']}"
            )
        else:
            print(
                f"  primitives={metrics['primitiveCount']} types={metrics['geometryTypeCount']} "
                f"boxes={metrics['boxRatio']:.1%} rotated={metrics['rotatedCount']} "
                f"subtract={metrics['subtractCount']} materials={metrics['materialCount']}"
            )
            print(
                f"  top3-volume={metrics['topThreeVolumeRatio']:.1%} "
                f"dominant-material={metrics['dominantMaterialRatio']:.1%} "
                f"landmarks={metrics['landmarkCount']} named-parts={metrics['namedPartRatio']:.1%} "
                f"unique-parts={metrics['uniquePartCount']}"
            )
            if metrics["handPartCount"]:
                print(
                    f"  hand-parts={metrics['handPartCount']} "
                    f"articulated-sides={metrics['articulatedHandSideCount']} "
                    f"unarticulated-sides={metrics['unarticulatedHandSideCount']} "
                    f"round-whole-hands={metrics['roundWholeHandCount']}"
                )
        for issue in issues:
            print(f"  - {issue}")
        if write:
            print("  qualitySelfCheck updated")
    return 0 if not issues else 1


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    subparsers = parser.add_subparsers(dest="command", required=True)
    check = subparsers.add_parser("check", help="validate a BrickMorph model and calculate quality metrics")
    check.add_argument("model", type=Path, help="path to model JSON")
    check.add_argument("--write-self-check", action="store_true", help="write calculated qualitySelfCheck into the model")
    check.add_argument("--json", action="store_true", help="emit a machine-readable report")
    return parser


def main() -> int:
    args = build_parser().parse_args()
    if args.command == "check":
        return check_model(args.model, write=args.write_self_check, as_json=args.json)
    return 2


if __name__ == "__main__":
    raise SystemExit(main())
