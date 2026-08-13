#!/usr/bin/env python3
"""Validate the LeetCode attempts CSV used by repo skills."""

from __future__ import annotations

import argparse
import csv
import re
import sys
from collections import defaultdict
from datetime import datetime
from decimal import Decimal, InvalidOperation
from pathlib import Path
from urllib.parse import urlparse

from leetcode_queries import canonical_url


EXPECTED_COLUMNS = [
    "date",
    "problem",
    "url",
    "topic",
    "difficulty",
    "attempt_type",
    "time_min",
    "result",
    "grade",
    "redo_due",
    "what_went_wrong",
    "transfer_skill",
    "adjacent_drills",
    "redo_target",
    "notes",
    "plan_score",
    "correctness_content_score",
    "correctness_delivery_score",
    "correctness_combined_score",
    "walkthrough_score",
    "implementation_validation",
    "complexity_analysis",
    "docket_note",
    "code_quality_score",
    "tier1_interview_outcome",
    "asymptotic_optimality",
]

SCORE_FIELDS = [
    "plan_score",
    "correctness_content_score",
    "correctness_delivery_score",
    "correctness_combined_score",
    "walkthrough_score",
]
CODE_QUALITY_FIELD = "code_quality_score"
SCORECARD_FIELDS = SCORE_FIELDS + [
    "implementation_validation",
    "complexity_analysis",
    "asymptotic_optimality",
]
DIFFICULTIES = {"easy", "medium", "hard", "custom"}
ATTEMPT_TYPES = {"first_pass", "redo", "mock"}
RESULTS = {"solved", "partial", "failed"}
GRADES = {"A", "B", "C", "D"}
IMPLEMENTATION_VALIDATIONS = {"passed", "partial", "failed"}
COMPLEXITY_ANALYSES = {"correct", "partial", "incorrect"}
TIER1_INTERVIEW_OUTCOMES = {"strong_pass", "pass", "borderline", "fail"}
ASYMPTOTIC_OPTIMALITIES = {
    "optimal",
    "acceptable_tradeoff",
    "minor_gap",
    "material_gap",
    "major_gap",
    "unclear",
}
TIME_RE = re.compile(r"\d+\.\d{2}")
SCORE_RE = re.compile(r"(?:10|[0-9])")
FOLLOWUP_LABEL_RE = re.compile(
    r"\b(?:Transfer skill|Adjacent drills|Cold redo target|Redo target):"
)
ORDINARY_DOCKET_NOTE_RE = re.compile(
    r"Cold same-problem redo without hints or external references"
    r"(?:; finish within (?:\d+(?:-\d+)? minutes|the standard interview window))?"
    r" under the standard attempt protocol\."
)
STAGED_DIAGNOSTIC_RE = re.compile(
    r"\b(?:last time|previous(?:ly)?|failed?|mistake|bug|missed|grade|"
    r"because|struggl\w*|slow|hinted|editorial|score|result)\b",
    re.IGNORECASE,
)
MAX_ACTIVE_REDOS_PER_DATE = 1


def valid_date(value: str) -> bool:
    if not re.fullmatch(r"\d{4}-\d{2}-\d{2}", value):
        return False
    try:
        datetime.strptime(value, "%Y-%m-%d")
    except ValueError:
        return False
    return True


def valid_url(value: str) -> bool:
    parsed = urlparse(value)
    return parsed.scheme in {"http", "https"} and bool(parsed.netloc)


def active_redo_capacity_errors(rows: list[dict[str, str]]) -> list[str]:
    """Return capacity errors for active redo commitments.

    Only the latest row for each canonical problem URL controls active state.
    """
    latest_by_url: dict[str, dict[str, str]] = {}
    for row in rows:
        url = canonical_url(row.get("url", ""))
        if url:
            latest_by_url[url] = row

    redos_by_date: dict[str, list[str]] = defaultdict(list)
    for row in latest_by_url.values():
        redo_due = (row.get("redo_due") or "").strip()
        if not redo_due or not valid_date(redo_due):
            continue
        problem = (row.get("problem") or "").strip()
        redos_by_date[redo_due].append(problem or (row.get("url") or "").strip())

    errors: list[str] = []
    for redo_due, problems in sorted(redos_by_date.items()):
        if len(problems) <= MAX_ACTIVE_REDOS_PER_DATE:
            continue
        errors.append(
            f"redo_due {redo_due}: {len(problems)} active redos scheduled "
            f"(maximum {MAX_ACTIVE_REDOS_PER_DATE}): {', '.join(sorted(problems))}"
        )
    return errors


def active_redo_docket_note_errors(rows: list[dict[str, str]]) -> list[str]:
    """Reject active public notes that are not assignment contracts."""
    latest_by_url: dict[str, dict[str, str]] = {}
    for row in rows:
        url = canonical_url(row.get("url", ""))
        if url:
            latest_by_url[url] = row

    errors: list[str] = []
    for row in latest_by_url.values():
        if not (row.get("redo_due") or "").strip():
            continue

        problem = (row.get("problem") or row.get("url") or "unknown").strip()
        note = (row.get("docket_note") or "").strip()
        ordinary = bool(ORDINARY_DOCKET_NOTE_RE.fullmatch(note))
        staged = (
            note.startswith("Cold same-problem ")
            and "without hints or external references" in note
            and note.endswith("The exact approach is intentionally withheld.")
            and not STAGED_DIAGNOSTIC_RE.search(note)
        )
        if not ordinary and not staged:
            errors.append(
                f"active redo {problem!r}: docket_note must use the ordinary "
                "cold-redo contract or an explicitly withheld staged contract"
            )
    return errors


def validate(path: Path) -> list[str]:
    errors: list[str] = []
    with path.open(newline="", encoding="utf-8-sig") as f:
        reader = csv.DictReader(f)
        if reader.fieldnames != EXPECTED_COLUMNS:
            errors.append(
                f"header mismatch: expected {EXPECTED_COLUMNS}, got {reader.fieldnames}"
            )
            return errors

        rows = list(reader)

    for row_number, row in enumerate(rows, start=2):
        extra = row.get(None)
        if extra:
            errors.append(f"line {row_number}: extra columns: {extra}")

        missing_columns = [
            field for field in EXPECTED_COLUMNS if row.get(field) is None
        ]
        if missing_columns:
            errors.append(f"line {row_number}: missing columns: {missing_columns}")
            continue

        for field in [
            "date",
            "problem",
            "url",
            "topic",
            "difficulty",
            "attempt_type",
            "time_min",
            "result",
            "grade",
        ]:
            if not (row.get(field) or "").strip():
                errors.append(f"line {row_number}: missing {field}")

        date = row.get("date", "")
        if date and not valid_date(date):
            errors.append(f"line {row_number}: invalid date {date!r}")

        url = row.get("url", "")
        if url and not valid_url(url):
            errors.append(f"line {row_number}: invalid url {url!r}")

        redo_due = row.get("redo_due", "")
        if redo_due and not valid_date(redo_due):
            errors.append(f"line {row_number}: invalid redo_due {redo_due!r}")
        if redo_due and not (row.get("redo_target") or "").strip():
            errors.append(
                f"line {row_number}: missing redo_target for scheduled redo"
            )
        if redo_due and not (row.get("docket_note") or "").strip():
            errors.append(
                f"line {row_number}: missing docket_note for scheduled redo"
            )

        difficulty = row.get("difficulty", "")
        if difficulty and difficulty not in DIFFICULTIES:
            errors.append(f"line {row_number}: invalid difficulty {difficulty!r}")

        attempt_type = row.get("attempt_type", "")
        if attempt_type and attempt_type not in ATTEMPT_TYPES:
            errors.append(f"line {row_number}: invalid attempt_type {attempt_type!r}")

        result = row.get("result", "")
        if result and result not in RESULTS:
            errors.append(f"line {row_number}: invalid result {result!r}")

        grade = row.get("grade", "")
        if grade and grade not in GRADES:
            errors.append(f"line {row_number}: invalid grade {grade!r}")

        scorecard = {
            field: (row.get(field) or "").strip() for field in SCORECARD_FIELDS
        }
        scorecard_populated = [field for field, value in scorecard.items() if value]
        if len(scorecard_populated) != len(SCORECARD_FIELDS):
            missing_scorecard = [
                field for field, value in scorecard.items() if not value
            ]
            errors.append(
                f"line {row_number}: missing required scorecard fields: {missing_scorecard}"
            )
        for field in SCORE_FIELDS:
            value = scorecard[field]
            if value and not SCORE_RE.fullmatch(value):
                errors.append(
                    f"line {row_number}: {field} must be a whole number from 0 through 10, got {value!r}"
                )

        code_quality_score = (row.get(CODE_QUALITY_FIELD) or "").strip()
        if not code_quality_score:
            errors.append(
                f"line {row_number}: missing required {CODE_QUALITY_FIELD}"
            )
        elif code_quality_score and not SCORE_RE.fullmatch(code_quality_score):
            errors.append(
                f"line {row_number}: {CODE_QUALITY_FIELD} must be a whole number from 0 through 10, got {code_quality_score!r}"
            )

        tier1_interview_outcome = (
            row.get("tier1_interview_outcome") or ""
        ).strip()
        if not tier1_interview_outcome:
            errors.append(
                f"line {row_number}: missing required tier1_interview_outcome"
            )
        elif (
            tier1_interview_outcome
            and tier1_interview_outcome not in TIER1_INTERVIEW_OUTCOMES
        ):
            errors.append(
                f"line {row_number}: invalid tier1_interview_outcome {tier1_interview_outcome!r}"
            )

        implementation_validation = scorecard["implementation_validation"]
        if (
            implementation_validation
            and implementation_validation not in IMPLEMENTATION_VALIDATIONS
        ):
            errors.append(
                f"line {row_number}: invalid implementation_validation {implementation_validation!r}"
            )

        complexity_analysis = scorecard["complexity_analysis"]
        if complexity_analysis and complexity_analysis not in COMPLEXITY_ANALYSES:
            errors.append(
                f"line {row_number}: invalid complexity_analysis {complexity_analysis!r}"
            )

        asymptotic_optimality = scorecard["asymptotic_optimality"]
        if (
            asymptotic_optimality
            and asymptotic_optimality not in ASYMPTOTIC_OPTIMALITIES
        ):
            errors.append(
                f"line {row_number}: invalid asymptotic_optimality "
                f"{asymptotic_optimality!r}"
            )

        what_went_wrong = (row.get("what_went_wrong") or "").strip()
        clean_no_redo = (
            row.get("grade") == "A"
            and row.get("result") == "solved"
            and not (row.get("redo_due") or "").strip()
        )
        if what_went_wrong.lower() == "none":
            errors.append(
                f"line {row_number}: leave what_went_wrong blank instead of using 'none'"
            )
        elif not what_went_wrong and not clean_no_redo:
            errors.append(
                f"line {row_number}: missing what_went_wrong for non-clean or scheduled-redo attempt"
            )

        time_min = row.get("time_min", "")
        if time_min:
            if not TIME_RE.fullmatch(time_min):
                errors.append(
                    f"line {row_number}: time_min must be decimal minutes with two decimals, got {time_min!r}"
                )
            try:
                if Decimal(time_min) < 0:
                    errors.append(f"line {row_number}: time_min is negative")
            except InvalidOperation:
                errors.append(f"line {row_number}: invalid decimal time_min {time_min!r}")

        notes = row.get("notes", "")
        if FOLLOWUP_LABEL_RE.search(notes):
            errors.append(
                f"line {row_number}: move transfer/adjacent/redo target labels out of notes into dedicated columns"
            )

    errors.extend(active_redo_capacity_errors(rows))
    errors.extend(active_redo_docket_note_errors(rows))
    return errors


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "path",
        nargs="?",
        default="leetcode_attempts.csv",
        help="Path to leetcode_attempts.csv",
    )
    args = parser.parse_args()

    errors = validate(Path(args.path))
    if errors:
        for error in errors:
            print(error, file=sys.stderr)
        return 1

    print(f"OK: {args.path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
