---
name: pr-creator
description: Creates professional Pull Request (PR) documentation in markdown format. Use this skill when asked to create a PR, write PR notes, document code changes for review, or prepare merge request documentation. The skill analyzes git changes, understands the codebase context, and produces comprehensive PR documentation.
argument-hint: [target-branch]
model: sonnet
---

# PR Creator Skill

Creates comprehensive Pull Request documentation in markdown format, suitable for copying into GitHub/GitLab PR descriptions or saving as PR notes.

## When to Use This Skill

- Creating PR documentation for code changes
- Writing PR notes before submitting for review
- Documenting what changed and why
- Preparing merge request descriptions

## How to Create PR Documentation

### Step 1: Gather Information (Run in Parallel)

Before writing the PR, collect information by running these git commands **in parallel** (single message, multiple Bash tool calls for speed):

```bash
# Run ALL THREE in parallel (single message with 3 Bash tool calls)
git log <target-branch>..HEAD --oneline           # Commit history
git diff <target-branch>...HEAD --name-status     # Changed files list
git diff <target-branch>...HEAD --stat            # Change statistics
```

**After** reviewing the above, only run full diff for specific files if needed:
```bash
git diff <target-branch>...HEAD -- path/to/specific/file.ts
```

**Context**: Ask the user about the purpose/reason for the changes if not clear from commits

### Step 2: Blast Radius Analysis

Assess how far the changes ripple through the codebase. Run these **in parallel**:

```bash
# For each modified file, find how many other files depend on it
# Repeat for key changed files
grep -rn "from.*<changed-module>.*import\|require.*<changed-module>" --include="*.py" --include="*.ts" --include="*.tsx" --include="*.js" .
grep -rn "<changed-function-or-class>" --include="*.py" --include="*.ts" --include="*.tsx" --include="*.js" . | grep -v "def \|function \|class "
```

Classify each changed file:

| Blast Radius | Criteria | Review Urgency |
|---|---|---|
| **LOW** | Leaf file (no other files import it), test files, docs | Normal |
| **MEDIUM** | Imported by 2-5 files, component used in a few pages | Careful |
| **HIGH** | Imported by 6+ files, shared utility/hook/service, config files | Thorough |
| **CRITICAL** | Auth, DB schema, API contracts, env config, CI/CD | Requires sign-off |

Include the blast radius summary in the PR documentation (see template below).

### Step 3: Security Analysis

Scan the diff for common security concerns. Check for:

**Secrets & Credentials:**
```bash
# Search diff for potential secrets
git diff <target-branch>...HEAD | grep -iE "(password|secret|token|api_key|apikey|private_key|credential|auth_token)\\s*[=:]" | grep -v "\\.(md|txt|example):"
```

**OWASP Top 10 Checks (review the diff for):**

| Category | What to Look For |
|---|---|
| **Injection** | Raw SQL, unsanitized user input in queries, `eval()`, `exec()`, template literals in queries |
| **Broken Auth** | Hardcoded tokens, missing auth checks on new endpoints, session handling changes |
| **Sensitive Data** | Logging PII, exposing internal errors to clients, new env vars with secrets |
| **XSS** | `dangerouslySetInnerHTML`, unescaped user content, `innerHTML` assignment |
| **Insecure Dependencies** | New packages with known CVEs, pinned to vulnerable versions |
| **Misconfiguration** | CORS wildcards (`*`), debug mode in prod, permissive file permissions |
| **SSRF** | User-controlled URLs passed to `fetch`/`requests` without validation |

**Rate the overall security posture:**
- **CLEAR** — No security-relevant changes detected
- **NOTE** — Minor items worth mentioning (e.g., new env var, new dependency)
- **CONCERN** — Issues found that should be addressed before merge

Include findings in the PR documentation (see template below).

### Step 4: Deviation & Scope Analysis

Blast radius and security are mechanical — grep finds them. This step is not, and it is the one reviewers most need. Ask two questions the diff alone cannot answer.

**"Where does this depart from what was asked?"**

Find the source of truth first, then compare each major change against it:

```bash
git log <target-branch>..HEAD --format=%B | grep -iE "closes|fixes|implements|refs|spec|design|ticket"
ls docs/ design/ specs/ 2>/dev/null   # spec/design docs the PR may implement
```

Classify anything that does not match:

| Type | Meaning | What to write |
|---|---|---|
| **Deviation** | Built deliberately differently from the spec/design/ticket | What the spec asked, what you built, and why the difference is correct |
| **Deferred** | A spec item this PR does not implement at all | What is missing and whether it blocks the spec's goal |
| **Spec defect** | The spec itself is wrong, stale, or self-contradictory | Whether this PR corrects it or only surfaces it |

Spec defects are worth their own attention. If the spec contradicts itself, say so and state which way you resolved it — a reviewer diffing implementation against spec will otherwise read your correct code as a bug. If you cannot resolve it, **do not guess**: implement the spec faithfully and raise it as an open question for the spec owner. Silently "fixing" a spec you misread is worse than transcribing one that is wrong.

**"What would a reader wrongly assume is done?"**

List work the change implies but does not contain: deferred spec items, follow-ups the approach now requires, stale artifacts left untouched, pre-existing problems in files you edited but chose not to fix.

Both answers go in the PR (see template). If genuinely neither applies — the change matches its spec exactly and implies no follow-up — say that explicitly rather than dropping the sections.

---

### Step 5: Analyze Changes

For each changed file, understand:
- **What** changed (added, modified, deleted)
- **Why** it changed (bug fix, feature, refactor, etc.)
- **Impact** on other parts of the system

### Step 6: Write PR Documentation

Generate a markdown document with the following sections:

---

## PR Documentation Template

```markdown
# PR: [Title - Brief description of the change]

**Branch:** `[source-branch]` → `[target-branch]`
**Date:** [YYYY-MM-DD]
**Total Files Changed:** [count] ([new] new, [modified] modified, [deleted] deleted)

## Summary

[2-4 sentences explaining:]
- What this PR does
- Why this change is needed
- High-level approach taken

**Key Features/Fixes:**
- [Bullet point 1]
- [Bullet point 2]
- [Bullet point 3]

---

## Blast Radius

| File | Dependents | Radius | Notes |
|------|-----------|--------|-------|
| `path/to/shared-util.ts` | 12 files | **CRITICAL** | Used across all services |
| `path/to/component.tsx` | 3 files | MEDIUM | Used in 3 pages |
| `path/to/leaf-file.ts` | 0 files | LOW | No downstream dependents |

**Overall Blast Radius:** [LOW / MEDIUM / HIGH / CRITICAL]

---

## Security Analysis

**Rating:** [CLEAR / NOTE / CONCERN]

[If CLEAR:]
> No security-relevant changes detected.

[If NOTE or CONCERN, list findings:]

| Category | Finding | Severity | File |
|----------|---------|----------|------|
| [e.g., Sensitive Data] | [e.g., New env var `API_SECRET` added] | NOTE | `path/to/file` |
| [e.g., Injection] | [e.g., Raw user input in SQL query] | CONCERN | `path/to/file` |

[If CONCERN, add recommended actions:]
> **Action Required:** [Describe what should be fixed before merge]

---

## Deviations from Spec

[Where the implementation departs from the spec/design/ticket it implements. If it matches exactly:]
> No deviations — implementation follows the spec as written.

[Otherwise:]

| Type | Item | Spec said | This PR does | Why |
|------|------|-----------|--------------|-----|
| Deviation | [e.g., Inline guide switching] | [what the design drew] | [what shipped] | [why the difference is correct] |
| Deferred | [e.g., Memory-save card] | [what the spec asked] | Not implemented | [what blocks it] |
| Spec defect | [e.g., Mixed register in copy] | [the contradiction] | [corrected here / surfaced only] | [how it was resolved] |

[For spec defects you could NOT resolve — implement the spec faithfully and ask:]

> **Open question for [spec owner]:** [state the contradiction, what the PR currently does, and what you need decided]

---

## Major Changes

### 1. [Major Change Category 1]

**Files Changed:**
- `path/to/file1.ts`
- `path/to/file2.ts`

**Why:**
[Explain why this change was needed]

**Key Implementation:**
```[language]
// Key code snippet if helpful
```

---

### 2. [Major Change Category 2]

[Repeat the pattern above for each major change category]

---

## All Files Changed

### [Category 1] Files ([count] files)

| File | Change | Purpose |
|------|--------|---------|
| `path/to/file.ts` | Modified | [Brief description] |
| `path/to/new-file.ts` | **NEW** | [Brief description] |
| `path/to/deleted-file.ts` | ~~Deleted~~ | [Why removed] |

### [Category 2] Files ([count] files)

[Repeat table for each category]

---

## Environment Variables

[If new environment variables are needed]

```env
# [Category]
VARIABLE_NAME=description-or-example-value
ANOTHER_VARIABLE=value
```

[If no new environment variables:]
> No new environment variables required.

---

## Testing Checklist

- [x] [Test case already verified by integration/unit tests]
- [x] [Another test case covered by automated tests]
- [ ] [Test case requiring manual verification - describe steps]
- [ ] [Another manual check needed]
- [ ] [Automatable test case not yet covered] ⚠️ **automatable** — suggest adding unit/integration test

---

## Related PRs / Dependencies

[If this PR depends on or relates to other PRs]

- [Related PR title](link) - [relationship description]

[If none:]
> No related PRs.

---

## Screenshots / Demo

[If applicable, include screenshots or demo links]

---

## Not Included / Out of Scope

[Work a reader might reasonably assume is done, but isn't. If nothing applies:]
> No known gaps — this PR fully covers its scope.

[Otherwise:]

- [Deferred spec item] — [why deferred, and whether it blocks anything]
- [Follow-up this approach now requires]
- [Stale artifact deliberately left untouched] — [e.g., superseded prototypes still carry old copy]
- [Pre-existing issue in a file you edited but chose not to fix] ⚠️ **automatable** — [if a test could cover it]

---

## Notes for Reviewers

[Any special instructions or areas to focus on during review]
```

---

## Guidelines

### Blast Radius Section
- Run dependency grep for every file with non-trivial changes
- Always classify each changed file into LOW / MEDIUM / HIGH / CRITICAL
- Flag CRITICAL items prominently — these need reviewer attention
- State the overall blast radius clearly

### Security Analysis Section
- Always scan the diff for secrets and OWASP concerns
- Rate as CLEAR if nothing found — don't skip the section
- For CONCERN items, include specific file and line references
- Recommend concrete fixes, not vague warnings

### Deviations from Spec Section
- Compare every major change against the spec/design/ticket it implements — do not assume the diff speaks for itself
- State what the spec asked, what shipped, and why the difference is correct. Two of the three is not enough
- Distinguish **deviation** (built differently on purpose) from **deferred** (not built) from **spec defect** (the spec is wrong)
- If you corrected a spec, say so here AND change the spec file in the same PR — otherwise implementation and spec drift apart silently
- If you could not resolve a spec contradiction, implement the spec faithfully and raise an open question. Never silently "fix" a spec you might be misreading
- Say "no deviations" explicitly when true — a missing section reads as an unasked question

### Not Included / Out of Scope Section
- Ask what a reader would wrongly assume is finished, and name it
- Cover: deferred spec items, follow-ups the approach now requires, stale artifacts left untouched, pre-existing issues in files you edited
- This is what stops a partial change being read as complete, and stops reviewers filing bugs for gaps you already know about
- Naming a gap converts it from an oversight into a decision

### Summary Section
- Be concise but complete
- Focus on the "what" and "why"
- Use bullet points for key features

### Major Changes Section
- Group related changes together
- Explain the reasoning, not just the code
- Include code snippets only when they add clarity

### Files Changed Section
- Categorize files logically (by feature, by type, etc.)
- Use tables for readability
- Mark NEW and Deleted files clearly

### Environment Variables Section
- Only include if new variables are needed
- Provide example values or descriptions
- Group by category if multiple

### Testing Checklist Section
- **Checked `[x]`**: Items already verified by existing integration/unit tests (pre-verified)
- **Unchecked `[ ]`**: Items that require manual verification by the reviewer (e.g., UI appearance, deploy steps, browser testing)
- Be specific about what to test
- Cover edge cases and regression tests

**Test coverage gap analysis (important):** Before finalizing the checklist, review each unchecked `[ ]` item and ask: *"Can this be covered by a unit or integration test?"* If the answer is yes — and the project already has a test setup — **flag it explicitly** as a test gap rather than leaving it as a manual-only item. Use this format:

```markdown
- [ ] Verify user registration creates auth user + member record ⚠️ **automatable** — suggest adding unit test
```

This ensures reviewers and authors are aware that the item is unchecked not because it *can't* be tested, but because a test *hasn't been written yet*. The goal is to minimize false "manual-only" items and encourage test coverage before merge.

---

## Quick Template (for simple PRs)

For small changes (< 5 files), use this minimal format instead of the full template:

```markdown
## Summary
[1-2 sentences explaining what and why]

## Changes
- [bullet point for each major change]

## Deviations / Not included
- [any departure from the spec, or known gap — omit only if genuinely none]

## Test plan
- [x] [item verified by automated tests]
- [ ] [item requiring manual verification]

🤖 Generated with [Claude Code](https://claude.com/claude-code)
```

---

## Creating the PR with GitHub CLI

**IMPORTANT:** Invoke GitHub CLI as `command gh`. This resolves `gh` through
`PATH` while bypassing shell aliases and functions, so it works across
Homebrew, Linux, and other installations without a hard-coded path.

Verify that the executable is available before creating or updating a PR:

```bash
if ! command gh --version >/dev/null 2>&1; then
  echo "GitHub CLI (gh) is not installed or not available on PATH." >&2
  exit 1
fi
```

For faster PR creation, use `command gh pr create` with HEREDOC directly (avoids creating intermediate files):

```bash
command gh pr create --base main --head feature-branch --title "feat: Brief title" --body "$(cat <<'EOF'
## Summary
[1-2 sentences]

## Changes
- [bullet points]

## Deviations / Not included
- [departure from spec, or known gap — omit only if genuinely none]

## Test plan
- [ ] [verification steps]

🤖 Generated with [Claude Code](https://claude.com/claude-code)
EOF
)"
```

**For longer PRs**, write to a temp file first then use `--body-file`:
```bash
# Write PR body to temp file
# Then create PR
command gh pr create --base main --head feature-branch --title "feat: Title" --body-file /tmp/pr-body.md
```

---

## Performance Tips

1. **Parallel git commands**: Always run `git log`, `git diff --name-status`, and `git diff --stat` in parallel (single message with multiple Bash calls)
2. **Use HEREDOC**: Avoid intermediate files for short PRs with `--body "$(cat <<'EOF' ... EOF)"`
3. **Stat before diff**: Use `--stat` first to see scope, only full diff specific files if needed
4. **Minimal first**: Start with quick template, add detail only if the PR is complex
5. **Skip optional sections**: Omit Screenshots/Demo, Related PRs, Environment Variables if not applicable
6. **Don't over-document**: A clear summary + changes list is often sufficient

## Keywords

PR, pull request, merge request, code review, git, documentation, changelog

## Reference Examples
- For a bugfix PR example, see [examples/bugfix-pr.md](examples/bugfix-pr.md)
- For a feature PR example, see [examples/sso-feature-pr.md](examples/sso-feature-pr.md)
