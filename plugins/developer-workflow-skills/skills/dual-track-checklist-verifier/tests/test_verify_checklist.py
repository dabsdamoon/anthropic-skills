"""Unit tests for scripts/verify_checklist.py.

Run from anywhere with pytest:

    pytest plugins/developer-workflow-skills/skills/dual-track-checklist-verifier/tests

Pure stdlib beyond pytest itself.

The first block below is the reason this skill exists: three regressions
observed against a real dual-track-pr-creator body, none of which the
predecessor's suite covered.
"""
import subprocess
import sys
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parent.parent / "scripts"
SCRIPT = SCRIPT_DIR / "verify_checklist.py"
sys.path.insert(0, str(SCRIPT_DIR))

import verify_checklist as vc  # noqa: E402

TITLE = vc.DEFAULT_SECTION_TITLE


def _count(text: str, heading: str) -> int:
    return sum(1 for line in text.splitlines() if line.strip() == heading)


# A trimmed dual-track-pr-creator Delivery body. Note the H1: it contains the
# word "test", which is what broke the predecessor.
DUAL_TRACK_BODY = """# PR: promote the refactoring-resistant test suite to the release branch

**Track:** Delivery
**Evidence handoff:** missing

## Summary

Promote-only merge.

## Verification

- [x] `pytest -q` -> 631 passed
- [ ] **CI on this PR** - not yet observed at the time of writing
- [ ] **Screen-reader verification** - needs a human

## Not included / out of scope

- This PR ships nothing to users.

## Notes for reviewers

Review the acceptance trace separately.
"""


# --------------------------------------------------------------------------- #
# Regressions this skill was created for
# --------------------------------------------------------------------------- #

def test_h1_title_containing_test_is_not_an_anchor():
    """The predecessor matched `^#{1,6}` and anchored on the PR title."""
    lines = DUAL_TRACK_BODY.splitlines()
    assert vc.ANCHOR_HEADING_RE.match(lines[0]) is None
    out = vc.upsert_section(DUAL_TRACK_BODY, "verdict: PASS")
    idx = out.splitlines().index(TITLE)
    assert idx > out.splitlines().index("**Track:** Delivery"), (
        "section must not land above the body's own header block"
    )


def test_verification_heading_is_recognised():
    """`## Verification` is what dual-track-pr-creator emits."""
    assert vc.ANCHOR_HEADING_RE.match("## Verification")
    out = vc.upsert_section(DUAL_TRACK_BODY, "verdict: PASS").splitlines()
    last_task = max(i for i, ln in enumerate(out) if ln.startswith("- ["))
    assert last_task < out.index(TITLE) < out.index("## Not included / out of scope")


def test_upsert_is_a_fixed_point_on_a_dual_track_body():
    """The predecessor moved the section back to the top on every re-run."""
    once = vc.upsert_section(DUAL_TRACK_BODY, "verdict: PASS\nmetric: 6/6")
    twice = vc.upsert_section(once, "verdict: PASS\nmetric: 6/6")
    assert once == twice
    assert _count(twice, TITLE) == 1


# --------------------------------------------------------------------------- #
# Placement control
# --------------------------------------------------------------------------- #

def test_before_heading_pins_placement():
    out = vc.upsert_section(
        DUAL_TRACK_BODY, "x", before_heading="## Notes for reviewers"
    ).splitlines()
    assert out.index(TITLE) < out.index("## Notes for reviewers")
    assert out.index("## Not included / out of scope") < out.index(TITLE)


def test_before_heading_is_a_fixed_point():
    once = vc.upsert_section(DUAL_TRACK_BODY, "x", before_heading="## Not included")
    twice = vc.upsert_section(once, "x", before_heading="## Not included")
    assert once == twice


def test_explicit_anchor_heading_wins_over_pattern():
    body = "## Testing\n- [ ] a\n\n## Verification\n- [ ] b\n\n## End\nz\n"
    out = vc.upsert_section(body, "x", anchor_heading="## Verification").splitlines()
    assert out.index("- [ ] b") < out.index(TITLE) < out.index("## End")


def test_appends_at_eof_when_nothing_anchors():
    body = "# PR\n\n## Summary\nonly prose\n"
    out = vc.upsert_section(body, "verdict: PASS").splitlines()
    assert out.index(TITLE) > out.index("only prose")


def test_custom_section_title_round_trips():
    once = vc.upsert_section(DUAL_TRACK_BODY, "x", title="## Evidence")
    twice = vc.upsert_section(once, "x", title="## Evidence")
    assert once == twice
    assert _count(twice, "## Evidence") == 1


# --------------------------------------------------------------------------- #
# tick_items — behavior carried over from the predecessor
# --------------------------------------------------------------------------- #

def test_tick_flips_only_matching_unchecked_items():
    out, matched = vc.tick_items(DUAL_TRACK_BODY, ["CI on this PR"])
    assert "- [x] **CI on this PR**" in out
    assert "- [ ] **Screen-reader verification**" in out
    assert matched == {"CI on this PR": True}


def test_tick_ignores_already_checked_items():
    body = "- [x] done\n- [ ] todo\n"
    out, matched = vc.tick_items(body, ["done"])
    assert out == body
    assert matched == {"done": False}


def test_tick_preserves_indentation_and_bullet_style():
    out, _ = vc.tick_items("    * [ ] nested\n", ["nested"])
    assert out == "    * [x] nested\n"


def test_tick_preserves_trailing_newline_state():
    assert vc.tick_items("- [ ] x\n", ["x"])[0].endswith("\n")
    assert not vc.tick_items("- [ ] x", ["x"])[0].endswith("\n")


def test_tick_ignores_empty_check_string():
    body = "- [ ] something\n"
    out, matched = vc.tick_items(body, [""])
    assert out == body
    assert matched == {"": False}


# --------------------------------------------------------------------------- #
# reword_items
# --------------------------------------------------------------------------- #

def test_reword_fixes_a_self_describing_item_before_it_is_ticked():
    """Ticking "not yet observed" leaves a line that contradicts itself."""
    body, reworded = vc.reword_items(
        DUAL_TRACK_BODY,
        [("not yet observed at the time of writing", "6/6 checks pass on 246a9b9")],
    )
    body, _ = vc.tick_items(body, ["CI on this PR"])
    assert "- [x] **CI on this PR** - 6/6 checks pass on 246a9b9" in body
    assert "not yet observed" not in body
    assert reworded == {"not yet observed at the time of writing": True}


def test_reword_touches_task_lines_only():
    body = "prose says not yet observed here\n- [ ] item not yet observed\n"
    out, _ = vc.reword_items(body, [("not yet observed", "verified")])
    assert out.splitlines()[0] == "prose says not yet observed here"
    assert out.splitlines()[1] == "- [ ] item verified"


def test_reword_reports_no_match():
    _, reworded = vc.reword_items("- [ ] a\n", [("absent", "x")])
    assert reworded == {"absent": False}


# --------------------------------------------------------------------------- #
# audit_conflicts
# --------------------------------------------------------------------------- #

def test_audit_flags_a_ticked_item_contradicted_by_the_table():
    body = (
        "| Observable criterion | Source | Verification | Status |\n"
        "|---|---|---|---|\n"
        "| Screen reader announces the active segment | ARIA | none | MISSING |\n"
        "\n## Verification\n"
        "- [x] Screen reader announces the active segment\n"
    )
    conflicts = vc.audit_conflicts(body)
    assert len(conflicts) == 1
    assert "MISSING" in conflicts[0]


def test_audit_is_quiet_when_table_and_checkboxes_agree():
    body = (
        "| c | s | v | Status |\n|---|---|---|---|\n"
        "| Backend suite is green | CI | pytest | PASS |\n"
        "\n## Verification\n- [x] Backend suite is green\n"
    )
    assert vc.audit_conflicts(body) == []


def test_audit_ignores_unchecked_items():
    body = (
        "| c | s | v | Status |\n|---|---|---|---|\n"
        "| Screen reader announces the segment | ARIA | none | MISSING |\n"
        "\n## Verification\n- [ ] Screen reader announces the segment\n"
    )
    assert vc.audit_conflicts(body) == []


def test_audit_skips_stems_too_short_to_match_meaningfully():
    body = (
        "| c | s | v | Status |\n|---|---|---|---|\n| ok | s | v | FAIL |\n"
        "\n## Verification\n- [x] ok\n"
    )
    assert vc.audit_conflicts(body) == []


# --------------------------------------------------------------------------- #
# CLI
# --------------------------------------------------------------------------- #

def _run(*args):
    return subprocess.run(
        [sys.executable, str(SCRIPT), *args], capture_output=True, text=True
    )


def _body(tmp_path):
    p = tmp_path / "body.md"
    p.write_text(DUAL_TRACK_BODY)
    return p


def test_cli_out_writes_result_and_leaves_source_untouched(tmp_path):
    body = _body(tmp_path)
    out = tmp_path / "out.md"
    r = _run("--body-file", str(body), "--check", "CI on this PR", "--out", str(out))
    assert r.returncode == 0
    assert "- [x] **CI on this PR**" in out.read_text()
    assert body.read_text() == DUAL_TRACK_BODY


def test_cli_full_dual_track_run_is_idempotent(tmp_path):
    body = _body(tmp_path)
    section = tmp_path / "qa.md"
    section.write_text("| item | verdict |\n|---|---|\n| CI | PASS |\n")
    args = (
        "--body-file", str(body),
        "--reword", "not yet observed at the time of writing::6/6 checks pass",
        "--check", "CI on this PR",
        "--section-file", str(section),
        "--before-heading", "## Not included",
        "--in-place",
    )
    assert _run(*args).returncode == 0
    first = body.read_text()
    # Second run: --reword and --check no longer match, which is expected.
    assert _run(*args).returncode == 0
    assert body.read_text() == first
    assert first.count(TITLE) == 1
    assert first.count("- [x] **CI on this PR**") == 1
    assert "not yet observed" not in first


def test_cli_strict_exits_2_on_unmatched_check(tmp_path):
    r = _run("--body-file", str(_body(tmp_path)), "--check", "absent", "--strict")
    assert r.returncode == 2
    assert "no item matched" in r.stderr


def test_cli_strict_exits_3_on_audit_conflict(tmp_path):
    body = tmp_path / "b.md"
    body.write_text(
        "| c | s | v | Status |\n|---|---|---|---|\n"
        "| Screen reader announces the active segment | ARIA | none | MISSING |\n"
        "\n## Verification\n- [ ] Screen reader announces the active segment\n"
    )
    r = _run(
        "--body-file", str(body),
        "--check", "Screen reader announces",
        "--audit-table", "--strict",
    )
    assert r.returncode == 3
    assert "FAIL/MISSING" in r.stderr


def test_cli_reword_requires_the_separator(tmp_path):
    r = _run("--body-file", str(_body(tmp_path)), "--reword", "no-separator")
    assert r.returncode != 0
    assert "OLD::NEW" in r.stderr


def test_cli_missing_body_file_exits_1(tmp_path):
    r = _run("--body-file", str(tmp_path / "absent.md"), "--check", "x")
    assert r.returncode == 1
    assert "cannot read --body-file" in r.stderr
