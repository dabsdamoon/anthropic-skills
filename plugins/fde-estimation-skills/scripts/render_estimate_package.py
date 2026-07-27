#!/usr/bin/env python3
"""Render Korean-first Markdown estimate documents from a canonical calculation."""

from __future__ import annotations

import argparse
from pathlib import Path
from typing import Any

from fde_estimation import load_structured


SCENARIO_LABELS = {
    "replacement-value": "전체 재조달 참고값",
    "remaining-work": "잔여 개발 견적",
    "change-adjustment": "추가 과업 조정 요청",
}


def parser() -> argparse.ArgumentParser:
    result = argparse.ArgumentParser()
    result.add_argument("--calculation", required=True)
    result.add_argument("--customer-baseline", required=True)
    result.add_argument("--field-discovery", required=True)
    result.add_argument("--as-built-evidence", required=True)
    result.add_argument("--scope-traceability", required=True)
    result.add_argument("--estimation-policy", required=True)
    result.add_argument("--output-dir", required=True)
    return result


def won(value: Any, currency: str) -> str:
    if isinstance(value, float) and not value.is_integer():
        number = f"{value:,.2f}"
    else:
        number = f"{int(value):,}"
    return f"{number} {currency}"


def marker(calculation: dict[str, Any]) -> str:
    return f"<!-- estimate-fingerprint:{calculation['fingerprint']} -->"


def signed_percent(value: Any) -> str:
    number = float(value)
    if number > 0:
        return f"+{number:g}%"
    return f"{number:g}%"


def write(path: Path, lines: list[str]) -> None:
    path.write_text("\n".join(lines).rstrip() + "\n", encoding="utf-8")


def summary_table(calculation: dict[str, Any]) -> list[str]:
    currency = calculation["currency"]
    lines = [
        "| 시나리오 | 성격 | 공수 | 공급가액 | 세금 | 합계 |",
        "|---|---|---:|---:|---:|---:|",
    ]
    for scenario in calculation["scenarios"]:
        lines.append(
            "| {scenario} | {label} | {effort} M/M | {supply} | {tax} | "
            "**{total}** |".format(
                scenario=scenario["scenario"],
                label=SCENARIO_LABELS[scenario["scenario"]],
                effort=scenario["effort_mm"],
                supply=won(scenario["supply_amount"], currency),
                tax=won(scenario["tax"], currency),
                total=won(scenario["total"], currency),
            )
        )
    return lines


def cell(value: Any) -> str:
    return str(value).replace("|", "\\|").replace("\n", " ")


def scenario_items(
    traceability: dict[str, Any],
    scenario_name: str,
) -> list[tuple[dict[str, Any], dict[str, Any]]]:
    result: list[tuple[dict[str, Any], dict[str, Any]]] = []
    for item in traceability["items"]:
        for allocation in item["allocations"]:
            if (
                allocation["scenario"] == scenario_name
                and allocation["include_in_estimate"]
            ):
                result.append((item, allocation))
    return result


def main() -> int:
    args = parser().parse_args()
    calculation = load_structured(args.calculation)
    customer = load_structured(args.customer_baseline)
    discovery = load_structured(args.field_discovery)
    as_built = load_structured(args.as_built_evidence)
    traceability = load_structured(args.scope_traceability)
    policy = load_structured(args.estimation_policy)
    output_dir = Path(args.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    project = calculation["project"]
    currency = calculation["currency"]

    estimate_lines = [
        f"# {project} 개산견적서",
        "",
        marker(calculation),
        "",
        "> 이 문서는 근거가 분리된 복수의 견적 시나리오를 제시한다. "
        "전체 재조달 가치, 잔여 작업, 추가 과업 조정은 서로 다른 "
        "상업적 질문이며 합산 청구액이 아니다.",
        "",
        "## 고객 목표",
        "",
        "| 목표 | 해결하려는 문제 | 기대 결과 |",
        "|---|---|---|",
    ]
    for outcome in customer["outcomes"]:
        estimate_lines.append(
            "| {title} | {problem} | {result} |".format(
                title=outcome["title"].replace("|", "\\|"),
                problem=outcome["problem"].replace("|", "\\|"),
                result=outcome["desired_result"].replace("|", "\\|"),
            )
        )
    estimate_lines.extend(
        [
        "",
        "## 견적 요약",
        "",
        *summary_table(calculation),
        "",
        "## 범위와 상태",
        "",
        "| 항목 | 분류 | 고객 확인 | 적용 시나리오 |",
        "|---|---|---|---|",
        ]
    )
    for item in traceability["items"]:
        included_scenarios = sorted(
            {
                allocation["scenario"]
                for allocation in item["allocations"]
                if allocation["include_in_estimate"]
            }
        )
        estimate_lines.append(
            "| {title} | {classification} | {confirmed} | {scenarios} |".format(
                title=item["title"].replace("|", "\\|"),
                classification=item["classification"],
                confirmed="예" if item["customer_confirmed"] else "아니오",
                scenarios=", ".join(included_scenarios) or "제외",
            )
        )
    success_measures = [
        measure
        for outcome in customer["outcomes"]
        for measure in outcome["success_measures"]
    ]
    assumptions = customer.get("assumptions") or []
    excluded_scope = [
        item for item in customer.get("explicit_scope", []) if not item["included"]
    ]
    unresolved_questions = traceability.get("unresolved_questions") or []
    estimate_lines.extend(
        [
        "",
        "## 인도 및 상업 조건",
        "",
        "- 일정: 정규 입력에는 확정 일정 전용 항목이 없다. 원문 제약사항과 "
        "계약서 또는 발주서에서 착수일·완료일을 서면 확정한다.",
        "- 지급: 정규 입력에는 확정 지급조건이 없다. 지급 시점과 조건은 "
        "계약 또는 발주 전에 별도로 확정한다.",
        "- 검수: 아래 고객 목표의 성공지표를 검수 기준 후보로 사용하며, "
        "최종 검수 기준은 계약 전에 확정한다.",
        "",
        "### 검수 기준 후보",
        "",
        ]
    )
    estimate_lines.extend(
        f"- {cell(measure)}" for measure in success_measures
    )
    if not success_measures:
        estimate_lines.append("- 기록된 성공지표 없음 — 계약 전 정의 필요")
    estimate_lines.extend(
        [
            "",
            "### 가정",
            "",
        ]
    )
    estimate_lines.extend(
        f"- {cell(item['description'])} "
        f"(출처 유형: `{item['provenance']['source_type']}`)"
        for item in assumptions
    )
    if not assumptions:
        estimate_lines.append("- 기록된 가정 없음")
    estimate_lines.extend(
        [
            "",
            "### 제외 범위",
            "",
        ]
    )
    estimate_lines.extend(
        f"- {cell(item['title'])}: {cell(item['description'])}"
        for item in excluded_scope
    )
    if not excluded_scope:
        estimate_lines.append(
            "- 명시된 제외 범위 없음 — 범위표의 `제외` 항목과 미결사항을 "
            "계약 전에 확인"
        )
    estimate_lines.extend(
        [
            "",
            "### 계약 전 결정사항",
            "",
        ]
    )
    estimate_lines.extend(
        f"- {cell(question)}" for question in unresolved_questions
    )
    if not unresolved_questions:
        estimate_lines.append("- 기록된 미결사항 없음")
    estimate_lines.extend(
        [
        "",
        "## 적용 원칙",
        "",
        "- `replacement-value`는 동일 제품을 다시 구축할 때의 참고 가치다.",
        "- `remaining-work`는 아직 완료하지 않은 후속 작업이다.",
        "- `change-adjustment`는 완료된 범위에 대한 서면 변경 협의 요청이다.",
        "- 제시 금액은 계약서, 승인 이력, 고객 제공사항과 함께 확정한다.",
        "",
        "## 유효성과 불확실성",
        "",
        f"- 산정 방식: {policy['estimation_method']['method']}",
        f"- 견적 유효기간: {policy['estimation_method']['validity_days']}일",
        "- 신뢰 범위: {low} ~ {high}".format(
            low=signed_percent(
                policy["estimation_method"]["confidence_low_percent"]
            ),
            high=signed_percent(
                policy["estimation_method"]["confidence_high_percent"]
            ),
        ),
        f"- 정책 유효기간: {policy['valid_from']} ~ {policy['valid_until']}",
        "",
        "본 개산견적은 법적 청약 또는 자동 확정된 추가금 권리가 아니다.",
        ]
    )
    write(output_dir / "budgetary-estimate.md", estimate_lines)

    basis_lines = [
        f"# {project} 견적산정근거서",
        "",
        marker(calculation),
        "",
        "## 산정 원칙",
        "",
        "- 고객의 명시 요구, 현장 관찰, FDE 추론, 고객 확인, 구현 증빙을 "
        "서로 다른 출처 유형으로 유지했다.",
        "- Git 기록은 구현 흔적이며 작업시간·사업가치·고객 승인의 증거로 "
        "단독 사용하지 않았다.",
        "- 각 시나리오는 독립 계산했으며 합산 청구액으로 표현하지 않았다.",
        "",
        "## 증빙 경계",
        "",
        f"- 최초 고객 원본: {len(customer['source_documents'])}개",
        f"- 현장 발견: {len(discovery['discoveries'])}개",
        f"- 솔루션 결정: {len(discovery['solution_decisions'])}개",
        f"- 구현 항목: {len(as_built['implementation_items'])}개",
        f"- Git 범위: {as_built['evidence_boundary']['revision']} "
        f"({as_built['git_evidence']['commit_count']} commits)",
        f"- Git fingerprint: `{as_built['git_evidence']['fingerprint']}`",
        "",
        "## 범위 조정",
        "",
        "| ID | 항목 | 분류 | 기준선 | 현장 발견 | 구현 증빙 |",
        "|---|---|---|---|---|---|",
    ]
    for item in traceability["items"]:
        basis_lines.append(
            "| {id} | {title} | {classification} | {baseline} | {discovery} | "
            "{implementation} |".format(
                id=item["id"],
                title=item["title"].replace("|", "\\|"),
                classification=item["classification"],
                baseline=", ".join(item["baseline_refs"]) or "—",
                discovery=", ".join(item["discovery_refs"]) or "—",
                implementation=", ".join(item["implementation_refs"]) or "—",
            )
        )
    basis_lines.extend(
        [
        "",
        "## 시나리오별 계산",
        "",
        ]
    )
    for scenario in calculation["scenarios"]:
        basis_lines.extend(
            [
                f"### {scenario['scenario']} — {SCENARIO_LABELS[scenario['scenario']]}",
                "",
                "| 범위 | 분류 | 역할 | 공수 | 월 단가 | 직접인건비 | 상태 |",
                "|---|---|---|---:|---:|---:|---|",
            ]
        )
        for line in scenario["lines"]:
            basis_lines.append(
                "| {scope} | {classification} | {role} | {effort} | {rate} | "
                "{direct} | {status} |".format(
                    scope=line["scope_title"].replace("|", "\\|"),
                    classification=line["classification"],
                    role=line["role_title"].replace("|", "\\|"),
                    effort=line["effort_mm"],
                    rate=won(line["monthly_rate"], currency),
                    direct=won(line["direct_labor"], currency),
                    status=line["commercial_status"],
                )
            )
        basis_lines.extend(
            [
                "",
                "| 구성 | 금액 |",
                "|---|---:|",
                f"| 직접인건비 | {won(scenario['direct_labor'], currency)} |",
                f"| 제경비 | {won(scenario['overhead'], currency)} |",
                f"| 기술료 | {won(scenario['technical_fee'], currency)} |",
                f"| 이윤 | {won(scenario['profit'], currency)} |",
                f"| 위험 준비금 | {won(scenario['risk'], currency)} |",
                "| 할인 | {discount} |".format(
                    discount=(
                        f"-{won(scenario['discount'], currency)}"
                        if scenario["discount"]
                        else won(0, currency)
                    )
                ),
                f"| 공급가액 | {won(scenario['supply_amount'], currency)} |",
                f"| 세금 | {won(scenario['tax'], currency)} |",
                f"| **합계** | **{won(scenario['total'], currency)}** |",
                "",
            ]
        )
    basis_lines.extend(
        [
            "## 산정 정책",
            "",
            f"- 통화: {policy['currency']}",
            f"- 공수 단위: {policy['estimation_method']['effort_unit']}",
            f"- 반올림: {policy['cost_rules']['rounding_unit']} "
            f"{policy['currency']} / {policy['cost_rules']['rounding_mode']}",
            f"- 세율: {policy['cost_rules']['tax_rate']}",
            "",
            "## 미해결 사항",
            "",
        ]
    )
    questions = traceability.get("unresolved_questions") or []
    basis_lines.extend(f"- {question}" for question in questions)
    if not questions:
        basis_lines.append("- 없음")
    write(output_dir / "basis-of-estimate.md", basis_lines)

    scenario_map = {
        scenario["scenario"]: scenario for scenario in calculation["scenarios"]
    }
    if "change-adjustment" in scenario_map:
        scenario = scenario_map["change-adjustment"]
        change_items = scenario_items(traceability, "change-adjustment")
        change_lines = [
            f"# {project} 추가 과업 조정 요청서",
            "",
            marker(calculation),
            "",
            "> 이 문서는 최초 범위와 실제 수행 범위의 차이를 서면으로 "
            "확인하고 계약금액 변경을 협의하기 위한 요청서다. 자동 확정된 "
            "법적 권리를 주장하지 않는다.",
            "",
            "## 최초 기준선과 수행 차이",
            "",
            "| 항목 | 분류 | 최초 기준선 | 현장 발견 | 구현 증빙 | 필요성 |",
            "|---|---|---|---|---|---|",
        ]
        for item, _allocation in change_items:
            change_lines.append(
                "| {title} | {classification} | {baseline} | {discovery} | "
                "{implementation} | {rationale} |".format(
                    title=cell(item["title"]),
                    classification=item["classification"],
                    baseline=", ".join(item["baseline_refs"]) or "—",
                    discovery=", ".join(item["discovery_refs"]) or "—",
                    implementation=", ".join(item["implementation_refs"]) or "—",
                    rationale=cell(item["rationale"]),
                )
            )
        change_lines.extend(
            [
                "",
                "## 증빙과 승인 경계",
                "",
                "| 항목 | 고객 범위 확인 | 승인 참조 | 상업 상태 |",
                "|---|---|---|---|",
            ]
        )
        for item, allocation in change_items:
            change_lines.append(
                "| {title} | {confirmed} | {approval} | {status} |".format(
                    title=cell(item["title"]),
                    confirmed="예" if item["customer_confirmed"] else "아니오",
                    approval=cell(item.get("approval_reference") or "없음"),
                    status=allocation["commercial_status"],
                )
            )
        change_lines.extend(
            [
                "",
                "- 고객의 범위 확인 또는 구현 증빙은 계약금액 변경 승인과 "
                "동일하지 않다.",
                "- `proposed` 항목은 금액과 계약 변경에 대한 별도 서면 합의가 "
                "필요하다.",
                "",
                "## 조정 요청 금액",
                "",
                f"- 공급가액: {won(scenario['supply_amount'], currency)}",
                f"- 세금: {won(scenario['tax'], currency)}",
                f"- 요청 합계: **{won(scenario['total'], currency)}**",
                f"- 공수: {scenario['effort_mm']} M/M",
                "",
                "세부 계산은 견적산정근거서를 따르며, 본 금액은 서면 변경 "
                "합의를 위한 제안이다.",
            ]
        )
        write(
            output_dir / "change-adjustment.md",
            change_lines,
        )
    if "remaining-work" in scenario_map:
        scenario = scenario_map["remaining-work"]
        remaining_items = scenario_items(traceability, "remaining-work")
        remaining_lines = [
            f"# {project} 후속 개발 견적서",
            "",
            marker(calculation),
            "",
            "> 이 문서는 아직 완료하지 않은 범위만을 대상으로 한다. 완료된 "
            "추가 과업은 별도 변경 협의에서 다룬다.",
            "",
            "## 후속 범위와 확인 상태",
            "",
            "| 항목 | 분류 | 고객 확인 | 구현 증빙 | 상업 상태 | 공수 | 비고 |",
            "|---|---|---|---|---|---:|---|",
        ]
        for item, allocation in remaining_items:
            remaining_lines.append(
                "| {title} | {classification} | {confirmed} | "
                "{implementation} | {status} | {effort} M/M | {note} |".format(
                    title=cell(item["title"]),
                    classification=item["classification"],
                    confirmed="예" if item["customer_confirmed"] else "아니오",
                    implementation=", ".join(item["implementation_refs"]) or "없음",
                    status=allocation["commercial_status"],
                    effort=allocation["effort_mm"],
                    note=cell(allocation["note"] or "—"),
                )
            )
        remaining_lines.extend(
            [
                "",
                "## 후속 개발 금액",
                "",
                f"- 공급가액: {won(scenario['supply_amount'], currency)}",
                f"- 세금: {won(scenario['tax'], currency)}",
                f"- 합계: **{won(scenario['total'], currency)}**",
                f"- 공수: {scenario['effort_mm']} M/M",
                "",
                "## 계약 전 확인",
                "",
                "- `future-option` 또는 고객 미확인 항목은 선택·승인 전에는 "
                "확정 범위가 아니다.",
                "- 일정, 검수 기준, 지급조건은 선택된 범위에 맞춰 계약 전에 "
                "서면 확정한다.",
            ]
        )
        write(
            output_dir / "remaining-work-estimate.md",
            remaining_lines,
        )
    generated = ["budgetary-estimate.md", "basis-of-estimate.md"]
    if "change-adjustment" in scenario_map:
        generated.append("change-adjustment.md")
    if "remaining-work" in scenario_map:
        generated.append("remaining-work-estimate.md")
    print(
        f"Rendered {len(generated)} Markdown report(s) in "
        f"{output_dir.resolve()}: {', '.join(generated)}"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
