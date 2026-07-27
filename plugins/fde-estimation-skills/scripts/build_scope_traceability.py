#!/usr/bin/env python3
"""Validate and render an agent-authored scope traceability artifact."""

from __future__ import annotations

import argparse
from collections import Counter
from pathlib import Path

from fde_estimation import fingerprint, load_structured, validate_package, write_json


def parser() -> argparse.ArgumentParser:
    result = argparse.ArgumentParser()
    result.add_argument("--traceability", required=True)
    result.add_argument("--customer-baseline")
    result.add_argument("--field-discovery")
    result.add_argument("--as-built-evidence")
    result.add_argument("--estimation-policy")
    result.add_argument("--final", action="store_true")
    result.add_argument("--output-md", required=True)
    result.add_argument("--verification", required=True)
    return result


def escape(value: object) -> str:
    return str(value).replace("|", "\\|").replace("\n", " ")


def main() -> int:
    args = parser().parse_args()
    traceability = load_structured(args.traceability)
    customer = load_structured(args.customer_baseline) if args.customer_baseline else None
    discovery = load_structured(args.field_discovery) if args.field_discovery else None
    as_built = load_structured(args.as_built_evidence) if args.as_built_evidence else None
    policy = load_structured(args.estimation_policy) if args.estimation_policy else None
    report = validate_package(
        customer=customer,
        discovery=discovery,
        as_built=as_built,
        policy=policy,
        traceability=traceability,
        final=args.final,
    )
    artifact_fingerprint = fingerprint(traceability)
    classifications = Counter(
        item["classification"] for item in traceability.get("items", [])
    )
    scenarios = Counter(
        allocation["scenario"]
        for item in traceability.get("items", [])
        for allocation in item.get("allocations", [])
        if allocation.get("include_in_estimate")
    )
    lines = [
        f"# {traceability.get('project', {}).get('name', '')} 범위 추적표",
        "",
        f"<!-- scope-fingerprint:{artifact_fingerprint} -->",
        "",
        "## 분류 요약",
        "",
        "| 분류 | 항목 수 |",
        "|---|---:|",
    ]
    for classification in sorted(classifications):
        lines.append(f"| {classification} | {classifications[classification]} |")
    lines.extend(
        [
            "",
            "## 시나리오 배정 요약",
            "",
            "| 시나리오 | 배정 수 |",
            "|---|---:|",
        ]
    )
    for scenario in sorted(scenarios):
        lines.append(f"| {scenario} | {scenarios[scenario]} |")
    lines.extend(
        [
            "",
            "## 요구사항–발견–구현 추적",
            "",
            "| ID | 항목 | 분류 | 고객 확인 | 기준선 | 현장 발견 | 구현 증빙 |",
            "|---|---|---|---|---|---|---|",
        ]
    )
    for item in traceability.get("items", []):
        lines.append(
            "| {id} | {title} | {classification} | {confirmed} | {baseline} | "
            "{discovery} | {implementation} |".format(
                id=escape(item["id"]),
                title=escape(item["title"]),
                classification=escape(item["classification"]),
                confirmed="예" if item["customer_confirmed"] else "아니오",
                baseline=escape(", ".join(item["baseline_refs"]) or "—"),
                discovery=escape(", ".join(item["discovery_refs"]) or "—"),
                implementation=escape(", ".join(item["implementation_refs"]) or "—"),
            )
        )
    lines.extend(["", "## 미해결 질문", ""])
    questions = traceability.get("unresolved_questions") or []
    lines.extend(f"- {question}" for question in questions)
    if not questions:
        lines.append("- 없음")
    Path(args.output_md).write_text("\n".join(lines) + "\n", encoding="utf-8")
    write_json(
        args.verification,
        {
            "fingerprint": artifact_fingerprint,
            "classifications": dict(classifications),
            "scenarios": dict(scenarios),
            **report.as_dict(),
        },
    )
    status = "PASS" if report.ok else "FAIL"
    print(
        f"Scope traceability {status}: {len(traceability.get('items', []))} "
        f"item(s). Markdown: {Path(args.output_md).resolve()}"
    )
    return 0 if report.ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
