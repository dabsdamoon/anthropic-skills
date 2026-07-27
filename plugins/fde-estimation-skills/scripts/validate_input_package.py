#!/usr/bin/env python3
"""Validate one or more canonical FDE estimation artifacts."""

from __future__ import annotations

import argparse
from pathlib import Path

from fde_estimation import (
    file_fingerprint,
    load_structured,
    utc_now,
    validate_package,
    write_json,
)


def parser() -> argparse.ArgumentParser:
    result = argparse.ArgumentParser()
    result.add_argument("--customer-baseline")
    result.add_argument("--field-discovery")
    result.add_argument("--as-built-evidence")
    result.add_argument("--estimation-policy")
    result.add_argument("--scope-traceability")
    result.add_argument("--final", action="store_true")
    result.add_argument("--output", required=True)
    result.add_argument("--manifest")
    return result


def main() -> int:
    args = parser().parse_args()
    paths = {
        "customer-baseline": args.customer_baseline,
        "field-discovery": args.field_discovery,
        "as-built-evidence": args.as_built_evidence,
        "estimation-policy": args.estimation_policy,
        "scope-traceability": args.scope_traceability,
    }
    loaded = {
        key: load_structured(value) if value else None for key, value in paths.items()
    }
    report = validate_package(
        customer=loaded["customer-baseline"],
        discovery=loaded["field-discovery"],
        as_built=loaded["as-built-evidence"],
        policy=loaded["estimation-policy"],
        traceability=loaded["scope-traceability"],
        final=args.final,
    )
    output = {
        "validated_at": utc_now(),
        "final_mode": args.final,
        "inputs": {
            key: {
                "path": str(Path(value).resolve()),
                "fingerprint": file_fingerprint(value),
            }
            for key, value in paths.items()
            if value
        },
        **report.as_dict(),
    }
    write_json(args.output, output)
    if args.manifest:
        manifest = {
            "schema_version": "1.0",
            "document_type": "project-estimate-manifest",
            "created_at": output["validated_at"],
            "validation_report": str(Path(args.output).resolve()),
            "inputs": output["inputs"],
        }
        write_json(args.manifest, manifest)
    status = "PASS" if report.ok else "FAIL"
    print(
        f"Input package validation {status}: "
        f"{len(report.errors)} error(s), {len(report.warnings)} warning(s). "
        f"Report: {Path(args.output).resolve()}"
    )
    return 0 if report.ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
