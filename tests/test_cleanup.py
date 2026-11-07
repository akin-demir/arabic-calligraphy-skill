"""Branch cleanup must preserve active or unmerged work."""

import importlib.util
from pathlib import Path
import unittest
from unittest.mock import patch

SPEC = importlib.util.spec_from_file_location(
    "rc3_cleanup", Path(__file__).resolve().parents[1] / "scripts/cleanup_rc3_branches.py")
MODULE = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(MODULE)
SOURCE, HEAD = "a" * 40, "b" * 40


class Cleanup(unittest.TestCase):
    def execute(self, *, status="ahead", active=False, moved=False, apply=False, tag=SOURCE):
        calls = []

        def api(path, method="GET"):
            calls.append((path, method))
            if path == "releases/tags/v0.1.0-rc.3":
                return dict(draft=False, prerelease=True)
            if path == "git/ref/tags/v0.1.0-rc.3":
                return {"object": dict(type="commit", sha=tag)}
            if path.startswith("git/matching-refs/"):
                return [{"ref": "refs/heads/feat/done", "object": {"sha": HEAD}}]
            if path.startswith("pulls?"):
                return [dict(number=1)] if active else []
            if path.startswith("compare/"):
                return dict(status=status)
            if path == "git/ref/heads/feat/done":
                return {"object": {"sha": SOURCE if moved else HEAD}}
            if method == "DELETE":
                return None
            raise AssertionError(path)

        with patch.object(MODULE, "api", side_effect=api), patch.object(
                MODULE, "BRANCHES", {"feat/done": HEAD}):
            result = MODULE.cleanup(SOURCE, apply)
        return result, [path for path, method in calls if method == "DELETE"]

    def test_dry_run_does_not_delete(self):
        report, deletes = self.execute()
        self.assertEqual(report[0]["result"], "would delete")
        self.assertEqual(deletes, [])

    def test_merged_inactive_branch_deleted_with_apply(self):
        report, deletes = self.execute(apply=True)
        self.assertEqual(report[0]["result"], "deleted")
        self.assertEqual(deletes, ["git/refs/heads/feat/done"])

    def test_open_pr_preserved(self):
        self.assertEqual(self.execute(active=True, apply=True)[1], [])

    def test_unmerged_work_preserved(self):
        self.assertEqual(self.execute(status="diverged", apply=True)[1], [])

    def test_branch_changed_during_inspection_preserved(self):
        self.assertEqual(self.execute(moved=True, apply=True)[1], [])

    def test_wrong_release_source_refused(self):
        with self.assertRaisesRegex(ValueError, "checked source"):
            self.execute(tag=HEAD, apply=True)
