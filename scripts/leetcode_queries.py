#!/usr/bin/env python3
"""Read-only queries over the LeetCode attempt log."""

from __future__ import annotations

import argparse
import csv
import json
import sys
from collections import Counter
from pathlib import Path


DEFAULT_PATH = Path("leetcode_attempts.csv")
ACTIVE_REDO_FIELDS = [
    "problem",
    "url",
    "difficulty",
    "redo_due",
    "docket_note",
]


def canonical_url(value: str) -> str:
    """Normalize the harmless URL variation used when grouping attempts."""
    return value.strip().rstrip("/")


def read_attempts(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8-sig") as f:
        reader = csv.DictReader(f)
        if not reader.fieldnames:
            raise ValueError(f"{path}: missing CSV header")

        rows: list[dict[str, str]] = []
        for row_number, row in enumerate(reader, start=2):
            extra = row.pop(None, None)
            if extra:
                raise ValueError(
                    f"{path}: line {row_number}: extra columns: {extra}"
                )
            rows.append({key: value or "" for key, value in row.items()})
        return rows


def attempt_history(rows: list[dict[str, str]], url: str) -> dict:
    target = canonical_url(url)
    if not target:
        raise ValueError("URL must not be empty")

    attempts = [
        row
        for row in rows
        if canonical_url(row.get("url", "")) == target
    ]
    return {
        "url": target,
        "attempt_count": len(attempts),
        "attempts": attempts,
    }


def recent_attempts(rows: list[dict[str, str]], limit: int) -> dict:
    if limit < 1:
        raise ValueError("LIMIT must be a positive integer")

    attempts = list(reversed(rows[-limit:]))
    return {
        "limit": limit,
        "attempt_count": len(attempts),
        "order": "newest_first",
        "attempts": attempts,
    }


def active_redos(rows: list[dict[str, str]]) -> dict:
    latest_by_url: dict[str, dict[str, str]] = {}
    for row in rows:
        url = canonical_url(row.get("url", ""))
        if url:
            latest_by_url[url] = row

    commitments = [
        {field: row.get(field, "") for field in ACTIVE_REDO_FIELDS}
        for row in latest_by_url.values()
        if row.get("redo_due", "").strip()
    ]
    commitments.sort(key=lambda row: (row["redo_due"], row["problem"]))
    capacity_by_date = Counter(row["redo_due"] for row in commitments)

    return {
        "active_redo_count": len(commitments),
        "capacity_by_date": dict(sorted(capacity_by_date.items())),
        "commitments": commitments,
    }


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--path",
        type=Path,
        default=DEFAULT_PATH,
        help="Path to leetcode_attempts.csv",
    )
    subparsers = parser.add_subparsers(dest="command", required=True)

    history = subparsers.add_parser("history", help="Show every attempt for a URL")
    history.add_argument("--url", required=True, help="Canonical problem URL")

    recent = subparsers.add_parser("recent", help="Show the most recent attempt rows")
    recent.add_argument("--limit", type=int, default=10)

    subparsers.add_parser(
        "active-redos",
        help="Show latest active redo commitments and per-date capacity",
    )
    return parser


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()
    try:
        rows = read_attempts(args.path)
        if args.command == "history":
            payload = attempt_history(rows, args.url)
        elif args.command == "recent":
            payload = recent_attempts(rows, args.limit)
        else:
            payload = active_redos(rows)
    except (OSError, ValueError) as exc:
        parser.error(str(exc))

    json.dump(payload, sys.stdout, indent=2)
    sys.stdout.write("\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
