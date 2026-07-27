#!/usr/bin/env python3
"""Collect a bounded, read-only Git snapshot for as-built editorial analysis."""

from __future__ import annotations

import argparse
import hashlib
import subprocess
from pathlib import Path

from fde_estimation import utc_now, write_json


def run_git(repo: Path, *args: str) -> str:
    completed = subprocess.run(
        ["git", "-C", str(repo), *args],
        check=True,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    return completed.stdout.strip()


def parser() -> argparse.ArgumentParser:
    result = argparse.ArgumentParser()
    result.add_argument("--repo", required=True)
    result.add_argument("--ref", default="HEAD")
    result.add_argument("--project-name", required=True)
    result.add_argument("--max-commits", type=int, default=5000)
    result.add_argument("--output", required=True)
    return result


def main() -> int:
    args = parser().parse_args()
    repo = Path(args.repo).resolve()
    try:
        is_work_tree = run_git(repo, "rev-parse", "--is-inside-work-tree")
    except (subprocess.CalledProcessError, FileNotFoundError):
        is_work_tree = "false"
    if is_work_tree != "true":
        raise SystemExit(f"not a Git repository: {repo}")
    head = run_git(repo, "rev-parse", args.ref)
    count = int(run_git(repo, "rev-list", "--count", args.ref))
    if count > args.max_commits:
        raise SystemExit(
            f"revision contains {count} commits, above --max-commits "
            f"{args.max_commits}; narrow the evidence boundary"
        )
    log_text = run_git(
        repo,
        "log",
        args.ref,
        "--reverse",
        "--date=iso-strict",
        "--format=%H%x1f%aI%x1f%s",
    )
    commits = []
    for line in log_text.splitlines():
        if not line:
            continue
        parts = line.split("\x1f", 2)
        if len(parts) != 3:
            raise SystemExit(f"unexpected Git log record: {line!r}")
        commit_hash, authored_at, subject = parts
        commits.append(
            {
                "hash": commit_hash,
                "authored_at": authored_at,
                "subject": subject,
            }
        )
    fingerprint_source = "\n".join(commit["hash"] for commit in commits)
    git_fingerprint = hashlib.sha256(
        fingerprint_source.encode("utf-8")
    ).hexdigest()
    output = {
        "schema_version": "1.0",
        "document_type": "as-built-evidence",
        "status": "draft",
        "project": {"name": args.project_name},
        "evidence_boundary": {
            "repository": str(repo),
            "revision": args.ref,
            "collected_at": utc_now(),
        },
        "git_evidence": {
            "head": head,
            "commit_count": len(commits),
            "first_commit_at": commits[0]["authored_at"] if commits else None,
            "last_commit_at": commits[-1]["authored_at"] if commits else None,
            "fingerprint": git_fingerprint,
            "commits": commits,
        },
        "implementation_items": [],
        "limitations": [
            "Git proves recorded changes inside the selected revision boundary, "
            "not hours, business value, customer approval, or off-repository work.",
            "An editor must add implementation_items from repository context before "
            "marking this artifact final.",
        ],
    }
    write_json(args.output, output)
    print(
        f"Collected {len(commits)} commit record(s) at {head[:12]}. "
        f"Draft: {Path(args.output).resolve()}"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
