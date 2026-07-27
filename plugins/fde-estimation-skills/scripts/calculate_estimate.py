#!/usr/bin/env python3
"""Calculate independent estimate scenarios with reproducible decimal arithmetic."""

from __future__ import annotations

import argparse

from fde_estimation import (
    calculate_scenarios,
    fingerprint,
    load_structured,
    utc_now,
    validate_package,
    write_json,
)


def parser() -> argparse.ArgumentParser:
    result = argparse.ArgumentParser()
    result.add_argument("--scope-traceability", required=True)
    result.add_argument("--estimation-policy", required=True)
    result.add_argument("--generated-at")
    result.add_argument("--output", required=True)
    result.add_argument("--verification", required=True)
    return result


def main() -> int:
    args = parser().parse_args()
    traceability = load_structured(args.scope_traceability)
    policy = load_structured(args.estimation_policy)
    report = validate_package(
        policy=policy,
        traceability=traceability,
        final=True,
    )
    if not report.ok:
        write_json(args.verification, report.as_dict())
        print(
            f"Estimate calculation FAIL: {len(report.errors)} validation error(s)."
        )
        return 1
    scenarios = calculate_scenarios(traceability, policy)
    if not scenarios:
        report.error(
            "scope-traceability: no allocations are included in an estimate scenario"
        )
        write_json(args.verification, report.as_dict())
        print("Estimate calculation FAIL: no included scenario allocation.")
        return 1
    calculation_core = {
        "schema_version": "1.0",
        "document_type": "estimate-calculation",
        "project": traceability["project"]["name"],
        "currency": policy["currency"],
        "input_fingerprints": {
            "scope_traceability": fingerprint(traceability),
            "estimation_policy": fingerprint(policy),
        },
        "scenarios": scenarios,
    }
    calculation = {
        **calculation_core,
        "generated_at": args.generated_at or utc_now(),
        "fingerprint": fingerprint(calculation_core),
    }
    write_json(args.output, calculation)
    write_json(
        args.verification,
        {
            "ok": True,
            "errors": [],
            "warnings": report.warnings,
            "calculation_fingerprint": calculation["fingerprint"],
            "scenario_count": len(scenarios),
        },
    )
    print(
        f"Estimate calculation PASS: {len(scenarios)} scenario(s). "
        f"Output: {args.output}"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
