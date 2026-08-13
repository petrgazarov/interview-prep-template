# LeetCode Grading Calibration

## Contents

- [Research before ambiguous grading](#research-before-ambiguous-grading)
- [Asymptotic optimality](#asymptotic-optimality)
- [Shared numeric anchors](#shared-numeric-anchors)
- [Walkthrough and delivery anchors](#walkthrough-and-delivery-anchors)
- [Implementation-validation anchors](#implementation-validation-anchors)
- [Coding-round outcome anchors](#coding-round-outcome-anchors)
- [Regrade stability](#regrade-stability)

## Research Before Ambiguous Grading

Before assigning, communicating, or persisting an evaluation, research likely
tier-1 interviewer treatment when the evidence plausibly supports adjacent
anchors or depends materially on company or format expectations.

Use the most relevant available evidence:

1. Start with official company interview guidance, official problem/editorial
   material, or other primary sources relevant to the disputed criterion.
2. Add credible direct-interviewer guidance, interview-platform data, or
   comparable real-interview evidence when official guidance does not resolve
   the boundary. Use at least two independent credible sources when available.
3. Calibrate to the target company tier, role seniority, interview format, and
   exact attempt evidence rather than treating source count as a vote.
4. Cite the research in the feedback and state the inference connecting it to
   the final decision. If strong evidence is sparse or conflicting, say so.
5. Make the best evidence-weighted decision only after research. If adjacent
   anchors remain equally plausible, choose the more conservative one and
   explain why.

## Asymptotic Optimality

Use `asymptotic_optimality` to predict how the algorithm choice would affect a
high-bar tier-1 coding round, not as a purely theoretical ranking.

Evaluate the prompt, constraints, time, auxiliary space, and hidden runtime
costs against the solution target a high-bar interviewer would reasonably
expect live. `acceptable_tradeoff` means the remaining stricter improvement is
normally optional.

Ground claims that an approach is standard, expected, or optional in the
prompt constraints and authoritative solution or interviewer evidence. An
officially recognized approach establishes canonicity, while interview
expectations may still require separate evidence.

### Required calibration research

Whenever a correct solution is strictly suboptimal and the decision could be
`acceptable_tradeoff` or `minor_gap`, research likely real-interviewer
treatment before grading or persisting the label, even for a familiar problem:

1. Inspect the exact constraints and the official editorial or problem-author
   reference when available.
2. Inspect at least two independent, credible interview-oriented sources that
   discuss or implement the expected approach and complexity. If no official
   source is available, use at least three independent credible sources. Do
   not count mirrors, copied explanations, or unsourced solution dumps as
   independent evidence.
3. When the company, role, or interview format is known, search for direct
   interviewer guidance or credible reports from comparable real interviews.
4. Weigh evidence by authority and relevance rather than treating source count
   as a vote. Distinguish recognized solution, common teaching solution,
   expected interview target, and optional follow-up.
5. Cite the sources in the feedback and state the inference connecting them to
   likely interviewer signal. Record a concise calibration rationale in
   `notes` when the label is non-obvious, contested, or changes a prior grade.
6. If good-faith research remains sparse, inaccessible, or conflicting, state
   that limitation and make the best evidence-weighted judgment. Best judgment
   is the fallback after research, not a substitute for it; `unclear` is not a
   shortcut around the research requirement.

### Labels

- `optimal`: meets the strongest time and auxiliary-space target a reasonable
  interviewer would expect for the prompt.
- `acceptable_tradeoff`: fully meets the expected interview bar although a
  stricter asymptotic improvement exists that a reasonable interviewer would
  normally treat as optional, or the chosen tradeoff is justified. Its absence
  is not negative interview evidence and it may support `strong_pass`.
- `minor_gap`: misses a modest improvement a reasonable interviewer would
  likely expect or probe as a natural follow-up while retaining the main
  scalable model. The missed improvement is negative interview evidence.
- `material_gap`: misses a standard target by a meaningful asymptotic factor,
  such as quadratic rather than linear work, while remaining correct for the
  stated constraints.
- `major_gap`: is fundamentally non-scalable for the prompt, such as
  exponential enumeration where a polynomial target is expected, or fails the
  constraint scale/TLE.
- `unclear`: the attempt's code or expected target is not sufficiently
  evidenced.

### Grade and outcome effects

- An independently reached `optimal` target can support `A` and
  `strong_pass`/`pass`, subject to the other dimensions.
- `acceptable_tradeoff` creates no automatic ceiling.
- A `minor_gap` at the attempt boundary normally caps the practice grade at
  `B` and tends toward `pass` or `borderline`, depending on whether the
  optimization is a prominent expected follow-up.
- A correct `material_gap` at the boundary defaults to `C` and `borderline`.
- A `major_gap` at the boundary, TLE, or absence of a scalable model normally
  yields `C`/`D` and `fail`.
- Reaching the target immediately after a neutral optimization probe warrants
  at most a small completeness penalty. Requiring a directional hint, repeated
  prompting, or substantial late repair usually moves the result into `B`/`C`
  and `pass`/`borderline` according to the intervention and total timing.

Require same-day targeted practice of the expected target for every
`minor_gap`, `material_gap`, or `major_gap`, and review the corrected solution.
This is not a new CSV attempt unless the user performs another actual timed
rep. Continue to use the redo ROI policy for later cold retention.
`acceptable_tradeoff` does not trigger mandatory same-day optimization.

## Shared Numeric Anchors

Use tier-1 calibration on every attempt. Apply these anchors to every numeric
dimension:

- `10`: no interview-relevant improvement is identifiable. An equally valid
  stylistic alternative or negligible micro-optimization does not block `10`.
- `9`: fully interview-ready; only a specific, objectively beneficial cosmetic
  or optional improvement remains.
- `8`: one concrete, nonfatal quality or clarity issue remains, with a
  plausible negative effect on interviewer understanding, confidence, or
  evaluation.
- `7`: fundamentally correct, but the nonfatal gap is more pronounced.
- `5-6`: the core idea is present, but the artifact is materially incomplete,
  brittle, inaccurate in one important place, or too verbose for a strong
  interview signal.
- `3-4`: a major error, mistrace, or communication defect makes interviewer
  intervention likely.
- `0-2`: absent, mostly wrong, or unusable.

## Walkthrough and Delivery Anchors

Treat a representative walkthrough as a selective but code-faithful trace,
not a high-level restatement. Require the relevant input/index values,
condition outcome, state mutations, output update, and ending state. Allow the
trace to begin from a clearly stated intermediate state when that isolates the
important transition. The ending state may be established incrementally; a
separate recital of the final output is optional when it is already
unambiguous. Compress repeated no-op iterations, and do not require a full-
array trace unless requested or every iteration tests distinct behavior. One
brief repeated correct transition is at most cosmetic unless it materially
lengthens or obscures the walkthrough.

Score spoken organization/concision from structure and proportionality as well
as duration. Use timing only as rough calibration: a short targeted transition
may take about 60-90 seconds, while a code-faithful walkthrough of a
six-to-eight-element official example may reasonably take about 2-3 minutes. A
roughly 10-minute exhaustive trace of a common-medium example normally belongs
in the `3-4` range when the same evidence could be delivered in a focused 2-3
minute walkthrough.

## Implementation-Validation Anchors

- `passed`: candidate-owned audit or walkthrough establishes before sign-off
  that the final implementation satisfies the prompt and intended algorithm.
  This includes independently detecting and repairing a defect before
  sign-off—even a material requirement, plan, or algorithm defect—when the
  candidate then revalidates the final implementation without human
  intervention.
- `partial`: permitted execution reveals a localized non-algorithmic defect
  that survived the intended audit; the candidate diagnoses, fixes, and
  revalidates it independently and quickly.
- `failed`: a material defect survives the intended unaided audit/walkthrough
  and is exposed only by execution, survives sign-off, requires
  interviewer/hint intervention to repair, or leaves a repaired final
  implementation that is not revalidated well enough to be trustworthy.
  Repeated localized defects or ad hoc debugging may also fail this component
  when they leave the final validation untrustworthy.

This component captures validation effectiveness. Planning, problem-solving,
pacing, grade, and round outcome capture the cost of reaching the final model.
A localized syntax, name, receiver, API, or return-variable defect found by
permitted execution and repaired independently within moments normally maps to
`partial`, an otherwise `B`-range attempt, and `pass`. In a no-execution format,
evaluate the code at declaration and weigh an obvious typo by its impact and
normal review repairability.

## Coding-Round Outcome Anchors

- `strong_pass`: independently reaches and validates the expected solution
  comfortably, with clear communication and no material concern.
- `pass`: likely advances; the solution is independently correct and complete,
  with only minor nonmaterial pacing, clarity, or code-quality issues.
- `borderline`: mixed/interviewer-dependent; substantial signal is present,
  but pacing, communication, or an independently self-repaired material defect
  creates meaningful doubt. Use this only when correctness did not require
  human intervention and the completed solution still fits the round.
- `fail`: most likely does not advance because the solution is incorrect or
  incomplete, material correctness requires human intervention, or repair is
  extensive enough to consume the round or substantially rebuild the core
  solution without a trustworthy finish.

Derive outcome from the target format, defect severity, repair independence,
final state, and total interview time; keep it independent from A-D grade and
implementation-validation label.

## Regrade Stability

Distinguish a contemporaneous review correction from a genuinely later regrade:

- During the immediate post-attempt review, keep the row provisional until its
  evidence, grading, and follow-up are settled, then write the final canonical
  state. Correct any previously communicated value explicitly.
- For a genuinely later correction to a settled record, apply the
  attempt-boundary rule and change an evaluative field only for new evidence,
  a factual correction, a policy change, or a prior grading error. Report each
  changed value as `old -> new` and its cause. Preserve amendment history in
  `notes` only when it is material to interpreting the record.
