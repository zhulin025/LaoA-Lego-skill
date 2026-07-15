#!/usr/bin/env python3
"""Regression tests for viewer reference-image packaging."""

from __future__ import annotations

import json
import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from build_viewer import package


def model(**metadata: str) -> dict:
    return {
        "version": "1.0",
        "format": "explicit-bricks-v1",
        "name": "测试模型",
        "subjectClass": "object",
        "palette": ["#ffffff"],
        "landmarks": [],
        "requestedBrickCount": 1,
        "bricks": [[0, 0, 0, 0]],
        **metadata,
    }


class ViewerReferenceTests(unittest.TestCase):
    def build(self, payload: dict, images: dict[str, bytes] | None = None) -> tuple[Path, str]:
        root = Path(self.temp_dir.name)
        for relative, content in (images or {}).items():
            path = root / relative
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_bytes(content)
        model_path = root / "model.json"
        model_path.write_text(json.dumps(payload), encoding="utf-8")
        output = root / "viewer"
        result = package(model_path, output, make_zip=False, force=False)
        self.assertEqual(result, 0)
        return output, (output / "index.html").read_text(encoding="utf-8")

    def setUp(self) -> None:
        self.temp_dir = tempfile.TemporaryDirectory()

    def tearDown(self) -> None:
        self.temp_dir.cleanup()

    def test_concept_reference_is_packaged_as_fallback(self):
        output, html = self.build(
            model(conceptReference="reference/concept.png"),
            {"reference/concept.png": b"concept"},
        )
        self.assertEqual((output / "assets/reference-image.png").read_bytes(), b"concept")
        self.assertIn('"label":"建模概念图"', html)
        self.assertIn("width: 100%; height: auto", html)
        self.assertIn("position: fixed; top: 70px; right: 20px", html)
        self.assertNotIn("height: 98px; object-fit: cover", html)

    def test_user_reference_takes_priority_over_concept(self):
        output, html = self.build(
            model(
                identityReference="reference/user.jpg",
                conceptReference="reference/concept.png",
            ),
            {
                "reference/user.jpg": b"user",
                "reference/concept.png": b"concept",
            },
        )
        self.assertEqual((output / "assets/reference-image.jpg").read_bytes(), b"user")
        self.assertIn('"label":"用户参考图"', html)
        self.assertFalse((output / "assets/reference-image.png").exists())

    def test_viewer_hides_preview_without_reference(self):
        _, html = self.build(model())
        self.assertIn("const REFERENCE_IMAGE = null;", html)


if __name__ == "__main__":
    unittest.main()
