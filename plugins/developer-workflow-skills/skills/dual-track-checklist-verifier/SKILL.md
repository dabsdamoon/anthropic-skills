---
name: dual-track-checklist-verifier
description: Verifies the unchecked items in a pull request's checklist by actually running the appropriate tool (browser/webapp-testing for UI behavior, the test suite for "tests pass", curl for endpoints, a build for "compiles", gh for CI status), then closes the loop by updating the PR body — ticking only what it proved, rewording items that described themselves as unverified, and recording the evidence. Built to work on bodies written by dual-track-pr-creator, so it honors the evidence gate: automated results never tick an item that claims customer, usability, or production validation. Use whenever someone asks to "verify the PR checklist", "check off the test plan", "confirm the QA items", "verify and update the PR", or when a PR has `- [ ]` items that should be confirmed before merge.
argument-hint: [pr-number]
model: sonnet
---

# Dual-Track Checklist Verifier

Turn a PR's checklist from a list of intentions into a list of *confirmed facts* — without letting a checkmark claim more than the evidence supports.

A checklist is a promise to the reviewer. `- [ ]` says "someone still needs to confirm this." There are three ways to break that promise:

1. **Verifying without recording.** You run the check, it passes, you move on. The reviewer still sees an empty box and either redoes the work or merges on faith. Verification that never reaches the PR is wasted.
2. **Recording without verifying.** Ticking a box because it *probably* works. A checkmark is a claim. An unbacked one is worse than an empty box: it actively misleads.
3. **Recording the wrong kind of proof.** Ticking "users can tell which tab is active" because an automated test asserts an attribute. The box now claims user validation that nobody obtained. This is the failure mode a dual-track body is specifically built to prevent, and the one a naive verifier walks straight into.

This skill does all three correctly.

## Relationship to sibling skills

- **`dual-track-pr-creator`** writes the bodies this skill reads. It emits a `## Verification` checklist, an acceptance-traceability table with PASS/FAIL/MISSING, and a `## Not included / out of scope` section. All three are load-bearing here.
- **`webapp-testing`** owns browser plumbing — server startup, auth/session injection, DOM assertions. Invoke it for browser-shaped items; do not reinvent it.
- **`pr-checklist-verifier`** is the predecessor. Prefer this skill for any body that came from `dual-track-pr-creator`; see [Why this exists](#why-this-exists) for the three concrete defects that motivated it.

This skill is otherwise self-contained. Do not assume another skill can be imported as a runtime dependency.

## The loop

```
resolve PR → parse checklist → classify each unchecked item →
verify (right tool per item) → evidence-kind gate → honesty gate →
reword + tick + record → cross-check the table → report
```

Work the unchecked items only. Never touch already-checked items or non-checklist prose.

---

## Step 1 — Resolve the PR

Use a given PR number. Otherwise resolve the current branch's PR. Invoke the CLI as `command gh` so a shell alias or function cannot shadow it:

```bash
command gh --version
command gh pr view --json number,title,url,body,headRefName,baseRefName
```

If there is no PR for the branch, stop and say so. Offer `dual-track-pr-creator` if creating one seems to be the intent.

Save the raw `body` verbatim to a file. You will edit it surgically and write it back; never regenerate it from scratch.

## Step 2 — Parse the checklist

Find task-list lines — `- [ ]` / `- [x]`, allowing indentation and `*` bullets. Split into:

- **Already checked** — leave byte-for-byte. Do not re-verify, do not reword.
- **Unchecked** — your work queue.

Zero unchecked items means the checklist is complete. Report that and stop; do not invent work.

Also locate, if present:

- the **acceptance-traceability table** (rows ending in PASS / FAIL / MISSING);
- the **`## Not included / out of scope`** section.

Both record status a second time. If you tick an item, they may now disagree with the checklist — see Step 7.

## Step 3 — Classify each unchecked item

The text is freeform English. Use judgment, not keyword matching.

| Item looks like… | Verify with |
|---|---|
| UI/visual/responsive/interaction behavior | the **webapp-testing** skill — a real browser |
| "tests pass", "suite green", "no regressions" | the project's runner (`pytest`, `npm test`, `go test`) |
| "type-checks", "builds", "compiles", "lint clean" | the build/typecheck/lint command |
| endpoint/API behavior | `curl` or an HTTP client against a running or deployed service |
| "CI is green", "checks pass on this PR" | `command gh pr checks <n>` **and** `statusCheckRollup`; confirm the head SHA the checks ran against |
| data/migration/file-shape claims | query the DB or inspect the file |
| "PM signed off", "copy reads well", "looks on-brand" | **cannot self-verify** — human judgment |
| "users can tell / notice / understand …", "screen reader announces …" | **cannot self-verify** — needs a representative user or assistive technology |
| "behaves correctly in production", "no errors after deploy" | **cannot self-verify** before the deploy exists |

If an item bundles claims ("tabs work and persist across reload"), verify each; tick only if all pass.

When checking CI, verify the checks ran against the current head:

```bash
command gh pr view <n> --json headRefOid,statusCheckRollup,mergeable,mergeStateStatus
```

A green check against a stale SHA proves nothing about what is about to merge.

## Step 4 — Verify, gathering evidence

Capture, per item: the commands run and their key output (pass counts, HTTP status, measured values, SHAs), screenshot paths for browser checks, and a one-line verdict.

Four outcomes:

- **PASS** — proven with evidence. Eligible to tick.
- **FAIL** — you ran it and it did not hold. A **finding**, not a skip. Leave unchecked and surface it prominently; the PR may have a real bug. Never quietly adapt the check until it passes.
- **BLOCKED — needs a human** — subjective, or requires a representative user or assistive technology. No amount of tooling closes it.
- **BLOCKED — deferred to an event** — verifiable later but not now, and not without side effects: a deploy has to happen, a tag has to be pushed, a cron has to fire. Distinct from *needs a human* because it will become checkable on its own; say which event unblocks it.

Keeping those two BLOCKED kinds apart matters. "Needs a human" is a standing gap in the PR. "Deferred to an event" is a scheduling fact, and a reviewer reads them differently.

**Never manufacture the event to close a box.** Pushing a release tag so that a "tag gate works" item can be ticked deploys to production for the sake of a checkmark. Leave it BLOCKED.

## Step 5 — Evidence-kind gate

Before the honesty gate, check that the *kind* of evidence matches the *kind* of claim. This is what makes the skill safe on a dual-track body.

> An automated result may not tick an item that claims customer, usability, or production validation.

Concretely:

| The item claims | An automated pass proves | Verdict |
|---|---|---|
| an attribute/DOM state exists | exactly that | may tick |
| a user can perceive or understand something | nothing about perception | BLOCKED — needs a human |
| a screen reader announces something | that the attribute is present, not that it is announced | BLOCKED — needs a human |
| behavior in production | nothing until deployed | BLOCKED — deferred |
| a stakeholder approved | nothing | BLOCKED — needs a human |

When an item mixes both ("`aria-current` is set **and** users hear the active segment"), split it in the report: the attribute half is proven, the perception half is not, and the box stays unchecked because the item as written is not satisfied.

## Step 6 — Honesty gate

> **Tick a box only for an item with a PASS and real evidence behind it. Everything else stays unchecked.**

No "probably fine." No ticking a FAIL because the fix looks easy. No checking a subjective item because you hold an opinion. An honest "could not verify X" is far more useful to a reviewer than a false green check.

## Step 7 — Reword, tick, and record

Do all three in one pass with the bundled helper. **Read `--help` before first use.**

### Reword items that describe their own state

An item written as `- [ ] CI on this PR — not yet observed at the time of writing` becomes self-contradictory the instant it is ticked. Flipping the box is not enough; the sentence has to stop claiming it is unverified. Pass `--reword 'OLD::NEW'`, which rewrites task lines only and leaves prose alone.

### Record the evidence

Write a section documenting every item — PASS, FAIL, and both BLOCKED kinds — so the reviewer sees the whole picture, not just the wins. On a dual-track body, place it between the checklist and `## Not included / out of scope` with `--before-heading`.

```bash
python scripts/verify_checklist.py \
  --body-file /tmp/pr_body.md \
  --reword 'not yet observed at the time of writing::6/6 checks pass on 246a9b9' \
  --check "CI on this PR" \
  --section-file /tmp/evidence.md \
  --before-heading "## Not included" \
  --audit-table --strict \
  --out /tmp/pr_body_new.md
```

The helper flips only lines containing a `--check` string, replaces rather than stacks the evidence section, and is a fixed point under re-running. `--audit-table` warns when a ticked item's text also appears in a traceability row marked FAIL or MISSING — a dual-track body states status twice and the two must not disagree. With `--strict`, that warning is exit code 3.

Diff before pushing, then push:

```bash
command diff -u /tmp/pr_body.md /tmp/pr_body_new.md
command gh pr edit <number> --body-file /tmp/pr_body_new.md
```

### Reconcile the second record

If a ticked item corresponds to a table row still reading MISSING, update the row too. If `## Not included / out of scope` lists something you just proved, remove that line. Leaving them stale re-creates the problem this skill exists to fix, one section lower.

## Step 8 — Report

- **Ticked (N):** each item + one-line evidence.
- **Failed (N):** each item + what broke. Call these out; they may block merge.
- **Blocked — needs a human (N):** each item + who has to do it.
- **Blocked — deferred (N):** each item + which event unblocks it.
- Any table/out-of-scope lines you reconciled.
- The PR URL.

If nothing could be verified, say so plainly and do not edit the PR.

---

## Principles

- **Close the loop or it did not happen.** The deliverable is an updated PR body, not a verification you keep to yourself.
- **A checkmark is a claim.** Back every one with evidence of the right *kind*.
- **A failed check is a gift.** Discovering that "persists across reload" is broken is the best possible outcome of running it.
- **Never manufacture the event.** Do not deploy, tag, or mutate production to close a box.
- **Touch only what you verified.** Preserve checked items, prose, and formatting exactly. Running twice equals running once.
- **Lean on webapp-testing for browser work.** Orchestrate it; do not duplicate its machinery.

## Why this exists

Three defects observed running the predecessor against a real `dual-track-pr-creator` body, none covered by its test suite. All three are regression-tested in `tests/`.

1. **The anchor matched the H1 title.** `^#{1,6}\s+.*(test|checklist|qa)\b` matched `# PR: promote the refactoring-resistant test suite …`, so the evidence section was inserted above the body's own `**Track:**` header. PR titles about testing are this tool's whole population. Anchors are now `##`..`######` only.
2. **`## Verification` was invisible.** That is the heading the sibling skill emits, and it contains none of `test|checklist|qa`. The two skills could not compose. `verification` is now in the vocabulary, and `--anchor-heading` / `--before-heading` override outright.
3. **Idempotency was not a fixed point.** Following from (1): the upsert removes the section then re-inserts it at the computed index, so a wrong index silently undid a human's corrected placement on every re-run — while the docstring promised idempotency.

Beyond the fixes, this skill adds the evidence-kind gate (Step 5), the two-way BLOCKED split (Step 4), `--reword` for self-describing items, and `--audit-table` for checklist/table agreement.

## Example

**Input:** a dual-track Delivery body with

```
## Verification
- [x] pytest -q → 631 passed
- [ ] **CI on this PR** — not yet observed at the time of writing
- [ ] **Screen-reader verification of aria-current** — the announcement needs a human
- [ ] **Tag-gate behavior on the new main** — unverifiable until a tag is pushed
```

**Process:** CI → `gh pr checks` + rollup, head SHA matches `origin/develop` → PASS, and the text is reworded so it no longer says "not yet observed". Screen reader → evidence-kind gate: an e2e assertion proves the attribute, not the announcement → BLOCKED, needs a human. Tag gate → BLOCKED, deferred; pushing a tag would deploy.

**Output:** one box flipped with its wording corrected, an evidence section placed before `## Not included` recording all three, two boxes deliberately left unchecked.

**Report:**
> Ticked 1 of 3 on PR #96. CI: PASS — 6/6 checks on `246a9b9`, `mergeStateStatus=CLEAN`, `Deploy Production (Vercel)` correctly SKIPPED. Left unchecked: screen-reader announcement (needs a person with assistive tech — e2e proves the attribute, not the announcement) and tag-gate behavior (deferred; proving it means pushing a tag, which deploys).
