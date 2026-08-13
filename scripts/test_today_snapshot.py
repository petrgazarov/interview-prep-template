#!/usr/bin/env python3
"""Regression checks for the DSA-only $today snapshot and policy."""

from __future__ import annotations

import csv
import sys
import tempfile
import unittest
from datetime import date
from pathlib import Path


sys.path.insert(0, str(Path(__file__).resolve().parent))

from today_snapshot import build_leetcode_snapshot  # noqa: E402
from validate_leetcode_attempts import EXPECTED_COLUMNS  # noqa: E402


def write_attempts(root: Path, rows: list[dict[str, str]]) -> None:
    with (root / "leetcode_attempts.csv").open(
        "w", newline="", encoding="utf-8"
    ) as f:
        writer = csv.DictWriter(f, fieldnames=EXPECTED_COLUMNS)
        writer.writeheader()
        writer.writerows(rows)


class DsaSnapshotTest(unittest.TestCase):
    def test_empty_template_is_valid_snapshot_input(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            write_attempts(root, [])
            data_quality: list[str] = []
            snapshot = build_leetcode_snapshot(
                root, date(2026, 8, 12), data_quality
            )

        self.assertEqual(data_quality, [])
        self.assertEqual(snapshot["row_count"], 0)
        self.assertEqual(snapshot["latest_problem_count"], 0)
        self.assertEqual(snapshot["due_redos"], [])

    def test_malformed_header_is_reported(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            (root / "leetcode_attempts.csv").write_text(
                "wrong,header\n", encoding="utf-8"
            )
            data_quality: list[str] = []
            snapshot = build_leetcode_snapshot(
                root, date(2026, 8, 12), data_quality
            )

        self.assertEqual(snapshot["row_count"], 0)
        self.assertEqual(len(data_quality), 1)
        self.assertIn("header mismatch", data_quality[0])

    def test_due_redo_carries_only_public_contract_fields(self) -> None:
        row = dict.fromkeys(EXPECTED_COLUMNS, "")
        row.update(
            {
                "date": "2026-08-01",
                "problem": "Example Problem",
                "url": "https://example.com/problem",
                "difficulty": "hard",
                "attempt_type": "first_pass",
                "redo_due": "2026-08-12",
                "redo_target": "hidden diagnostic target",
                "what_went_wrong": "hidden failure evidence",
                "docket_note": (
                    "Cold same-problem redo without hints or external references; "
                    "finish within 25-30 minutes under the standard attempt protocol."
                ),
            }
        )

        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            write_attempts(root, [row])
            data_quality: list[str] = []
            snapshot = build_leetcode_snapshot(
                root, date(2026, 8, 12), data_quality
            )

        self.assertEqual(data_quality, [])
        self.assertEqual(len(snapshot["due_redos"]), 1)
        self.assertEqual(
            set(snapshot["due_redos"][0]),
            {"problem", "redo_due", "url", "docket_note"},
        )
        self.assertNotIn("difficulty", snapshot["due_redos"][0])
        self.assertNotIn("redo_target", snapshot["due_redos"][0])

    def test_completed_attempt_does_not_claim_study_time(self) -> None:
        row = dict.fromkeys(EXPECTED_COLUMNS, "")
        row.update(
            {
                "date": "2026-08-12",
                "problem": "Example Problem",
                "url": "https://example.com/problem",
                "difficulty": "medium",
                "attempt_type": "first_pass",
                "time_min": "22.87",
            }
        )

        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            write_attempts(root, [row])
            snapshot = build_leetcode_snapshot(
                root, date(2026, 8, 12), []
            )

        completed = snapshot["completed_today"]
        self.assertEqual(completed["attempt_count"], 1)
        self.assertNotIn("time_min", completed["attempts"][0])

    def test_latest_url_row_controls_redo_state(self) -> None:
        first = dict.fromkeys(EXPECTED_COLUMNS, "")
        first.update(
            {
                "date": "2026-08-01",
                "problem": "Example",
                "url": "https://example.com/problem/",
                "redo_due": "2026-08-12",
                "docket_note": "old contract",
            }
        )
        second = dict(first)
        second.update(
            {
                "date": "2026-08-12",
                "url": "https://example.com/problem",
                "redo_due": "",
                "docket_note": "",
            }
        )

        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            write_attempts(root, [first, second])
            snapshot = build_leetcode_snapshot(
                root, date(2026, 8, 12), []
            )

        self.assertEqual(snapshot["latest_problem_count"], 1)
        self.assertEqual(snapshot["due_redos"], [])


class RepositoryPolicyTest(unittest.TestCase):
    def setUp(self) -> None:
        self.root = Path(__file__).resolve().parent.parent

    def test_empty_live_csv_owns_current_schema(self) -> None:
        with (self.root / "leetcode_attempts.csv").open(
            newline="", encoding="utf-8-sig"
        ) as f:
            reader = csv.DictReader(f)
            rows = list(reader)

        self.assertEqual(reader.fieldnames, EXPECTED_COLUMNS)
        self.assertEqual(rows, [])

        skill = (
            self.root
            / ".agents/skills/record-leetcode-attempt/SKILL.md"
        ).read_text(encoding="utf-8")
        self.assertIn(
            "Treat the current `leetcode_attempts.csv` header as the "
            "canonical schema.",
            skill,
        )

    def test_pre_attempt_policy_has_one_public_contract(self) -> None:
        agents = (self.root / "AGENTS.md").read_text(encoding="utf-8")
        record = (
            self.root
            / ".agents/skills/record-leetcode-attempt/SKILL.md"
        ).read_text(encoding="utf-8")
        today = (
            self.root / ".agents/skills/today/SKILL.md"
        ).read_text(encoding="utf-8")

        self.assertIn("Pre-attempt disclosure is allowlist-based", agents)
        self.assertIn("opens its post-attempt review", agents)
        self.assertIn("prospective public assignment contract", record)
        self.assertIn("authoritative public assignment contract", today)

    def test_template_uses_local_time_and_external_lists(self) -> None:
        agents = (self.root / "AGENTS.md").read_text(encoding="utf-8")
        today = (
            self.root / ".agents/skills/today/SKILL.md"
        ).read_text(encoding="utf-8")

        self.assertIn("runtime's local timezone", agents)
        self.assertIn("repository deliberately does not duplicate", agents)
        self.assertIn("This repository owns no queue", today)
        self.assertIn("preserve the user's best focus for unseen", today)
        self.assertIn("without inventing hours", today)
        self.assertNotIn("PT_ZONE", agents + today)

    def test_readme_explains_forking_and_both_primary_skills(self) -> None:
        readme = (self.root / "README.md").read_text(encoding="utf-8")

        self.assertIn("from this GitHub template", readme)
        self.assertIn("$today", readme)
        self.assertIn("$record-leetcode-attempt", readme)
        self.assertIn(
            "Problem statement with examples and constraints copy-pasted",
            readme,
        )
        self.assertIn("one continuous transcript", readme)
        self.assertIn("Python 3.10+", readme)

    def test_claude_code_uses_the_same_instructions_and_skills(self) -> None:
        self.assertEqual(
            (self.root / "CLAUDE.md").read_text(encoding="utf-8"),
            "@AGENTS.md\n",
        )
        for name in ["today", "record-leetcode-attempt"]:
            claude_skill = self.root / ".claude" / "skills" / name
            self.assertTrue(claude_skill.is_symlink())
            self.assertEqual(
                claude_skill.resolve(),
                (self.root / ".agents" / "skills" / name).resolve(),
            )

if __name__ == "__main__":
    unittest.main()
