---
name: collect-as-built-evidence
description: Collect a bounded, read-only as-built evidence record from a Git repository and related implementation artifacts. Use when a user needs to inventory delivered or remaining product scope, connect code, tests, deployment, architecture, and operating documents to customer outcomes and FDE decisions, or prepare implementation evidence for a scope delta, budgetary estimate, work valuation, or change-adjustment discussion.
---

# Collect As-Built Evidence

Treat the repository as implementation evidence, not a timesheet or proof of
commercial entitlement.

## Workflow

1. Read `../../references/interactive-review-protocol.md` completely.
2. Define repository path, revision, reporting boundary, project name, and
   output directory. Do not silently include all refs or the working tree.
3. Read `../../references/evidence-and-claim-rules.md` completely.
4. Read `references/interpretation-and-output.md` completely.
5. Reuse a compatible `git-evidence.json` from
   `generate-git-work-report` when the user supplies one. Otherwise collect a
   narrow snapshot:

```bash
python3 "$PLUGIN_DIR/scripts/collect_git_evidence.py" \
  --repo "$REPO_PATH" \
  --ref HEAD \
  --project-name "$PROJECT_NAME" \
  --output "$OUTPUT_DIR/as-built-evidence.json"
```

6. Inspect README, project guidance, ADRs, domain notes, source modules, tests,
   deployment files, release notes, issue or PR context, and substantive merge
   messages.
7. Add implementation items to the draft. For each item record:
   - what was delivered;
   - `new`, `modified`, or `reused`;
   - delivery status;
   - related outcome and decision IDs;
   - stable code, test, document, deployment, or review evidence;
   - known verification and limitations.
8. Do not derive M/M from commits. Add external work or time records only as
   separately identified evidence.
9. Create `as-built-evidence.md` from the same implementation items.
10. Set `status` to `final` and validate against the baseline and discovery
   inputs when available.

Read-only collection may run before GATE-0, but it must stop at evidence. Do not
select an estimate scenario, infer customer value or approval, or choose rates,
M/M, margin, risk, or commercial entitlement from repository contents.

## Safety

- Keep production customer systems and data read-only.
- Do not expose credentials, personal data, author emails, or sensitive paths.
- Stop and disclose shallow history, missing refs, rewritten history, empty
  scope, or truncation.
- Do not describe unverified working-tree changes as delivered.

## Completion gate

Require at least one editorially verified implementation item for a final
artifact. A raw Git snapshot remains a draft.
