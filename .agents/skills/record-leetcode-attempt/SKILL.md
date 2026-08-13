---
name: record-leetcode-attempt
description: Review, grade, record, schedule follow-up, and provide progressively disclosed hints for LeetCode-style coding practice. Use for first passes, redos, mocks, failed attempts, hint requests, optimization feedback, attempt-history questions, or requests for the logging format.
---

# Record LeetCode Attempt

## Purpose And Invariants

Record complete LeetCode-style coding reps in `leetcode_attempts.csv`, review
their evidence, and choose the highest-value follow-up.

- Append one row per actual rep; scheduling and later evidence update the latest
  existing row for that URL.
- `url` is the canonical problem identity.
- `redo_due` is a binary commitment to a same-problem redo. Blank `redo_due` means there is no same-problem redo.
- `docket_note` is the prospective public assignment contract that `$today`
  may show before the next attempt; it contains no prior-performance or
  scheduling rationale.
- `transfer_skill` and `adjacent_drills` guide new-problem selection when
  `redo_due` is blank.
- Older rows remain audit history. The latest row for a URL controls active follow-up state because `$today` groups by latest row.
- The active schedule contains at most one latest-row redo commitment per date.
- For pre-attempt interactions, apply the allowlist in `AGENTS.md`; only the
  public assignment contract is externally visible.
- In the review interaction immediately following a completed and shared attempt,
  provide the full grading evidence and prior-attempt comparison before the
  next scheduled rep returns to pre-attempt status.

## Request Routing

- For a new actual rep, use the full evidence, grading, write, validation, and
  follow-up workflow below.
- For later evidence, a factual correction, or a follow-up-state decision,
  update the existing row under Attempt Boundary And Later Repair.
- For attempt-history questions, general optimization feedback, or process
  discussion, answer from the relevant evidence. Write only when the user
  reports new attempt evidence or authorizes a durable follow-up-state change.
- Before giving an active-attempt hint, read and follow [`references/hint-escalation.md`](references/hint-escalation.md) completely.

### Attempt Boundary And Later Repair

Scope every evaluative field to evidence produced within the logged attempt's
recorded time and sign-off boundary. This applies to `result`, `grade`,
`what_went_wrong`, all numeric scorecard fields, `implementation_validation`,
`complexity_analysis`, `tier1_interview_outcome`, and `asymptotic_optimality`.
Corrections completed before that boundary are part of the attempt; later
same-day or post-attempt repairs, accepted implementations, editorial study,
and follow-up practice are not.

Record later improvement in `notes` and update mutable follow-up state such as
`redo_due`, `redo_target`, `docket_note`, `transfer_skill`, or
`adjacent_drills` when appropriate. Regrade an evaluative field only when new
evidence clarifies the original attempt, a factual or policy correction
applies, or the prior grade was erroneous.

Treat the immediate post-attempt review as one finalization transaction. If
facts, grading, or follow-up decisions change while that review is still being
resolved, rewrite the row to its final canonical state and keep `notes` focused
on settled evidence and follow-up state. Apply the grading reference's Regrade
Stability policy to later changes.

## Attempt Evidence

Collect this evidence before editing the CSV:

- identity: local `date`, exact `problem`, canonical `url`, `difficulty`, and
  `attempt_type` (`first_pass`, `redo`, or `mock`), plus the full problem
  statement and constraints for grading context;
- outcome at the attempt boundary: `solved`, `partial`, or `failed`; whether
  hints were used; any solution/editorial use reported under the
  Missing-Input Audit convention below; whether the code was
  accepted/correct; and the code at sign-off and at the end of the attempt
  when different;
- validation context: whether execution was available, how each defect was
  detected, who localized and fixed it, repair time, and whether the algorithm
  changed;
- the `implementation_ready_time` lap and `total_time_after_spoken_wrap`, both
  in `MM:SS`;
- the pre-code plan and the user's post-code correctness argument;
- the automatic transcript of the timed representative dry run, time/space
  analysis, and correctness argument.
  A second example is required only when it tests a materially different case.

For an older attempt logged later, use only the evidence required by the
protocol active on its original date. Store its original active time under the
prior convention in decimal `time_min`; do not invent laps, transcripts, or
other missing historical evidence.

Derive `topic`, all grading fields, and follow-up fields from the evidence. Do
not ask the user to classify their own performance or supply scheduling
wording.

### Timed Spoken-Wrap Protocol

Use one continuous interview clock:

1. Take the `implementation_ready_time` lap when the implementation is ready for validation; this is not the completed-problem time.
2. Keep the clock running while the user walks through at least one representative example, states time/space complexity, gives the correctness argument, and fixes anything the spoken review exposes.
3. Stop at `total_time_after_spoken_wrap`.
4. Use the automatic transcript of the timed speech and exclude
   transcription-processing delay from the interview total.

Persist the timing according to CSV Writing below. Grade using the total interview-style time while using the implementation lap to diagnose whether coding or communication caused the slowdown.

### Bug Detection And Interview-Format Convention

- Determine whether the target format allows code execution from the user's
  report, recruiter guidance, or known company format. When unknown, grade the
  actual practice flow and state material format sensitivity.
- In an execution-enabled format, candidate-initiated tests and their output
  are candidate-owned validation. Sign-off occurs at an explicit declaration
  of completion, final submission, final walkthrough, or end of active
  debugging unless the format defines another boundary.
- Separate the detection channel from defect severity. Record whether the defect was caught by unaided audit/walkthrough, candidate-initiated execution, or interviewer/hint intervention; whether the candidate localized and fixed it independently; repair time; and whether the core algorithm changed. Tool output alone is not interviewer intervention.
- Apply the grading reference's implementation-validation and round-outcome
  anchors. In a no-execution format, evaluate the code at declaration.
- Keep `result=solved` when code corrected within the logged attempt actually solved the platform problem. The result, practice grade, implementation-validation field, and interview-outcome field intentionally answer different questions.

### Derived CSV Fields

Conditionally required:

- `what_went_wrong`: concise failure mode or slowdown. Leave blank only for a
  clean solved `A` attempt with no scheduled redo.
- `redo_target`: concrete performance/correctness bar for the next same-problem redo. Required whenever `redo_due` is set; otherwise leave blank.
- `docket_note`: agent-authored prospective assignment contract safe to show before the scheduled redo. Required whenever `redo_due` is set; otherwise leave blank.

Optional follow-up/context fields:

- `transfer_skill`: underlying skill or concept the attempt exposed.
- `adjacent_drills`: similar-but-not-identical drill family or problem types to practice.
- `notes`: short narrative context or takeaway. Do not put parseable follow-up labels here; use dedicated fields for follow-up state.

### Docket Note Contract

Apply the pre-attempt allowlist in `AGENTS.md` with low discretion:

- For an ordinary full redo, use the form: `Cold same-problem redo without
  hints or external references; finish within X minutes under the standard
  attempt protocol.` Omit the time clause when no specific cap is assigned.
- For a deliberately staged follow-up or alternate rep, add only the minimum
  constraint needed to distinguish it from an ordinary repeat and say that the
  exact approach is intentionally withheld. Do not mention prior performance,
  diagnoses, mistakes, or scheduling rationale.
- Keep the note within the `AGENTS.md` allowlist. The standard protocol already
  covers uniform correctness, walkthrough, validation, complexity, and
  communication requirements; include one only when it defines a staged
  assignment. Schedule the redo only with an actionable compliant note.

### Missing-Input Audit

Before asking a follow-up or editing the CSV, do a strict input audit:

- Count evidence already supplied in prose, problem metadata, code comments, or
  an unambiguous outcome statement; never ask for it again.
- In this repository, unreported solution/editorial use means none before the
  attempt boundary. An explicit give-up closes that boundary; subsequent
  solution/editorial study is post-attempt exposure. Record reported exposure
  and clarify its timing only when that would materially affect evaluation or
  follow-up.
- Outcome and grading facts may come from code/result context. Explanation
  inputs must come from the user's own interview-style explanation; do not
  infer complexity, correctness reasoning, or example coverage from code.
- Code comments may satisfy the pre-code plan when they state the planned
  approach and correctness strategy. They do not replace a required timed
  spoken transcript or the separate post-code correctness argument.
- Under the spoken-wrap protocol, require both stopwatch marks and a transcript
  covering correctness, one representative example, and both complexities. If
  the user forgot the wrap, they may time it separately and add its duration to
  the implementation lap; exclude the break and transcription delay.
- Ask only for evidence that remains missing; derive classifications, scores,
  and follow-up wording from the evidence.

## Grading Calibration Reference

Before grading, regrading, predicting a coding-round outcome, or answering
algorithm-optimality feedback, read
[`references/grading-calibration.md`](references/grading-calibration.md)
completely. It owns the asymptotic labels and research requirements, numeric
anchors, implementation-validation anchors, outcome anchors, and regrade
stability rules.

### Mandatory Pre-Write Grading Audit

Draft from the evidence, then challenge each judgment against its anchor before
communicating or persisting it.

1. Convert the Attempt Evidence into a fact ledger. Preserve exact timing and
   section boundaries, and explicitly separate code at sign-off, the final code
   reached within the attempt, and any later repair.
2. Verify timing arithmetic and score each dimension only from its named
   artifact. Do not import proof requirements into the plan score, presentation
   polish into technical-content scores, or timing into code quality.
3. For every numeric score, write one evidence sentence. For every score below
   `10`, identify the dimension-specific improvement and classify it under the
   shared numeric anchors. An equally valid stylistic alternative is not an
   improvement and supports no deduction; optional but objectively beneficial
   polish may support `9`; `8` or below requires a concrete issue with a
   plausible negative interview consequence. If the rationale cannot state
   that consequence for `8` or below, raise the score.
4. Apply the grading reference consistently and complete its ambiguity research
   whenever adjacent anchors remain plausibly supported.
5. Check that timing matches the ledger; no shortcoming is double-counted
   across dimensions without a separate effect in each; code quality,
   validation, complexity analysis, optimality, A-D grade, and round outcome
   remain independent; and hypothetical follow-up answers receive no credit.
6. Resolve any material missing fact with the smallest targeted question before
   writing the row.

## Review And Grading

Apply these evidence conventions:

- Treat the automatic transcript as unrehearsed speech, not polished prose.
  Ignore transcription artifacts and harmless fragments or self-corrections;
  judge actual structure, precision, proportionality, and filler.
- Require the central correctness mechanism and enough invariant/control-flow
  detail to trust the code, not a proof-complete monologue. Distinguish a
  planning/model gap from a delivery gap.
- Lead feedback with the exact missing or incorrect mechanism before offering
  improved wording. Tie criticism to the user's phrase, omitted state, or code
  mismatch.
- Within the attempt boundary, an immediate correct answer to a neutral probe
  is successful collaboration with at most a small completeness penalty;
  directional help, repeated prompting, or a still-wrong answer carries more
  weight. Post-attempt answers are later repair under Attempt Boundary And
  Later Repair.
- Verify stated complexity against the attempt's code, including amortization
  and hidden runtime costs such as copying, sorting, materialization, and
  recursion depth.
- Default an unqualified space answer to auxiliary space. Accept a clear
  auxiliary or output-inclusive convention; for non-scalar output, the
  strongest answer states both. Count separate working storage even if it later
  becomes the return value.
- Accept a valid standard editorial upper bound even when a tighter
  output-sensitive form exists. Penalize false bounds and category errors such
  as equating total recursive calls with live stack depth.
- Independently compare actual time and auxiliary space with the expected
  tier-1 target even when the code is accepted and the user's analysis is
  correct.

### Required Component Scorecard

For every graded attempt, include this diagnostic breakdown in the final
response:

```text
Pre-code plan: N/10
Correctness argument:
  - Technical content: N/10
  - Spoken organization/concision: N/10
  - Combined correctness-argument score: N/10
Representative example/walkthrough: N/10
Code quality: N/10
Implementation validation: passed | partial | failed
Complexity analysis: correct | partial | incorrect
Asymptotic optimality: optimal | acceptable_tradeoff | minor_gap | material_gap | major_gap | unclear
Likely tier-1 coding-round outcome: strong_pass | pass | borderline | fail
```

Give one concise evidence sentence for every component.
Keep the dimensions separate:

- Score the pre-code plan from the plan stated before coding. Judge whether it
  is implementation-ready through its approach, necessary state/data
  structure, transition or invariant, and processing order. Do not require the
  formal correctness proof in the plan; that belongs to correctness content.
  Practice-only plan comments are plan evidence and must not reduce code
  quality; treat them as code documentation only when the user intended them
  to remain.
- Score the correctness argument from the reasoning expressed in that section:
  correctness, completeness, state/control-flow specificity, organization, and
  spoken concision. Always report its three-part breakdown: technical content,
  spoken organization/concision, and a holistic combined score. Ignore
  transcription artifacts and keep walkthrough or code-divergence evidence in
  their own dimensions.
- Score the representative example on whether it exercises a meaningful
  transition and accurately traces the attempt's code. An ending state may be
  established incrementally; do not require a redundant final-output recital.
  One brief repeated correct transition is at most optional concision polish
  unless it materially lengthens or obscures the trace.
- Score code quality on whether the implementation is minimal, idiomatic, and
  easy to reason about, using the final implementation reached within the
  attempt. Exclude practice-only planning comments. Do not deduct for an
  equivalent expression, personal style preference, or irrelevant constant-
  factor micro-optimization; identify an objective readability, safety,
  maintainability, or idiomaticity benefit before treating an alternative as
  better. A defect affects this score only when the surrounding design is
  itself brittle, obscure, or unnecessarily complicated.
- Use overall attempt timing for the A-D grade and predicted round outcome.
  Use a section's duration inside a numeric component only where that
  component expressly includes proportionality or concision, and never as the
  sole basis for a deduction.
- Grade implementation validation with the grading reference's canonical
  anchors.
- Grade complexity analysis by comparing the user's stated bounds with the
  attempt's code, including hidden allocations and language/runtime behavior.
- Grade asymptotic optimality separately from complexity-analysis correctness.
  State the attempt's and expected time/space bounds in the evidence sentence;
  a candidate may accurately describe a suboptimal algorithm.
- Predict only this coding round's outcome and include one concise reason.

The component scorecard is diagnostic and does not mechanically average into
the overall `A`-`D` attempt grade.

## Grading

The A-D grade is a practice/mastery signal. It is deliberately separate from
`tier1_interview_outcome`, which predicts whether the particular round would
advance.

- `A`: independently correct, clean, no hints, comfortably paced, and well validated.
- `B`: correct core model and completed solution with only nonmaterial pacing, clarity, code-quality, or internally repaired issues.
- `C`: the core model was independently obtained, but the attempt had a material implementation/validation or asymptotic gap, substantial hint dependence, major pacing or explanation weakness, or required a localized external correction.
- `D`: the core model was missing or mostly wrong, the full solution/editorial was required, the attempt was abandoned or remained substantially incomplete, or repair required major conceptual intervention.

### Tier-1 Timing Calibration

Use a tier-1 big-tech live-coding bar, not a generic LeetCode acceptance bar.

- Preserve the platform's official difficulty as problem metadata, but
  calibrate pacing and round outcome against the solution actually required:
  base prompt versus optimized follow-up, conceptual burden, first pass versus
  redo, and prior exact-problem exposure. Do not infer effective interview
  difficulty or a time bar from the official label alone.
- Correct accepted work with borderline pacing or a slow transition to the
  expected target normally falls in the `B` range. Include a same-problem
  expected optimization in the total; identify a materially separate follow-up
  in `notes`.
- A common-medium solution around 20-25 minutes is solid but earns `A` only
  when the expected target, validation, and spoken wrap are also clean.
- Grade pacing from `total_time_after_spoken_wrap`; use the implementation lap
  and wrap duration diagnostically rather than as independent penalties.
- Resolve an ambiguous `A`/`B` boundary through the grading reference; if it
  remains tied, choose `B` and explain the timing bar.

## Follow-up ROI And Redo Decision Policy

Choose a same-problem redo only through the ROI audit; grade determines spacing
after exact repetition wins.

Separate same-day correction from a scheduled full redo:

- Same-day correction may be a closed-book explanation, targeted code fix, or
  focused reimplementation. It becomes a new row only when the user performs a
  new actual rep.
- A scheduled `redo_due` is normally a full, cold same-problem solve.
- Count substantial correction, reimplementation, or solution study as
  same-problem exposure when spacing a redo.
- Space a full same-problem redo at least seven calendar days after the latest
  actual attempt or substantial same-problem exposure, except for a distinct
  staged follow-up.

### Mandatory Follow-up ROI Audit

Before setting `redo_due`, use first-principles reasoning rather than grade as a proxy:

1. Inspect same-URL history, meaningful exact-problem exposure, recent fresh reps of the implicated skill, and the active follow-up load.
2. Classify the failure and establish whether the corrected model is explainable closed-book. Ask for the minimum correction summary when needed.
3. Define the future capability the next rep should improve or measure. Compare an exact redo, an unseen near-transfer rep, a focused micro-drill, and no additional follow-up by expected transfer, solution-memory contamination, problem-specificity, diagnostic information, time cost, and the candidate's observed response to prior exact and transfer reps.
4. Research the exact-versus-transfer decision when relevant local evidence and first principles leave material ambiguity or when establishing a reusable policy. Prefer primary learning research and direct candidate evidence; state the inference rather than treating source count as a vote.
5. Schedule an exact redo only when it is the highest-ROI test of an unresolved gap. Otherwise use `transfer_skill` and/or `adjacent_drills` and leave exact-redo fields blank.
6. Record a concise decision rationale in `notes`. For a scheduled redo, author `redo_target` and `docket_note` under the contract above.

Specific rules:

- Before assigning or changing a nonblank `redo_due`, scan active commitments
  from the latest row for each URL, excluding the current problem's URL because
  the new row or edit supersedes it. If the intended date already has another
  redo, move the new or rescheduled redo forward by calendar day, including
  weekends, until the date is open. Existing commitments keep their dates.
- Apply these intervals only after the ROI audit selects an exact redo; use the
  repeat-backoff rules after the second actual attempt.
- `A`: leave `redo_due` blank unless a distinct staged same-problem follow-up remains.
- `B`: prefer adjacent transfer. Use a 10-14 day exact redo only for a concrete
  unresolved high-transfer issue or a staged follow-up.
- `C`: require same-day correction. Once the corrected model is explainable closed-book, run the ROI audit. If exact repetition wins, schedule it 7-10 days after the correction; otherwise prefer the selected transfer option.
- `D`: require same-day model repair. Once the corrected model is explainable closed-book, run the ROI audit. If exact repetition wins, schedule it 7-10 days after the repair; otherwise prefer the selected transfer option. If the model remains unclear, continue repair before choosing a later follow-up.
- Adjust timing by what the next redo is meant to test:
  - If the attempt failed because a previously seen model decayed over time but is now understood after review, schedule a cold retrieval redo 7-10 days out.
  - If the issue is an implementation contract or execution-hygiene bug, use
    the applicable grade interval only when it is repeated, problem-specific,
    or especially high-transfer; otherwise use adjacent reps.
  - If the issue is a weak correctness argument, deliver it aloud again the
    same day and review the automatic transcript; an untimed written rewrite is
    supporting study. Use an exact redo only when the weakness affected solving
    or reflects a shaky model.
- A materially different staged alternate implementation or follow-up may be
  scheduled sooner and is recorded as distinct exposure rather than cold
  retention evidence.
- After two actual attempts, use a third only for an unresolved
  problem-specific/high-transfer gap, a staged follow-up, or a still-materially
  unresolved second attempt; space it 14-21 days after the latest meaningful
  exposure.
- After three actual attempts, retire the exact problem. A fourth-or-later rep
  requires recurrence of the same material failure in fresh evidence, a staged
  follow-up, or an imminent interview; normally space it 28-42 days after the
  latest exposure.
- If the user reports that the exact code or traversal is still readily replayable from memory, extend the full-redo interval rather than treating a faster replay as durable retrieval.
- For staged alternate implementations, carry forward only active follow-up state into the latest row. Set `redo_due`, `transfer_skill`, `adjacent_drills`, and `redo_target` for the hidden target; use `docket_note` only to say that the next rep requires a different implementation and that the exact approach is withheld.

## CSV Writing

Rules:

- Treat the current `leetcode_attempts.csv` header as the canonical schema.
  Append one row per actual coding rep, preserve older rows, and update the
  latest row only under Attempt Boundary And Later Repair.
- Every newly appended row must populate all scorecard fields:
  - `plan_score`, `correctness_content_score`,
    `correctness_delivery_score`, `correctness_combined_score`,
    `walkthrough_score`, and `code_quality_score`: whole-number scores from `0`
    through `10`.
  - `implementation_validation`: `passed`, `partial`, or `failed`.
  - `complexity_analysis`: `correct`, `partial`, or `incorrect`.
  - `tier1_interview_outcome`: `strong_pass`, `pass`, `borderline`, or `fail`.
  - `asymptotic_optimality`: `optimal`, `acceptable_tradeoff`, `minor_gap`,
    `material_gap`, `major_gap`, or `unclear`.
- Backfill historical scorecard cells only on explicit request.
- Use valid CSV quoting when any field contains a comma, quote, or newline.
- Use blank optional fields for not-applicable data.
- Keep new `what_went_wrong`, `transfer_skill`, `adjacent_drills`,
  `redo_target`, `notes`, and `docket_note` content concise and scan-friendly;
  later factual or policy amendments may extend `notes` without rewriting the
  original attempt evidence.
- Treat `docket_note` as public pre-attempt text and enforce the Docket Note Contract above; keep `redo_target` and all diagnostic history internal.
- For attempts under the spoken-wrap protocol, store
  `total_time_after_spoken_wrap` in `time_min`. Include the exact
  implementation-ready lap, spoken-wrap duration, and total in `notes` using
  `MM:SS`. Store `time_min` as decimal minutes rounded to two decimal places.

## Workflow

Use this workflow for a new actual rep. For history, optimization, later
evidence, and follow-up-state requests, use Request Routing above.

1. Read the current CSV header, gather evidence, and run the missing-input
   audit.
2. For redo attempts, run `make leetcode_attempt_history URL=<canonical-url>`
   to read prior rows for the same `url`.
3. Build the fact ledger, complete the grading audit, and assign the scorecard,
   optimality, A-D grade, and round outcome.
4. Complete the follow-up ROI audit. For a nonblank `redo_due`, run
   `make leetcode_active_redos`, enforce the
   one-active-redo-per-date capacity rule, and move the new commitment forward
   until capacity exists.
5. Author `docket_note` when needed, write the row, and validate with
   `make validate_leetcode_attempts`.
6. Return proactive feedback using the Review And Grading rubric, with one
   evidence sentence for every score. Lead correctness-argument feedback with
   the specific gap before offering tighter spoken wording; say explicitly
   when the artifact is already strong.
7. For redo attempts, compare against previous attempts: time trend,
   grade/result trend, recurring vs fixed failure modes, and whether the
   attempt is improving, worse, or roughly flat.
8. Reply with the recorded grade, likely tier-1 coding-round outcome, redo
   date if any, and the reason for the schedule or no-redo decision.

## User Prompt Template

If the user asks what to provide, request this compact format:

```text
date: YYYY-MM-DD (omit if today)
problem and difficulty:
full problem statement and constraints:
url:
attempt_type: first_pass | redo | mock
implementation_ready_time: MM:SS
total_time_after_spoken_wrap: MM:SS
result: solved | partial | failed
hints_used: yes/no
solution_or_editorial_use: omit if none; otherwise before-give-up | post-give-up
accepted_or_correct: yes/no
execution_available: yes/no/unknown
timestamped timeline, including submissions, defects, and repairs:

- pre-code plan:
- code at sign-off:
- final code reached within the attempt, if different:
- complete automatic spoken-wrap transcript as one continuous text, covering a
  representative example/dry run, time and space complexity, the correctness
  argument, and a second materially distinct edge case when useful:
- later repair, if any, clearly labeled as post-attempt:
```
