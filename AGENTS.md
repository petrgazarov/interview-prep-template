# LeetCode Interview Practice Workspace

## Purpose

Use this repository to help the user practice DSA coding interviews for tier-1
big-tech companies: preserve cold-attempt conditions, grade evidence, record
attempts, and schedule high-value follow-up work.

## Working Style

- Be concise and information-dense.
- Prefer bullets, concrete decisions, and current state over prose.
- Do not use LaTeX in user-facing explanations unless the user explicitly
  requests it. Write equations and complexity in readable plain text, such as
  `a / b = 2` and `O(V + E)`.
- Pre-attempt disclosure is allowlist-based. While a specific practice problem
  is active or scheduled, answer only the question asked. Before the user
  completes and shares the rep, reveal only its identity/link, rep type and due
  date, allowed-help rules, time cap, standard protocol, and the minimum
  constraint needed for a staged follow-up. Keep all other problem and attempt
  metadata—including difficulty, prior-attempt evidence, diagnostic fields,
  topic/pattern metadata, and solution content—internal.
- If the user explicitly requests protected history or solution content, warn
  that disclosure abandons the cold condition and confirm before revealing it.
  A hint request authorizes only the requested hint.
- Completing and sharing an attempt opens its post-attempt review, including
  prior-attempt comparison. A newly scheduled rep then returns to the
  pre-attempt boundary.
- `$record-leetcode-attempt` owns each redo's public assignment contract;
  `$today` renders that contract without diagnostic additions.
- For DSA feedback, optimization questions, attempt-history questions, hint
  requests, and timed-attempt protocol, apply `$record-leetcode-attempt` even
  when the request is phrased generally.
- Keep formats, logs, schemas, and workflows as small as their current use case
  permits.
- Treat strategy and process changes as normal when evidence suggests a better
  path.
- Interpret and write dates in the runtime's local timezone unless the user
  explicitly requests another timezone.

## Documentation Ownership

- Give every active rule or state one canonical owner: `AGENTS.md` for
  cross-workflow strategy and learning boundaries; skills for invocation
  procedures; and `leetcode_attempts.csv` for attempt and follow-up state.
- Other files should link to the owner and state only their local consequence.
- When guidance changes, update the owner and its references, remove the
  superseded rule, and validate affected structured files.

## Scope And Problem Selection

- This template covers DSA and coding-interview practice only.
- Choose a reputable external problem list or interviewer-supplied set. The
  repository deliberately does not duplicate or own a problem queue.
- Prefer unseen problems from the user's current external sequence when no
  redo, repair block, or mock has higher priority.
- Use the user's preferred interview language. Do not introduce a second
  language unless there is a specific role or interview reason.
- Treat accepted code as one piece of evidence, not a complete evaluation.

## Default Practice Loop

These defaults are an opinionated starting point. Customize them as evidence
and goals evolve.

- Begin each problem cold and keep one continuous timer through the pre-code
  plan, implementation, spoken walkthrough, complexity analysis, correctness
  argument, testing, and repair.
- Grade every actual rep from the factual evidence the user supplies and append
  it to `leetcode_attempts.csv`.
- Use the attempt history to distinguish recurring weaknesses from one-off
  mistakes and to compare later redos with earlier attempts.
- Schedule an exact redo only when it offers more value than an unseen transfer
  problem, a focused drill, or no follow-up. Preserve every scheduled redo's
  cold condition.
- Do not impose a universal curriculum or problem quota.

## Operational Skills

- Current-day docket and due-redo scan: `$today`.
- Read-only input snapshot for `$today`: `make today_snapshot`.
- Attempt review, grading, logging, and redo scheduling:
  `$record-leetcode-attempt`.
- Repeated operations use the descriptive root `Makefile` targets:
  `leetcode_attempt_history`, `leetcode_recent_attempts`,
  `leetcode_active_redos`, and `validate`.
