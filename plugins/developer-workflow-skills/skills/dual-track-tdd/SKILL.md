---
name: dual-track-tdd
description: Plan and deliver uncertain product work by running evidence-driven discovery ahead of test-driven implementation. Use when a feature, MVP, Phase 0, UX flow, or product experiment still has desirability or usability risk but also needs production-quality delivery; when a user asks for Dual-Track Agile, discovery plus delivery, prototype-to-TDD, or a comparison of prototype-first and TDD approaches; or when a plan must define explicit evidence, handoff, and acceptance gates before coding.
---

# Dual-Track TDD

Separate learning from production delivery without separating the people doing the work. Use Discovery to reduce product uncertainty and Delivery to implement the resulting behavior contract with TDD.

## Preserve these invariants

- Treat Discovery and Delivery as concurrent tracks across different slices, not as one project-wide waterfall.
- For the same slice, require an evidence handoff before production implementation.
- Treat a prototype as a question made executable. Do not call its existence validation.
- Keep throwaway prototype code separate from production code. Carry decisions and acceptance criteria forward, not accidental architecture.
- Write tests against observable behavior and public boundaries. Avoid assertions on component structure, private helpers, CSS classes, or mock call order.
- Never claim customer validation without customer or production evidence. Label heuristic review, stakeholder approval, and synthetic usability checks accurately.
- Feed delivery findings back into Discovery when implementation exposes a false assumption.

## Build a dual-track plan

Start with one outcome and one thin vertical slice. Record:

```text
Outcome:
Target user and situation:
Riskiest assumption:
Discovery question:
Evidence and success threshold:
Delivery contract:
Out of scope:
```

Divide the plan into:

1. **Discovery:** investigate the riskiest assumption with the cheapest credible method.
2. **Evidence gate:** choose `validated`, `rejected`, or `insufficient evidence` and record why.
3. **Delivery:** convert only accepted learning into observable acceptance criteria and implement it test-first.
4. **Outcome check:** verify the delivered slice and identify the next discovery question.

Keep Delivery pending for a slice until its evidence gate is resolved. Discovery for a later slice may run while the current accepted slice is in Delivery.

## Run Discovery

1. Inspect existing product evidence, code, constraints, and prior decisions.
2. State the assumption before choosing an artifact.
3. Select the smallest credible experiment:
   - interview or workflow observation for problem and desirability risk;
   - sketch or clickable prototype for comprehension and usability risk;
   - technical spike for feasibility risk;
   - data query or production experiment for behavior and value risk.
4. Define the success threshold before running the experiment.
5. Run the experiment and preserve raw observations separately from interpretation.
6. Make the evidence decision.

If representative users are unavailable, proceed only when the requested work can safely remain provisional. Mark the gate `provisional`, state the proxy used, and keep missing user validation as an explicit risk.

## Write the evidence handoff

Produce a concise handoff before Delivery:

```text
Decision: validated | rejected | insufficient | provisional
Evidence:
Observed user behavior or verified constraint:
Accepted interaction and terminology:
Rejected alternatives:
Observable acceptance criteria:
Remaining risks and non-goals:
Prototype disposition: delete | archive | retain as non-production reference
```

Do not turn visual details into requirements unless they are supported by the outcome or evidence. Do not hand implementation internals from a prototype to Delivery as requirements.

## Run Delivery with TDD

For each acceptance criterion, deliver the thinnest vertical slice:

1. Choose the narrowest stable boundary that proves user- or consumer-visible behavior.
2. Write one failing test.
3. Run it and confirm it fails for the intended missing behavior, not setup or syntax.
4. Implement the minimum behavior that passes.
5. Run the focused test.
6. Refactor while green.
7. Run broader contract, integration, build, and browser checks in proportion to risk.
8. Record discoveries that invalidate or extend the handoff and return those questions to Discovery.

Use deterministic fixtures and clocks. Fake only external boundaries. Use real owned collaborators wherever practical.

## Compare implementation methods

When evaluating this workflow against TDD-first or prototype-first:

1. Hold the product contract, fixture, runtime, and verification environment constant.
2. State what each method knew before implementation and prevent later variants from silently benefiting from earlier discoveries.
3. Capture red-green evidence for TDD and predeclared hypotheses and thresholds for Discovery.
4. Compare contract completeness, evidence quality, rework, automated coverage, browser findings, implementation size, and suitability for the dominant uncertainty.
5. Report limitations such as sequence bias, one implementer, missing users, or unmeasured development time.
6. Recommend a method by risk type, not by a universal winner.

## Completion gate

Before declaring the slice complete, verify:

- The evidence decision and its source are explicit.
- Acceptance criteria trace to accepted learning or a fixed safety constraint.
- Each new behavior was observed failing before its implementation passed.
- Tests remain valid across internal refactors.
- The appropriate component, integration, build, and browser checks pass.
- Missing customer evidence and remaining product risks are not disguised as engineering completion.
