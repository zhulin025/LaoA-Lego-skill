#!/usr/bin/env python3
"""Package a BrickMorph JSON model as a self-contained interactive web viewer."""

from __future__ import annotations

import argparse
import json
import shutil
import sys
from pathlib import Path

from brick_model import (
    ModelError,
    assess,
    assess_explicit,
    self_check,
    validate_explicit_schema,
    validate_schema,
)


TOKEN = "__BRICK_MODEL_JSON__"


def safe_embedded_json(model: dict) -> str:
    payload = json.dumps(model, ensure_ascii=False, separators=(",", ":"))
    return payload.replace("</", "<\\/").replace("\u2028", "\\u2028").replace("\u2029", "\\u2029")


def package(model_path: Path, output: Path, *, make_zip: bool, force: bool) -> int:
    try:
        model = json.loads(model_path.read_text(encoding="utf-8"))
        if model.get("format") == "explicit-bricks-v1":
            bricks = validate_explicit_schema(model)
            metrics, issues = assess_explicit(model, bricks)
        else:
            primitives = validate_schema(model)
            metrics, issues = assess(model, primitives)
    except (OSError, json.JSONDecodeError, ModelError) as error:
        print(f"FAIL {model_path}: {error}", file=sys.stderr)
        return 1

    model["qualitySelfCheck"] = self_check(metrics, issues)
    skill_root = Path(__file__).resolve().parent.parent
    template_root = skill_root / "assets" / "viewer"
    template_path = template_root / "viewer-template.html"
    if not template_path.is_file():
        print(f"FAIL viewer template missing: {template_path}", file=sys.stderr)
        return 1

    if output.exists():
        if not force:
            print(f"FAIL output already exists; choose a new path or pass --force: {output}", file=sys.stderr)
            return 1
        if output.is_dir():
            shutil.rmtree(output)
        else:
            output.unlink()

    output.mkdir(parents=True)
    shutil.copytree(template_root / "vendor", output / "vendor")
    shutil.copytree(template_root / "assets", output / "assets")

    template = template_path.read_text(encoding="utf-8")
    if template.count(TOKEN) != 1:
        print(f"FAIL viewer template must contain exactly one {TOKEN} token", file=sys.stderr)
        return 1
    html = template.replace(TOKEN, safe_embedded_json(model))
    (output / "index.html").write_text(html, encoding="utf-8")
    (output / "model.json").write_text(json.dumps(model, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    archive = None
    if make_zip:
        archive = Path(shutil.make_archive(str(output), "zip", root_dir=output))

    print(f"Viewer: {output / 'index.html'}")
    print(f"Model:  {output / 'model.json'}")
    if archive:
        print(f"ZIP:    {archive}")
    detail = (
        f"{metrics['brickCount']} explicit bricks"
        if metrics.get("format") == "explicit-bricks-v1"
        else f"{metrics['primitiveCount']} primitives"
    )
    print(f"Quality: {'PASS' if not issues else 'WARNING'} · {detail} · {len(issues)} issue(s)")
    for issue in issues:
        print(f"  - {issue}")
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("model", type=Path, help="BrickMorph model JSON")
    parser.add_argument("--output", type=Path, required=True, help="new viewer directory")
    parser.add_argument("--zip", action="store_true", help="also write <output>.zip")
    parser.add_argument("--force", action="store_true", help="replace an existing output directory")
    return parser


def main() -> int:
    args = build_parser().parse_args()
    return package(args.model, args.output, make_zip=args.zip, force=args.force)


if __name__ == "__main__":
    raise SystemExit(main())
