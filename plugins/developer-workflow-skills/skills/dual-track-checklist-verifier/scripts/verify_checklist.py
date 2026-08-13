#!/usr/bin/env python3
"""Deterministically + idempotently update a PR body's checklist and evidence section.

Successor to pr-checklist-verifier's update_pr_checklist.py, fixed to work on
bodies produced by the dual-track-pr-creator skill. Three concrete problems in
the original are addressed:

  1. Anchor detection matched the H1 title. The old pattern was
     `^#{1,6}\\s+.*(test|checklist|qa)\\b`, so a PR titled
     "# PR: promote the refactoring-resistant test suite" matched at line 0 and
     the section was inserted above the body's own header block. Titles of
     testing PRs routinely contain "test", which is exactly this tool's
     population. Anchors are now `##`..`######` only (`ANCHOR_HEADING_RE`).

  2. `## Verification` was not recognised. That is the heading
     dual-track-pr-creator emits, so the two skills could not compose. It is
     now in the anchor vocabulary, and `--anchor-heading` overrides outright.

  3. Idempotency broke as a consequence of (1). The upsert removes the section
     and re-inserts it at the computed index, so a wrong index silently undid a
     human's corrected placement on every re-run — while the docstring promised
     a fixed point. With the anchor fixed, and with `--before-heading` to pin
     placement, re-running is a genuine no-op.

Also added, because a checklist is prose as well as state:

  * `--reword OLD::NEW` rewrites an item's text in the same pass as the flip.
    An item that describes its own unverified state ("not yet observed at the
    time of writing") becomes self-contradictory the moment it is ticked.
  * `--audit-table` warns when a ticked item's text also appears in an
    acceptance-traceability row marked FAIL or MISSING. dual-track bodies record
    status in two places; they must not disagree.

What it does NOT do: decide what passed. Judgment stays with the caller.

Usage:
  python verify_checklist.py --body-file BODY [--check TEXT ...]
      [--reword 'OLD::NEW' ...] [--section-file S.md]
      [--section-title '## QA Verification'] [--anchor-heading '## Verification']
      [--before-heading '## Not included'] [--audit-table]
      [--out OUT | --in-place] [--strict]

Exit codes: 0 ok; 2 a --check/--reword matched nothing (only with --strict);
3 a ticked item contradicts a FAIL/MISSING audit row (only with --strict);
1 usage/IO.
"""
from __future__ import annotations

import argparse
import re
import sys

DEFAULT_SECTION_TITLE = "## QA Verification"

# A task-list line: indentation, bullet, unchecked box, then the item text.
UNCHECKED_RE = re.compile(r"^(?P<prefix>\s*[-*]\s+)\[ \](?P<rest>\s+.*)$")
ANY_TASK_RE = re.compile(r"^\s*[-*]\s+\[[ xX]\]\s+")
CHECKED_RE = re.compile(r"^\s*[-*]\s+\[[xX]\]\s+(?P<rest>.*)$")

# Headings that introduce a checklist. `##` and deeper only: an H1 is the PR
# title, and titles about testing are common enough that matching them was the
# original bug. "verification" is included so dual-track-pr-creator bodies work.
ANCHOR_HEADING_RE = re.compile(
    r"^#{2,6}\s+.*(test|checklist|qa|verification)\b", re.IGNORECASE
)

# A Markdown thematic break (---, ***, ___). These divide sections, so they
# bound a section rather than belonging to it.
THEMATIC_BREAK_RE = re.compile(r"^(-{3,}|\*{3,}|_{3,})$")

# An acceptance-traceability row: `| criterion | source | verification | PASS |`
AUDIT_VERDICT_RE = re.compile(r"\b(PASS|FAIL|MISSING)\b")


def _is_section_boundary(line: str) -> bool:
    """True if `line` ends a section: an h1/h2 heading or a thematic break."""
    return bool(re.match(r"^#{1,2}\s+\S", line)) or bool(
        THEMATIC_BREAK_RE.match(line.strip())
    )


def reword_items(body: str, rewords: list[tuple[str, str]]) -> tuple[str, dict[str, bool]]:
    """Replace item text on task lines only, leaving prose untouched.

    Ticking an item whose text says "not yet observed" produces a line that
    contradicts itself, so the rewrite has to happen alongside the flip rather
    than as a separate manual step the caller may forget.
    """
    matched = {old: False for old, _ in rewords}
    out = []
    for line in body.splitlines():
        if ANY_TASK_RE.match(line):
            for old, new in rewords:
                if old and old in line:
                    line = line.replace(old, new)
                    matched[old] = True
        out.append(line)
    result = "\n".join(out)
    return (result + "\n" if body.endswith("\n") else result), matched


def tick_items(body: str, checks: list[str]) -> tuple[str, dict[str, bool]]:
    """Flip unchecked lines whose text contains any check substring.

    Returns the new body and a map of check-string -> whether it matched.
    """
    matched = {c: False for c in checks}
    out_lines = []
    for line in body.splitlines():
        m = UNCHECKED_RE.match(line)
        if m:
            text = m.group("rest")
            hit = next((c for c in checks if c and c in text), None)
            if hit is not None:
                matched[hit] = True
                line = f"{m.group('prefix')}[x]{m.group('rest')}"
        out_lines.append(line)
    result = "\n".join(out_lines)
    if body.endswith("\n"):
        result += "\n"
    return result, matched


def audit_conflicts(body: str) -> list[str]:
    """Ticked items whose text appears in a FAIL/MISSING traceability row.

    A dual-track body states status twice: once as a checkbox, once as a row in
    the acceptance table. Disagreement between them is the kind of thing a
    reviewer trusts and should not have to cross-check by eye.
    """
    checked_texts = [
        m.group("rest").strip()
        for m in (CHECKED_RE.match(ln) for ln in body.splitlines())
        if m
    ]
    bad_rows = [
        ln
        for ln in body.splitlines()
        if ln.lstrip().startswith("|")
        and (m := AUDIT_VERDICT_RE.search(ln))
        and m.group(1) in {"FAIL", "MISSING"}
    ]
    conflicts = []
    for text in checked_texts:
        # Compare on the item's leading words; full lines rarely match verbatim
        # across a checkbox and a table cell.
        stem = re.sub(r"[*`_]", "", text).strip()[:40]
        if len(stem) < 12:
            continue
        for row in bad_rows:
            if stem.lower() in re.sub(r"[*`_]", "", row).lower():
                conflicts.append(f"{stem!r} is ticked but a table row says FAIL/MISSING")
                break
    return conflicts


def _remove_existing_section(lines: list[str], title: str) -> list[str]:
    """Strip an existing section (and one separator blank before it).

    Replace == remove-then-insert, so the insert path stays the single source of
    truth for spacing.
    """
    start = next((i for i, l in enumerate(lines) if l.strip() == title), -1)
    if start == -1:
        return lines
    end = len(lines)
    for j in range(start + 1, len(lines)):
        if _is_section_boundary(lines[j]):
            end = j
            break
    pre = start - 1 if start > 0 and lines[start - 1].strip() == "" else start
    return lines[:pre] + lines[end:]


def _insertion_index(
    lines: list[str],
    anchor_heading: str | None = None,
    before_heading: str | None = None,
) -> int:
    """Where a fresh section goes.

    Order of preference:
      1. immediately before `before_heading` — the caller pinning placement,
         which is how a dual-track body keeps the section between Verification
         and "Not included / out of scope";
      2. after the last task line under `anchor_heading` if given, else under
         the first `##`+ heading whose text looks like a checklist;
      3. end of file.
    """
    if before_heading:
        idx = next(
            (i for i, ln in enumerate(lines) if ln.strip().startswith(before_heading)),
            None,
        )
        if idx is not None:
            return idx

    if anchor_heading:
        heading_idx = next(
            (i for i, ln in enumerate(lines) if ln.strip() == anchor_heading.strip()),
            None,
        )
    else:
        heading_idx = next(
            (i for i, ln in enumerate(lines) if ANCHOR_HEADING_RE.match(ln)), None
        )
    if heading_idx is None:
        return len(lines)

    last_task = heading_idx
    for k in range(heading_idx + 1, len(lines)):
        if ANY_TASK_RE.match(lines[k]):
            last_task = k
        elif re.match(r"^#{1,6}\s+\S", lines[k]) or THEMATIC_BREAK_RE.match(
            lines[k].strip()
        ):
            break
    return last_task + 1


def upsert_section(
    body: str,
    section_md: str,
    title: str = DEFAULT_SECTION_TITLE,
    anchor_heading: str | None = None,
    before_heading: str | None = None,
) -> str:
    """Insert or replace a section idempotently."""
    block_lines = [title, ""] + section_md.strip().splitlines()
    lines = _remove_existing_section(body.splitlines(), title)
    at = _insertion_index(lines, anchor_heading, before_heading)

    before, after = lines[:at], lines[at:]
    chunk: list[str] = []
    if before and before[-1].strip() != "":
        chunk.append("")
    chunk += block_lines
    if after and after[0].strip() != "":
        chunk.append("")

    result = "\n".join(before + chunk + after)
    return result + "\n" if body.endswith("\n") else result


def _parse_reword(spec: str) -> tuple[str, str]:
    if "::" not in spec:
        raise argparse.ArgumentTypeError(
            f"--reword needs 'OLD::NEW', got {spec!r}"
        )
    old, new = spec.split("::", 1)
    return old, new


def main() -> int:
    ap = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter
    )
    ap.add_argument("--body-file", required=True)
    ap.add_argument(
        "--check", action="append", default=[],
        help="Substring of an item to tick. Repeatable.",
    )
    ap.add_argument(
        "--reword", action="append", default=[], type=_parse_reword,
        help="'OLD::NEW' text rewrite, task lines only. Repeatable.",
    )
    ap.add_argument("--section-file", help="Markdown body for the evidence section.")
    ap.add_argument("--section-title", default=DEFAULT_SECTION_TITLE)
    ap.add_argument("--anchor-heading", help="Exact heading whose checklist to follow.")
    ap.add_argument(
        "--before-heading",
        help="Insert immediately before this heading (prefix match).",
    )
    ap.add_argument(
        "--audit-table", action="store_true",
        help="Warn when a ticked item conflicts with a FAIL/MISSING table row.",
    )
    ap.add_argument("--out")
    ap.add_argument("--in-place", action="store_true")
    ap.add_argument("--strict", action="store_true")
    args = ap.parse_args()

    try:
        with open(args.body_file, encoding="utf-8") as f:
            body = f.read()
    except OSError as e:
        print(f"error: cannot read --body-file: {e}", file=sys.stderr)
        return 1

    # Reword before ticking: the caller's --check may target the new wording.
    body, reworded = reword_items(body, args.reword)
    body, matched = tick_items(body, args.check)

    if args.section_file:
        try:
            with open(args.section_file, encoding="utf-8") as f:
                section_md = f.read()
        except OSError as e:
            print(f"error: cannot read --section-file: {e}", file=sys.stderr)
            return 1
        body = upsert_section(
            body, section_md, args.section_title,
            args.anchor_heading, args.before_heading,
        )

    unmatched = [c for c, ok in matched.items() if not ok]
    unmatched += [o for o, ok in reworded.items() if not ok]
    for c in unmatched:
        print(f"warning: no item matched: {c!r}", file=sys.stderr)

    conflicts = audit_conflicts(body) if args.audit_table else []
    for c in conflicts:
        print(f"warning: {c}", file=sys.stderr)

    if args.in_place:
        with open(args.body_file, "w", encoding="utf-8") as f:
            f.write(body)
    elif args.out:
        with open(args.out, "w", encoding="utf-8") as f:
            f.write(body)
    else:
        sys.stdout.write(body)

    if args.strict and conflicts:
        return 3
    if args.strict and unmatched:
        return 2
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
