#!/usr/bin/env python3
"""Verify fingerprint and monetary consistency across rendered Markdown reports."""

from __future__ import annotations

import argparse
from pathlib import Path

from fde_estimation import load_structured, write_json


def parser() -> argparse.ArgumentParser:
    result = argparse.ArgumentParser()
    result.add_argument("--calculation", required=True)
    result.add_argument("--output-dir", required=True)
    result.add_argument("--output", required=True)
    return result


def formatted(value: object) -> str:
    if isinstance(value, float) and not value.is_integer():
        return f"{value:,.2f}"
    return f"{int(value):,}"


def main() -> int:
    args = parser().parse_args()
    calculation = load_structured(args.calculation)
    output_dir = Path(args.output_dir)
    errors: list[str] = []
    required = ["budgetary-estimate.md", "basis-of-estimate.md"]
    scenario_files = {
        "change-adjustment": "change-adjustment.md",
        "remaining-work": "remaining-work-estimate.md",
    }
    for scenario in calculation["scenarios"]:
        if scenario["scenario"] in scenario_files:
            required.append(scenario_files[scenario["scenario"]])
    marker = f"<!-- estimate-fingerprint:{calculation['fingerprint']} -->"
    documents: dict[str, str] = {}
    for name in required:
        path = output_dir / name
        if not path.exists():
            errors.append(f"missing report: {name}")
            continue
        text = path.read_text(encoding="utf-8")
        documents[name] = text
        if marker not in text:
            errors.append(f"{name}: missing calculation fingerprint")
        if "[TODO" in text or "{{" in text:
            errors.append(f"{name}: unresolved placeholder")
    for scenario in calculation["scenarios"]:
        total = formatted(scenario["total"])
        if total not in documents.get("budgetary-estimate.md", ""):
            errors.append(
                f"budgetary-estimate.md: missing {scenario['scenario']} total {total}"
            )
        if total not in documents.get("basis-of-estimate.md", ""):
            errors.append(
                f"basis-of-estimate.md: missing {scenario['scenario']} total {total}"
            )
        optional_name = scenario_files.get(scenario["scenario"])
        if optional_name and total not in documents.get(optional_name, ""):
            errors.append(f"{optional_name}: missing scenario total {total}")
    report = {
        "ok": not errors,
        "errors": errors,
        "warnings": [],
        "calculation_fingerprint": calculation["fingerprint"],
        "verified_files": sorted(documents),
    }
    write_json(args.output, report)
    status = "PASS" if not errors else "FAIL"
    print(
        f"Estimate package verification {status}: "
        f"{len(documents)} file(s), {len(errors)} error(s). "
        f"Report: {Path(args.output).resolve()}"
    )
    return 0 if not errors else 1


if __name__ == "__main__":
    raise SystemExit(main())
