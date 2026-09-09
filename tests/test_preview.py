"""Offline acceptance checks for the consumer-owned preview helpers."""

import contextlib
import io
import json
import os
import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from scripts import build_preview, smoke_preview

HTML = "<!doctype html><html><title>Demo</title><body>Hello</body></html>"


class PreviewBuildTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.public = self.root / "public"
        self.public.mkdir()
        (self.public / "index.html").write_text(HTML, encoding="utf-8")

    def build(self, destination=None):
        # Verification must not publish output values into a surrounding job.
        with (
            patch.dict(os.environ, {"GITHUB_OUTPUT": ""}),
            contextlib.redirect_stdout(io.StringIO()),
            contextlib.redirect_stderr(io.StringIO()),
        ):
            return build_preview.assemble_preview_artifact(
                str(self.root), str(destination or self.root / "dist")
            )

    def test_copies_only_public_files_into_canonical_dist(self):
        (self.public / "style.css").write_text("body { color: blue; }", encoding="utf-8")
        (self.public / "credentials.txt").write_text("not public", encoding="utf-8")
        (self.public / ".env").write_text("not public", encoding="utf-8")
        (self.public / "internal.json").write_text("{}", encoding="utf-8")
        self.assertTrue(self.build())
        self.assertEqual((self.root / "dist/index.html").read_text(encoding="utf-8"), HTML)
        self.assertEqual(
            {entry.name for entry in (self.root / "dist").iterdir()},
            {"index.html", "style.css"},
        )

    def test_rejects_source_symlink_without_replacing_existing_output(self):
        (self.public / "linked.html").symlink_to(self.public / "index.html")
        output = self.root / "dist"
        output.mkdir()
        marker = output / "keep.txt"
        marker.write_text("keep", encoding="utf-8")
        self.assertFalse(self.build())
        self.assertEqual(marker.read_text(encoding="utf-8"), "keep")

    def test_rejects_output_outside_source_without_mutation(self):
        with tempfile.TemporaryDirectory() as external:
            output = Path(external) / "dist"
            output.mkdir()
            marker = output / "keep.txt"
            marker.write_text("keep", encoding="utf-8")
            self.assertFalse(self.build(output))
            self.assertEqual(marker.read_text(encoding="utf-8"), "keep")

    def test_rejects_output_symlink_without_mutating_target(self):
        target = self.root / "target"
        target.mkdir()
        (self.root / "dist").symlink_to(target, target_is_directory=True)
        self.assertFalse(self.build())
        self.assertEqual(list(target.iterdir()), [])

    def test_rejects_runnable_surface_without_entrypoint(self):
        (self.public / "index.html").unlink()
        self.assertFalse(self.build())
        self.assertFalse((self.root / "dist").exists())


class PreviewSmokeTests(unittest.TestCase):
    def test_scenario_read_and_parse_failures_remain_structured(self):
        malformed = {
            "invalid JSON": b"[",
            "invalid UTF-8": b"\xff",
            "excessive nesting": b"[" * (sys.getrecursionlimit() + 1) + b"]" * (sys.getrecursionlimit() + 1),
        }
        digit_limit = sys.get_int_max_str_digits()
        if digit_limit:
            malformed["oversized integer"] = b"9" * (digit_limit + 1)
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "smoke.json"
            for label, contents in malformed.items():
                with self.subTest(label=label):
                    path.write_bytes(contents)
                    valid, scenarios, reason = smoke_preview.load_and_validate_scenarios(str(path))
                    self.assertFalse(valid)
                    self.assertIsNone(scenarios)
                    self.assertTrue(reason)
            with patch("builtins.open", side_effect=OSError("read failed")):
                valid, scenarios, reason = smoke_preview.load_and_validate_scenarios(str(path))
            self.assertFalse(valid)
            self.assertIsNone(scenarios)
            self.assertIn("read failed", reason)
            # Exercise resource limits without exhausting the test process.
            for error in (RecursionError("nesting limit"), MemoryError("input too large")):
                with self.subTest(error=type(error).__name__):
                    with patch.object(smoke_preview.json, "load", side_effect=error):
                        valid, scenarios, reason = smoke_preview.load_and_validate_scenarios(str(path))
                    self.assertFalse(valid)
                    self.assertIsNone(scenarios)
                    self.assertIn(str(error), reason)

    def test_valid_html_satisfies_repository_scenarios(self):
        scenarios_path = Path(__file__).resolve().parents[1] / ".github/scenarios/smoke.json"
        valid, scenarios, reason = smoke_preview.load_and_validate_scenarios(str(scenarios_path))
        self.assertTrue(valid, reason)
        results = smoke_preview.evaluate_html_scenarios(HTML, scenarios)
        self.assertTrue(results)
        self.assertTrue(all(result.passed for result in results))

    def test_missing_title_and_runtime_error_fail_html_acceptance(self):
        html = "<html><body>500 Internal Server Error</body></html>"
        failures = {
            result.name for result in smoke_preview.evaluate_html_scenarios(html)
            if not result.passed
        }
        self.assertEqual(failures, {"Page Title Declaration", "Absence of Runtime Errors"})

    def test_invalid_scenario_is_rejected(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "smoke.json"
            path.write_text(json.dumps([{"name": "empty assertion"}]), encoding="utf-8")
            valid, scenarios, reason = smoke_preview.load_and_validate_scenarios(str(path))
        self.assertFalse(valid)
        self.assertIsNone(scenarios)
        self.assertIn("at least one valid assertion", reason)


if __name__ == "__main__":
    unittest.main()
