import os
import stat
import tempfile
import unittest
from pathlib import Path

from setup_company import WORKSHEETS, initialize


class SetupWorkspaceTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.repository = Path(self.temp.name) / "checkout"
        templates = self.repository / "templates"
        templates.mkdir(parents=True)
        for name in WORKSHEETS:
            (templates / name).write_text("# Blank " + name + "\n", encoding="utf-8")

    def test_creates_private_worksheets_without_changing_sources(self):
        directory, created, preserved = initialize(self.repository / ".company", self.repository)
        self.assertEqual(set(created), set(WORKSHEETS))
        self.assertEqual(preserved, [])
        for name in WORKSHEETS:
            self.assertEqual((directory / name).read_bytes(), (self.repository / "templates" / name).read_bytes())
            if os.name == "posix":
                self.assertEqual(stat.S_IMODE((directory / name).stat().st_mode), 0o600)

    def test_resume_preserves_existing_company_answers(self):
        directory, _, _ = initialize(self.repository / ".company", self.repository)
        answer = directory / "company-profile.md"
        answer.write_text("Existing approved company answers\n", encoding="utf-8")
        _, created, preserved = initialize(directory, self.repository)
        self.assertEqual(created, [])
        self.assertEqual(set(preserved), set(WORKSHEETS))
        self.assertEqual(answer.read_text(), "Existing approved company answers\n")

    def test_rejects_public_checkout_destinations(self):
        for destination in (self.repository, self.repository / "docs", self.repository / "templates"):
            with self.assertRaises(ValueError):
                initialize(destination, self.repository)
        self.assertFalse((self.repository / "company-profile.md").exists())

    def test_missing_source_writes_no_partial_workspace(self):
        (self.repository / "templates" / WORKSHEETS[-1]).unlink()
        destination = self.repository / ".company"
        with self.assertRaises(FileNotFoundError):
            initialize(destination, self.repository)
        self.assertFalse(destination.exists())

    @unittest.skipUnless(hasattr(os, "symlink"), "symbolic links unavailable")
    def test_does_not_follow_existing_worksheet_symlink(self):
        destination = self.repository / ".company"
        destination.mkdir()
        existing = Path(self.temp.name) / "existing-record.md"
        existing.write_text("Do not overwrite\n", encoding="utf-8")
        (destination / WORKSHEETS[0]).symlink_to(existing)
        _, _, preserved = initialize(destination, self.repository)
        self.assertIn(WORKSHEETS[0], preserved)
        self.assertEqual(existing.read_text(), "Do not overwrite\n")

    def test_allows_explicit_external_workspace(self):
        requested = Path(self.temp.name) / "approved-private-workspace"
        destination, created, _ = initialize(requested, self.repository)
        self.assertEqual(destination, requested.resolve())
        self.assertEqual(len(created), 6)


if __name__ == "__main__":
    unittest.main()
