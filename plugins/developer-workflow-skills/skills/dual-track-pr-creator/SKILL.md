---
name: dual-track-pr-creator
description: Create evidence-aware pull request bodies for Dual-Track product work by classifying a change as Discovery/prototype, Delivery/TDD, or a justified combined PR, then preserving the correct evidence gate, review question, and engineering risk analysis. Use when asked to write, review, or open a PR for a prototype, product experiment, discovery handoff, Dual-Track Agile slice, TDD delivery, or any change where customer learning must not be confused with engineering completion.
---

# Dual-Track PR Creator

Make the PR's review question explicit before describing its diff. A Discovery PR asks whether the team learned credibly. A Delivery PR asks whether accepted learning was implemented safely. Do not make one masquerade as the other.

This skill is self-contained. Do not assume another skill can be imported or invoked as a runtime dependency.

## Preserve these invariants

- Classify the PR before choosing its body structure.
- Treat a prototype as an executable question, not as validation.
- Require an explicit evidence decision before describing same-slice production Delivery as accepted.
- Label proxy, stakeholder, heuristic, synthetic, customer, and production evidence accurately.
- Never invent a predeclared threshold, observation, evidence decision, or red-green result.
- Carry observable acceptance criteria into Delivery; do not carry prototype internals as requirements.
- Keep generic blast-radius, security, deviation, test-gap, and out-of-scope analysis in every track.
- State what a reviewer could wrongly assume is complete.

## Gather the change evidence

Resolve the target branch, then run these in parallel:

```bash
git log <target>..HEAD --oneline
git diff <target>...HEAD --name-status
git diff <target>...HEAD --stat
```

Inspect only the full diffs needed to understand material behavior. Also inspect the source of truth and evidence artifacts:

```bash
git log <target>..HEAD --format=%B
rg -n "outcome|assumption|threshold|evidence|decision|handoff|acceptance|red.green|prototype" docs design specs . 2>/dev/null
```

Find dependents for non-trivial changed modules and classify blast radius as `LOW`, `MEDIUM`, `HIGH`, or `CRITICAL`. Scan the diff for secrets, injection, broken authorization, sensitive-data exposure, XSS, dependency risk, permissive configuration, and SSRF. Classify spec mismatches as `deviation`, `deferred`, or `spec defect`.

Do not let a large file list replace product evidence. Do not let a compelling product narrative replace code-risk analysis.

## Classify the PR track

Choose exactly one primary track:

### Discovery

Choose `Discovery` when the primary purpose is to reduce product, usability, desirability, feasibility, or value uncertainty. Typical artifacts include interview notes, observations, experiment definitions, sketches, prototypes, spikes, comparison results, and evidence handoffs.

The primary review question is:

> Did this work test the stated assumption credibly, and does the evidence support the recorded decision?

Read [references/discovery-pr.md](references/discovery-pr.md) completely before drafting.

### Delivery

Choose `Delivery` when the primary purpose is to implement an accepted behavior contract with production-quality code and tests. Typical artifacts include application code, APIs, migrations, integrations, observable acceptance tests, and operational verification.

The primary review question is:

> Does this implementation trace to an accepted handoff and satisfy its contract safely?

Read [references/delivery-pr.md](references/delivery-pr.md) completely before drafting.

### Combined

Choose `Combined` only when the diff contains both the evidence record and Delivery, and history proves the evidence gate was resolved before production implementation for that slice. Read both track references completely and keep separate `Discovery decision` and `Delivery verification` sections.

Do not choose `Combined` merely because a feature includes screenshots, design files, exploratory commits, or tests. If prototype and production implementation advanced together without a prior evidence gate, describe the gate as missing and recommend splitting or holding Delivery review.

If classification is genuinely ambiguous, state the evidence for the leading classification. Ask the user only when the choice would materially change merge eligibility or external publication.

## Apply the evidence gate

For Discovery, record one decision:

- `validated`: the predeclared threshold was met with evidence credible for the claim;
- `rejected`: evidence contradicts the assumption or threshold;
- `insufficient`: the experiment cannot support a decision;
- `provisional`: a clearly identified proxy supports limited continued work while material validation is missing.

For Delivery, record the linked handoff decision. A `rejected` or `insufficient` same-slice handoff blocks normal Delivery approval. A `provisional` handoff permits only work whose scope and risk are explicitly safe to keep provisional.

If no handoff is present, say `Evidence handoff: missing`. Do not reconstruct validation from the implementation or test results.

## Draft the PR body

Follow the selected reference template, then add or retain these common review sections when relevant:

1. Branch, target, date, and change count.
2. Concise summary and one primary review question.
3. Track decision and its supporting artifact.
4. Blast radius with dependents and overall rating.
5. Security rating of `CLEAR`, `NOTE`, or `CONCERN`.
6. Deviations, deferred work, and spec defects.
7. Verification with checked items only for evidence actually observed.
8. Not included / what readers could wrongly assume is complete.
9. Reviewer focus.

Use `experiment:` or `discovery:` titles for learning changes when repository conventions allow. Use `feat:`, `fix:`, or the repository's normal change type for Delivery. A title must not claim validated, production-ready, or complete unless the corresponding evidence supports it.

## Check honesty before publication

For every PR, verify:

- The body names its track and primary review question.
- Claims cite a diff artifact, preserved observation, command result, or linked evidence source.
- Discovery separates raw observation from interpretation.
- Delivery acceptance criteria trace to the handoff or a fixed safety constraint.
- Missing representative-user or production evidence remains visible.
- Red-green evidence is reported only when the failing and passing states were actually observed.
- Automated tests are not presented as usability or customer validation.
- Prototype disposition or deferred product risk is explicit.

If a gate fails, keep the PR factual and mark the missing evidence. Do not polish uncertainty away.

## Create or update the PR

Only mutate GitHub or GitLab when the user authorized PR creation or update. With GitHub CLI, invoke it as `command gh`, verify availability first, and use a body file for a long PR:

```bash
command gh --version
command gh pr create --base <target> --head <source> --title "<title>" --body-file <body-file>
```

After creation, verify the base, head, title, body, commit set, and URL. Report the track and evidence decision alongside the PR link.
