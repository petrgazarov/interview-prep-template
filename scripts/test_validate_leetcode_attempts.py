#!/usr/bin/env python3
"""Regression checks for LeetCode attempt-log validation."""

from __future__ import annotations

import csv
import sys
import tempfile
import unittest
from pathlib import Path


sys.path.insert(0, str(Path(__file__).resolve().parent))

from validate_leetcode_attempts import (  # noqa: E402
    ASYMPTOTIC_OPTIMALITIES,
    EXPECTED_COLUMNS,
    MAX_ACTIVE_REDOS_PER_DATE,
    active_redo_capacity_errors,
    active_redo_docket_note_errors,
    validate,
)


def complete_row(**overrides: str) -> dict[str, str]:
    row = dict.fromkeys(EXPECTED_COLUMNS, "")
    row.update(
        {
            "date": "2026-08-12",
            "problem": "Example Problem",
            "url": "https://example.com/problem",
            "topic": "array",
            "difficulty": "medium",
            "attempt_type": "first_pass",
            "time_min": "23.40",
            "result": "solved",
            "grade": "A",
            "plan_score": "9",
            "correctness_content_score": "9",
            "correctness_delivery_score": "9",
            "correctness_combined_score": "9",
            "walkthrough_score": "9",
            "implementation_validation": "passed",
            "complexity_analysis": "correct",
            "code_quality_score": "9",
            "tier1_interview_outcome": "pass",
            "asymptotic_optimality": "optimal",
        }
    )
    row.update(overrides)
    return row


def write_rows(rows: list[dict[str, str]]) -> tuple[tempfile.TemporaryDirectory, Path]:
    temp_dir = tempfile.TemporaryDirectory()
    path = Path(temp_dir.name) / "leetcode_attempts.csv"
    with path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=EXPECTED_COLUMNS)
        writer.writeheader()
        writer.writerows(rows)
    return temp_dir, path


class FreshTemplateValidationTest(unittest.TestCase):
    def test_header_only_log_is_valid(self) -> None:
        temp_dir, path = write_rows([])
        self.addCleanup(temp_dir.cleanup)

        self.assertEqual(validate(path), [])

    def test_first_row_requires_complete_current_scorecard(self) -> None:
        row = complete_row(asymptotic_optimality="")
        temp_dir, path = write_rows([row])
        self.addCleanup(temp_dir.cleanup)

        self.assertIn(
            "line 2: missing required scorecard fields: "
            "['asymptotic_optimality']",
            validate(path),
        )

    def test_complete_current_row_is_valid(self) -> None:
        temp_dir, path = write_rows([complete_row()])
        self.addCleanup(temp_dir.cleanup)

        self.assertEqual(validate(path), [])

    def test_dates_require_zero_padded_iso_format(self) -> None:
        temp_dir, path = write_rows([complete_row(date="2026-8-2")])
        self.addCleanup(temp_dir.cleanup)

        self.assertIn("line 2: invalid date '2026-8-2'", validate(path))


class ActiveRedoCapacityTest(unittest.TestCase):
    @staticmethod
    def row(problem: str, url: str, redo_due: str) -> dict[str, str]:
        return {"problem": problem, "url": url, "redo_due": redo_due}

    def test_allows_one_active_redo_on_one_date(self) -> None:
        rows = [self.row("A", "https://example.com/a", "2026-08-20")]
        self.assertEqual(MAX_ACTIVE_REDOS_PER_DATE, 1)
        self.assertEqual(active_redo_capacity_errors(rows), [])

    def test_rejects_second_active_redo_on_one_date(self) -> None:
        rows = [
            self.row("A", "https://example.com/a", "2026-08-20"),
            self.row("B", "https://example.com/b", "2026-08-20"),
        ]
        self.assertEqual(
            active_redo_capacity_errors(rows),
            [
                "redo_due 2026-08-20: 2 active redos scheduled "
                "(maximum 1): A, B"
            ],
        )

    def test_latest_canonical_url_controls_capacity(self) -> None:
        rows = [
            self.row("A", "https://example.com/a/", "2026-08-20"),
            self.row("B", "https://example.com/b", "2026-08-20"),
            self.row("A", "https://example.com/a", ""),
        ]
        self.assertEqual(active_redo_capacity_errors(rows), [])


class ActiveRedoDocketNoteTest(unittest.TestCase):
    @staticmethod
    def row(
        problem: str, url: str, redo_due: str, docket_note: str
    ) -> dict[str, str]:
        return {
            "problem": problem,
            "url": url,
            "redo_due": redo_due,
            "docket_note": docket_note,
        }

    def test_accepts_ordinary_and_staged_contracts(self) -> None:
        rows = [
            self.row(
                "Ordinary",
                "https://example.com/ordinary",
                "2026-08-20",
                "Cold same-problem redo without hints or external references; "
                "finish within 25-30 minutes under the standard attempt protocol.",
            ),
            self.row(
                "Staged",
                "https://example.com/staged",
                "2026-08-21",
                "Cold same-problem alternate-implementation redo without hints "
                "or external references; use a different implementation. The "
                "exact approach is intentionally withheld.",
            ),
        ]
        self.assertEqual(active_redo_docket_note_errors(rows), [])

    def test_rejects_diagnostic_prose(self) -> None:
        rows = [
            self.row(
                "Unsafe",
                "https://example.com/unsafe",
                "2026-08-20",
                "Redo the bug that failed last time.",
            )
        ]
        self.assertEqual(
            active_redo_docket_note_errors(rows),
            [
                "active redo 'Unsafe': docket_note must use the ordinary "
                "cold-redo contract or an explicitly withheld staged contract"
            ],
        )

    def test_rejects_diagnostic_prose_inside_staged_contract(self) -> None:
        rows = [
            self.row(
                "Unsafe staged",
                "https://example.com/unsafe-staged",
                "2026-08-20",
                "Cold same-problem alternate-implementation redo without hints "
                "or external references; last time you missed dynamic programming. "
                "The exact approach is intentionally withheld.",
            )
        ]
        self.assertEqual(
            active_redo_docket_note_errors(rows),
            [
                "active redo 'Unsafe staged': docket_note must use the ordinary "
                "cold-redo contract or an explicitly withheld staged contract"
            ],
        )


class AsymptoticOptimalityValidationTest(unittest.TestCase):
    def test_accepts_every_label(self) -> None:
        for value in ASYMPTOTIC_OPTIMALITIES:
            with self.subTest(value=value):
                temp_dir, path = write_rows(
                    [complete_row(asymptotic_optimality=value)]
                )
                try:
                    self.assertEqual(validate(path), [])
                finally:
                    temp_dir.cleanup()

    def test_rejects_invalid_label(self) -> None:
        temp_dir, path = write_rows(
            [complete_row(asymptotic_optimality="almost_optimal")]
        )
        self.addCleanup(temp_dir.cleanup)

        self.assertIn(
            "line 2: invalid asymptotic_optimality 'almost_optimal'",
            validate(path),
        )


class CalibrationPolicyTest(unittest.TestCase):
    def test_tradeoff_boundary_requires_research(self) -> None:
        skill_dir = (
            Path(__file__).resolve().parents[1]
            / ".agents"
            / "skills"
            / "record-leetcode-attempt"
        )
        skill = (skill_dir / "SKILL.md").read_text(encoding="utf-8")
        policy = (
            skill_dir / "references" / "grading-calibration.md"
        ).read_text(encoding="utf-8")
        normalized = " ".join(policy.split())

        self.assertIn("references/grading-calibration.md", skill)
        self.assertIn("### Required calibration research", normalized)
        self.assertIn("at least two independent, credible", normalized)
        self.assertIn("Cite the sources in the feedback", normalized)
        self.assertIn("Best judgment is the fallback after research", normalized)


if __name__ == "__main__":
    unittest.main()
