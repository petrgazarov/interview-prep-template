#!/usr/bin/env python3
"""Regression checks for read-only LeetCode log queries."""

from __future__ import annotations

import sys
import unittest
from pathlib import Path


sys.path.insert(0, str(Path(__file__).resolve().parent))

from leetcode_queries import (  # noqa: E402
    active_redos,
    attempt_history,
    recent_attempts,
)


class LeetCodeQueriesTest(unittest.TestCase):
    rows = [
        {
            "date": "2026-07-01",
            "problem": "Alpha",
            "url": "https://example.com/alpha/",
            "difficulty": "medium",
            "attempt_type": "first_pass",
            "grade": "C",
            "redo_due": "2026-07-08",
            "docket_note": "Cold redo.",
        },
        {
            "date": "2026-07-02",
            "problem": "Beta",
            "url": "https://example.com/beta",
            "difficulty": "easy",
            "attempt_type": "first_pass",
            "grade": "B",
            "redo_due": "2026-07-08",
            "docket_note": "Cold redo.",
        },
        {
            "date": "2026-07-08",
            "problem": "Alpha",
            "url": "https://example.com/alpha",
            "difficulty": "medium",
            "attempt_type": "redo",
            "grade": "B",
            "redo_due": "",
            "docket_note": "",
        },
        {
            "date": "2026-07-09",
            "problem": "Gamma",
            "url": "https://example.com/gamma",
            "difficulty": "medium",
            "attempt_type": "first_pass",
            "grade": "C",
            "redo_due": "2026-07-10",
            "docket_note": "Cold redo.",
        },
    ]

    def test_history_normalizes_trailing_slashes(self) -> None:
        payload = attempt_history(self.rows, "https://example.com/alpha/")
        self.assertEqual(payload["attempt_count"], 2)
        self.assertEqual(
            [row["attempt_type"] for row in payload["attempts"]],
            ["first_pass", "redo"],
        )

    def test_recent_attempts_are_newest_first(self) -> None:
        payload = recent_attempts(self.rows, 2)
        self.assertEqual(payload["attempt_count"], 2)
        self.assertEqual(
            [row["problem"] for row in payload["attempts"]],
            ["Gamma", "Alpha"],
        )

    def test_active_redos_use_only_latest_row_per_url(self) -> None:
        payload = active_redos(self.rows)
        self.assertEqual(payload["active_redo_count"], 2)
        self.assertEqual(
            [row["problem"] for row in payload["commitments"]],
            ["Beta", "Gamma"],
        )
        self.assertEqual(
            payload["capacity_by_date"],
            {"2026-07-08": 1, "2026-07-10": 1},
        )
        for row in payload["commitments"]:
            self.assertEqual(
                set(row),
                {"problem", "url", "difficulty", "redo_due", "docket_note"},
            )

    def test_recent_limit_must_be_positive(self) -> None:
        with self.assertRaisesRegex(ValueError, "positive integer"):
            recent_attempts(self.rows, 0)


if __name__ == "__main__":
    unittest.main()
