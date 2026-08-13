# Interview Prep Template

LeetCode and DSA practice with AI.

Use your favorite harness to grade every attempt, track redos, and build a
history you can analyze to find your remaining gaps.

This repo does not provide a problem list. Choose problems from any source, then
use this repo to record and learn from your attempts. Create your own repository
from this GitHub template, then customize the instructions and skills as your
study process evolves.

## Use it

- Codex: `$today` and `$record-leetcode-attempt`
- Claude Code: `/today` and `/record-leetcode-attempt`

### `$today`

Run it at the start of the day or mid-day to see completed attempts, due redos,
and what to do next.

### `$record-leetcode-attempt`

After an attempt, share as much factual context as possible. For example:

````text
Did a new problem. Time 31:10. No hints used. When I ran the first solution
against the example cases, some tests failed. I fixed the code using a different
approach (BFS), and the submission succeeded.

Problem:
[Problem URL]
[Problem statement with examples and constraints copy-pasted from LeetCode]

Timeline:
- 02:45 Finished pre-code plan; started implementation
- 14:20 Finished code; started spoken walkthrough
- 19:10 Finished walkthrough; started complexity
- 20:05 Finished complexity; started correctness argument
- 22:30 Finished correctness argument; example tests failed; debugging
- 31:10 Fixed code; submitted successfully

First solution (wrong):
[My first solution, including pre-code plan comments]

Final solution (correct):
[My final solution]

Spoken portion:
[one continuous transcript of my example walkthrough, complexity analysis,
and correctness argument]
````

More context produces better grading and follow-up decisions.

### Hints during an attempt

Ask the AI for a hint without ending the attempt. It gives one small nudge and
stops; ask again to move one step closer to the solution. Keep the timer
running—the hints and their timing are recorded and affect grading.

## Recommended loop

1. Start one timer and type a pre-code plan.
2. Implement the solution.
3. Speak through an example, complexity, and a correctness argument (ChatGPT is
   great for transcribing this).
4. Test or submit while keeping the timer running through any fixes.
5. Share everything with `$record-leetcode-attempt`.

The agent grades the attempt, updates `leetcode_attempts.csv`, and schedules
useful follow-up. Later, ask it to analyze your history for recurring gaps in
topics, planning, correctness, implementation, complexity, or communication.

## Scoring rubric

The scoring rubric is intentionally opinionated. It tries to reproduce the
timing, independence, correctness, optimization, and communication bar of a
real tier-1 DSA interview—not merely whether LeetCode accepted the code.

A complete scorecard might look like:

```text
Practice grade: B — overall mastery across the whole attempt
Pre-code plan: 8/10 — implementation readiness before coding
Correctness argument:
  Technical content: 8/10 — correctness and completeness
  Spoken delivery: 9/10 — organization and concision
  Combined: 8/10 — overall correctness explanation
Walkthrough: 9/10 — accurate, code-faithful example trace
Code quality: 9/10 — clarity, safety, and idiomatic implementation
Implementation validation: partial — execution exposed one localized bug
Complexity analysis: correct — stated bounds match the code
Asymptotic optimality: optimal — meets the expected interview target
Likely tier-1 round outcome: pass — likely to advance in this round
```

For numeric scores, `10` means no interview-relevant improvement, `9` means
optional polish, and `8` means a concrete but nonfatal issue. The practice
grade and predicted round outcome are separate judgments, not score averages.

## Requirements

Python 3.10+; standard library only. Run `make help` for commands and
`make validate` for checks.
