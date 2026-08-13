# LeetCode Hint Escalation

Preserve as much candidate discovery as possible. A hint that is too small can
be followed by another; a hint that reveals the core model cannot be undone.

## Protocol

1. Give exactly one hint, then stop. Do not bundle later rungs, examples,
   pseudocode, adjacent advice, or an invitation containing extra direction.
2. Start with the smallest useful rung even when the candidate has been stuck
   for a long time. Elapsed time does not authorize a larger intervention.
3. If the candidate returns, advance by at most one rung and use their new
   reasoning to target the next obstacle. Do not repeat or rephrase a prior
   hint unless asked.
4. Jump farther only when the candidate explicitly requests a stronger hint,
   pseudocode, or the solution.
5. Record each hint's timestamp when known, rung, and exact conceptual content
   in the completed attempt. Do not append an incomplete attempt row.

## Rungs

1. **Diagnostic nudge:** Ask a focused question about a constraint,
   bottleneck, counterexample, or property their current approach must exploit.
   Do not identify the pattern, approach family, data structure, recurrence, or
   maintained state.
2. **Structural nudge:** Suggest a broad viewpoint such as processing order,
   prefix/suffix information, decomposing cases, or compressing partial
   candidates. Do not name the exact state, invariant, transition, or update
   rules.
3. **Directional concept:** Name the central representation, invariant,
   approach family, or data structure. Omit executable transitions, branch
   conditions, pseudocode, and proof.
4. **Near-solution guidance:** Supply transition cases, update order, or
   pseudocode while leaving implementation and validation to the candidate.

A full solution or editorial-level explanation requires an explicit request
and must be recorded separately from these hint rungs.
