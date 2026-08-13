---
name: today
description: Build or refresh today's LeetCode practice docket from the current attempt log. Use for "$today", "/today", "what is due today", "what should I practice today", mid-day docket refreshes, completed-today summaries, or due-redo scans.
---

# Today

## Purpose

Create a concise current-day DSA docket from live repository data. Each run
must reflect the latest completed attempts, due work, and follow-up state. Do
not store day-specific plans.

## Data To Gather

- Run `make today_snapshot` for the runtime-local date/time, repository status,
  completed-today attempts, and due-redo state.
- Read `AGENTS.md` for durable strategy and learning boundaries.
- Treat `leetcode_attempts.csv` as the canonical attempt and follow-up state.
- Read detailed rows only for internal prioritization. Never use them to expand
  a pre-attempt public assignment contract.

## Workflow

1. Run `make today_snapshot` from the repository root. If it fails or appears
   stale, parse `leetcode_attempts.csv` with a real CSV parser, run
   `git status --short`, and obtain the runtime-local date with `date`.
2. Scan current strategy from `AGENTS.md`; keep this skill as the owner of the
   current-day procedure.
3. Scan attempts and redos:
   - Group attempts by canonical `url`. Never fall back to problem title when a
     row lacks a URL; report the data-quality gap and run
     `make validate_leetcode_attempts`.
   - Explicitly inspect attempts logged on today's local date before
     recommending remaining work.
   - Report completed attempts first: count and broad split by `attempt_type`.
     Do not report logged minutes.
   - If a completed attempt currently has another active redo, acknowledge the
     activity without identifying the problem or exposing its date, result,
     grade, or other protected metadata.
   - Treat the latest row for each URL as current state.
   - A redo is due when that latest row has a valid `redo_due` on or before
     today. Include overdue work and sort by `redo_due`, then `problem`.
   - Apply the pre-attempt allowlist in `AGENTS.md`. Never render difficulty,
     prior dates, grades, results, times, diagnostic labels, scheduling
     rationale, topic/pattern metadata, or solution content.
   - Treat `docket_note` as the authoritative public assignment contract.
     Render it faithfully and do not synthesize additions from internal fields.
   - For each due redo, report only problem, due status/date, and `docket_note`.
   - If a due redo lacks a valid, actionable `docket_note`, report the
     data-quality gap and do not recommend starting it until
     `$record-leetcode-attempt` supplies a valid contract.
   - After the user completes and shares the redo, its post-attempt review may
     compare it with prior attempts.
   - Older rows are history. Do not infer hidden future redos from them.
   - Use latest-row `transfer_skill` and `adjacent_drills` only internally to
     bias new-problem selection. They are not due work.
4. Recommend remaining work:
   - List due redo commitments, then recommend continuing the user's chosen
     external problem list. This repository owns no queue; never claim an
     external-list problem is canonical unless the user supplied the sequence.
   - When both are present, generally preserve the user's best focus for unseen
     work and fit due redos or review around it, unless targeted repair or a mock
     is the day's main priority.
   - Include same-day correction, review, transfer practice, or a mock when
     current evidence makes it the highest-value next step.
   - Treat CSV `time_min` as attempt evidence, not a complete study-time
     ledger. Never subtract it from an assumed daily target or infer remaining
     study capacity from it.
   - If the user supplies availability or a focus, fit the docket to it. If
     not, give a priority order without inventing hours, timed blocks, or a
     problem-count quota.
5. Return the docket without editing any logs or strategy files.

## Output Shape

Keep the answer concise and decision-oriented:

```text
Today is YYYY-MM-DD (local time).

Completed today:
- ...

Due redos:
- Problem — due/overdue YYYY-MM-DD
  Contract: exact docket_note

Next priority:
- Continue the chosen external list, or name the higher-value repair/mock.

Recommended order: ...
```

If there are no completed attempts or due redos, say so explicitly. Before
returning a docket with redos, verify every `docket_note` is actionable under
the contract owned by `$record-leetcode-attempt`.

## Boundaries

- Do not duplicate this procedure in `AGENTS.md`.
- Do not silently update logs from a docket scan.
- Do not disclose internal attempt evidence before a scheduled redo.
- Adjust to user-supplied time or focus without inventing missing context.
