#!/usr/bin/env python3
"""Build a read-only JSON snapshot for the $today skill."""

from __future__ import annotations

import argparse
import csv
import json
import subprocess
import sys
from collections import Counter
from datetime import date, datetime
from pathlib import Path

from leetcode_queries import canonical_url
from validate_leetcode_attempts import EXPECTED_COLUMNS


def parse_iso_date(value: str) -> date | None:
    value = (value or "").strip()
    if not value:
        return None
    try:
        return date.fromisoformat(value)
    except ValueError:
        return None


def read_csv(
    path: Path, data_quality: list[str]
) -> tuple[list[str], list[dict[str, str]]]:
    if not path.exists():
        data_quality.append(f"missing file: {path}")
        return [], []

    with path.open(newline="", encoding="utf-8-sig") as f:
        reader = csv.DictReader(f)
        headers = list(reader.fieldnames or [])
        if headers != EXPECTED_COLUMNS:
            data_quality.append(
                f"{path}: header mismatch: expected {EXPECTED_COLUMNS}, "
                f"got {headers}"
            )
            return headers, []
        rows: list[dict[str, str]] = []
        for row_number, row in enumerate(reader, start=2):
            extra = row.pop(None, None)
            if extra:
                data_quality.append(
                    f"{path}: line {row_number}: extra columns: {extra}"
                )
            clean_row = {key: value or "" for key, value in row.items()}
            clean_row["_row_number"] = str(row_number)
            rows.append(clean_row)

    return headers, rows


def record_invalid_dates(
    path: Path,
    rows: list[dict[str, str]],
    fields: list[str],
    data_quality: list[str],
) -> None:
    for row in rows:
        for field in fields:
            value = (row.get(field) or "").strip()
            if value and not parse_iso_date(value):
                data_quality.append(
                    f"{path}: line {row.get('_row_number')}: "
                    f"invalid {field} {value!r}"
                )


def pick(row: dict[str, str], fields: list[str]) -> dict[str, str]:
    return {field: row.get(field, "") for field in fields}


def dsa_issue_labels(row: dict[str, str]) -> list[str]:
    """Return coarse internal labels without exposing diagnostic prose."""
    wrong = (row.get("what_went_wrong") or "").lower()
    labels: list[str] = []

    if any(term in wrong for term in ["complexity", "space complexity", "time analysis"]):
        labels.append("complexity issue")
    if any(term in wrong for term in ["explain", "explanation"]):
        labels.append("explanation issue")
    if any(term in wrong for term in ["follow-up", "followup", "alternate", "staged"]):
        labels.append("follow-up issue")
    if any(
        term in wrong
        for term in [
            "could not derive",
            "conceptual",
            "model",
            "approach",
            "editorial",
            "hint",
            "missed",
            "recognized",
            "recognizing",
            "prove",
            "proof",
            "contract",
        ]
    ):
        labels.append("conceptual mistake")
    if any(
        term in wrong
        for term in [
            "bug",
            "wrong",
            "syntax",
            "base-case",
            "base case",
            "runtime",
            "mutation",
            "guard",
            "submission",
        ]
    ):
        labels.append("implementation mistake")
    if any(term in wrong for term in ["slow", "pacing", "borderline"]):
        labels.append("slow")

    if not labels:
        labels.append("main-problem issue")

    return list(dict.fromkeys(labels))[:2]


def sort_by_redo_due_then_problem(row: dict[str, str]) -> tuple[date, str]:
    return (
        parse_iso_date(row.get("redo_due", "")) or date.max,
        row.get("problem", ""),
    )


def build_leetcode_snapshot(
    root: Path, today: date, data_quality: list[str]
) -> dict:
    path = root / "leetcode_attempts.csv"
    headers, rows = read_csv(path, data_quality)
    record_invalid_dates(path, rows, ["date", "redo_due"], data_quality)

    missing_url_rows = [
        row.get("_row_number", "")
        for row in rows
        if not (row.get("url") or "").strip()
    ]

    latest_by_url: dict[str, dict[str, str]] = {}
    for row in rows:
        url = canonical_url(row.get("url", ""))
        if url:
            latest_by_url[url] = row

    attempt_summary_fields = [
        "date",
        "problem",
        "difficulty",
        "attempt_type",
        "url",
    ]
    redo_contract_fields = ["problem", "redo_due", "url", "docket_note"]

    todays_rows = [
        row for row in rows if parse_iso_date(row.get("date", "")) == today
    ]
    today_count_by_attempt_type = Counter(
        (row.get("attempt_type") or "").strip() or "blank"
        for row in todays_rows
    )

    due: list[dict[str, str]] = []
    future: list[dict[str, str]] = []
    adjacent_focus: list[dict] = []
    for row in latest_by_url.values():
        redo_due = parse_iso_date(row.get("redo_due", ""))
        item = pick(row, redo_contract_fields)
        if redo_due and not (row.get("docket_note") or "").strip():
            data_quality.append(
                f"{path}: line {row.get('_row_number')}: "
                "active redo missing docket_note"
            )
        if redo_due and redo_due <= today:
            due.append(item)
        elif redo_due:
            future.append(item)

        if (row.get("transfer_skill") or "").strip() or (
            row.get("adjacent_drills") or ""
        ).strip():
            adjacent_focus.append(
                {
                    "date": row.get("date", ""),
                    "problem": row.get("problem", ""),
                    "difficulty": row.get("difficulty", ""),
                    "grade": row.get("grade", ""),
                    "redo_due": row.get("redo_due", ""),
                    "has_transfer_skill": bool(
                        (row.get("transfer_skill") or "").strip()
                    ),
                    "has_adjacent_drills": bool(
                        (row.get("adjacent_drills") or "").strip()
                    ),
                    "issue_labels": dsa_issue_labels(row),
                    "url": row.get("url", ""),
                }
            )

    due.sort(key=sort_by_redo_due_then_problem)
    future.sort(key=sort_by_redo_due_then_problem)

    recent = [
        pick(row, attempt_summary_fields)
        for row in sorted(
            latest_by_url.values(),
            key=lambda item: int(item.get("_row_number", "0") or 0),
        )[-10:]
    ]

    return {
        "path": "leetcode_attempts.csv",
        "headers": headers,
        "row_count": len(rows),
        "latest_problem_count": len(latest_by_url),
        "missing_url_rows": missing_url_rows,
        "completed_today": {
            "attempt_count": len(todays_rows),
            "count_by_attempt_type": dict(today_count_by_attempt_type),
            "attempts": [pick(row, attempt_summary_fields) for row in todays_rows],
        },
        "due_redos": due,
        "next_future_redos": future[:8],
        "latest_adjacent_focus": adjacent_focus[-10:],
        "recent_latest_attempts": recent,
    }


def git_status_short(root: Path) -> list[str]:
    result = subprocess.run(
        ["git", "status", "--short"],
        cwd=root,
        check=False,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
    )
    if result.returncode != 0:
        return [f"git status failed: {result.stderr.strip()}"]
    return [line for line in result.stdout.splitlines() if line.strip()]


def build_snapshot(
    root: Path, today: date, now: datetime, timezone: str
) -> dict:
    data_quality: list[str] = []
    return {
        "today": {
            "date": today.isoformat(),
            "now": now.strftime("%Y-%m-%d %H:%M %Z"),
            "timezone": timezone,
        },
        "git_status_short": git_status_short(root),
        "leetcode": build_leetcode_snapshot(root, today, data_quality),
        "data_quality": data_quality,
    }


def local_now() -> datetime:
    """Return a timezone-aware datetime using the runtime's local timezone."""
    return datetime.now().astimezone()


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--root",
        default=".",
        help="Repository root to scan. Defaults to the current directory.",
    )
    parser.add_argument(
        "--date",
        help="Override today's date in YYYY-MM-DD format. Defaults to local date.",
    )
    parser.add_argument(
        "--compact",
        action="store_true",
        help="Emit compact JSON instead of pretty-printed JSON.",
    )
    args = parser.parse_args()

    root = Path(args.root).resolve()
    now = local_now()
    if args.date:
        today = parse_iso_date(args.date)
        if today is None:
            print(
                f"invalid --date {args.date!r}; expected YYYY-MM-DD",
                file=sys.stderr,
            )
            return 2
    else:
        today = now.date()

    timezone = str(now.tzinfo or now.tzname() or "local")
    snapshot = build_snapshot(root, today, now, timezone)
    if args.compact:
        print(json.dumps(snapshot, separators=(",", ":")))
    else:
        print(json.dumps(snapshot, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
