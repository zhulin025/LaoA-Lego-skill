#!/usr/bin/env python3
"""Regression tests for BrickMorph semantic quality checks."""

from __future__ import annotations

import unittest
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from brick_model import assess_hand_articulation


def primitive(kind: str, part: str) -> dict:
    if kind == "capsule":
        return {
            "type": kind,
            "op": "add",
            "start": [0, 0, 0],
            "end": [0, 1, 0],
            "radius": 1,
            "material": 0,
            "part": part,
        }
    return {
        "type": kind,
        "op": "add",
        "center": [0, 0, 0],
        "size": [1, 1, 1],
        "rotation": [0, 0, 0],
        "material": 0,
        "part": part,
    }


class HandArticulationTests(unittest.TestCase):
    def test_round_ball_hands_fail(self):
        metrics, issues = assess_hand_articulation(
            [primitive("ellipsoid", "left_hand"), primitive("ellipsoid", "right_fist")]
        )
        self.assertEqual(metrics["roundWholeHandCount"], 2)
        self.assertEqual(metrics["unarticulatedHandSideCount"], 2)
        self.assertTrue(any("featureless round" in issue for issue in issues))

    def test_segmented_hands_pass(self):
        parts = []
        for side in ("left", "right"):
            parts.extend(
                [
                    primitive("box", f"{side}_palm"),
                    primitive("frustum", f"{side}_thumb"),
                    primitive("box", f"{side}_finger_block_outer"),
                    primitive("box", f"{side}_finger_block_inner"),
                    primitive("cylinder", f"{side}_wrist"),
                ]
            )
        metrics, issues = assess_hand_articulation(parts)
        self.assertEqual(metrics["articulatedHandSideCount"], 2)
        self.assertEqual(metrics["unarticulatedHandSideCount"], 0)
        self.assertEqual(metrics["roundWholeHandCount"], 0)
        self.assertEqual(issues, [])

    def test_unscoped_hand_names_fail(self):
        metrics, issues = assess_hand_articulation([primitive("box", "palm"), primitive("box", "thumb")])
        self.assertEqual(metrics["articulatedHandSideCount"], 0)
        self.assertTrue(any("left or right" in issue for issue in issues))


if __name__ == "__main__":
    unittest.main()
