#!/usr/bin/env python3
"""Shared validation and calculation helpers for the FDE estimation plugin."""

from __future__ import annotations

import hashlib
import json
from dataclasses import dataclass, field
from datetime import datetime, timezone
from decimal import Decimal, ROUND_DOWN, ROUND_HALF_UP, ROUND_UP
from pathlib import Path
from typing import Any, Iterable


SCHEMA_VERSION = "1.0"
SOURCE_TYPES = {
    "customer_request",
    "observed",
    "inferred",
    "validated",
    "implemented",
}
CONFIDENCE_LEVELS = {"confirmed", "probable", "unverified"}
CLASSIFICATIONS = {
    "explicit-baseline",
    "derived-necessary",
    "field-validated",
    "supplier-initiated",
    "future-option",
    "unresolved",
}
SCENARIOS = {
    "replacement-value",
    "remaining-work",
    "change-adjustment",
}
ROUNDING = {
    "HALF_UP": ROUND_HALF_UP,
    "DOWN": ROUND_DOWN,
    "UP": ROUND_UP,
}
REVIEW_STATUSES = {"pending", "approved", "rejected"}
SENIORITY_LEVELS = {"entry", "junior", "senior"}
RATE_SOURCE_TYPES = {
    "kosa",
    "government-statistics",
    "salary-survey",
    "job-posting",
    "customer-policy",
}
RATE_METHODS = {"kosa-seniority", "web-estimate", "customer-provided"}
WEB_RATE_SOURCE_TYPES = {
    "government-statistics",
    "salary-survey",
    "job-posting",
}


@dataclass
class ValidationReport:
    errors: list[str] = field(default_factory=list)
    warnings: list[str] = field(default_factory=list)

    @property
    def ok(self) -> bool:
        return not self.errors

    def error(self, message: str) -> None:
        self.errors.append(message)

    def warn(self, message: str) -> None:
        self.warnings.append(message)

    def as_dict(self) -> dict[str, Any]:
        return {
            "ok": self.ok,
            "errors": self.errors,
            "warnings": self.warnings,
        }


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()


def load_structured(path: str | Path) -> dict[str, Any]:
    source = Path(path)
    text = source.read_text(encoding="utf-8")
    try:
        value = json.loads(text)
    except json.JSONDecodeError as json_error:
        try:
            import yaml  # type: ignore
        except ImportError as import_error:
            raise ValueError(
                f"{source}: expected JSON-compatible YAML; install PyYAML for "
                "general YAML syntax"
            ) from import_error
        try:
            value = yaml.safe_load(text)
        except Exception as yaml_error:
            raise ValueError(f"{source}: invalid JSON/YAML: {json_error}") from yaml_error
    if not isinstance(value, dict):
        raise ValueError(f"{source}: top-level value must be an object")
    return value


def write_json(path: str | Path, value: Any) -> None:
    target = Path(path)
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(
        json.dumps(value, ensure_ascii=False, indent=2, sort_keys=False) + "\n",
        encoding="utf-8",
    )


def canonical_json(value: Any) -> str:
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":"))


def fingerprint(value: Any) -> str:
    return hashlib.sha256(canonical_json(value).encode("utf-8")).hexdigest()


def file_fingerprint(path: str | Path) -> str:
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def decimal(value: Any) -> Decimal:
    return Decimal(str(value))


def round_money(value: Decimal, unit: int, mode: str) -> Decimal:
    if unit <= 0:
        raise ValueError("rounding_unit must be positive")
    rounding = ROUNDING.get(mode)
    if rounding is None:
        raise ValueError(f"unsupported rounding mode: {mode}")
    decimal_unit = Decimal(unit)
    return (value / decimal_unit).quantize(Decimal("1"), rounding=rounding) * decimal_unit


def money_number(value: Decimal) -> int | float:
    integral = value.to_integral_value()
    if value == integral:
        return int(integral)
    return float(value)


def _require(
    obj: dict[str, Any],
    required: Iterable[str],
    path: str,
    report: ValidationReport,
) -> None:
    for key in required:
        if key not in obj:
            report.error(f"{path}: missing required field '{key}'")


def _validate_ids(
    values: Any,
    path: str,
    report: ValidationReport,
) -> set[str]:
    if not isinstance(values, list):
        report.error(f"{path}: must be an array")
        return set()
    seen: set[str] = set()
    for index, item in enumerate(values):
        item_path = f"{path}[{index}]"
        if not isinstance(item, dict):
            report.error(f"{item_path}: must be an object")
            continue
        item_id = item.get("id")
        if not isinstance(item_id, str) or not item_id:
            report.error(f"{item_path}.id: must be a non-empty string")
            continue
        if item_id in seen:
            report.error(f"{path}: duplicate id '{item_id}'")
        seen.add(item_id)
    return seen


def _iter_provenance(value: Any, path: str = "$") -> Iterable[tuple[str, Any]]:
    if isinstance(value, dict):
        for key, child in value.items():
            child_path = f"{path}.{key}"
            if key == "provenance":
                yield child_path, child
            yield from _iter_provenance(child, child_path)
    elif isinstance(value, list):
        for index, child in enumerate(value):
            yield from _iter_provenance(child, f"{path}[{index}]")


def _validate_provenance(
    document: dict[str, Any],
    final: bool,
    report: ValidationReport,
) -> None:
    required = {
        "source_type",
        "source_reference",
        "captured_at",
        "confidence",
        "customer_confirmed",
        "evidence",
    }
    for path, provenance in _iter_provenance(document):
        if not isinstance(provenance, dict):
            report.error(f"{path}: must be an object")
            continue
        missing = required - set(provenance)
        for key in sorted(missing):
            report.error(f"{path}: missing required field '{key}'")
        source_type = provenance.get("source_type")
        if source_type not in SOURCE_TYPES:
            report.error(f"{path}.source_type: unsupported value '{source_type}'")
        confidence = provenance.get("confidence")
        if confidence not in CONFIDENCE_LEVELS:
            report.error(f"{path}.confidence: unsupported value '{confidence}'")
        if not isinstance(provenance.get("customer_confirmed"), bool):
            report.error(f"{path}.customer_confirmed: must be boolean")
        evidence = provenance.get("evidence")
        if not isinstance(evidence, list):
            report.error(f"{path}.evidence: must be an array")
        elif final and not evidence:
            report.error(f"{path}.evidence: final artifacts require at least one reference")
        if source_type == "inferred" and provenance.get("customer_confirmed"):
            report.warn(
                f"{path}: inferred claim is customer-confirmed; prefer a separate "
                "validated record pointing to the inference"
            )


def _validate_document_header(
    document: dict[str, Any],
    expected_type: str,
    final: bool,
    report: ValidationReport,
) -> None:
    if document.get("schema_version") != SCHEMA_VERSION:
        report.error(
            f"{expected_type}: schema_version must be '{SCHEMA_VERSION}', got "
            f"'{document.get('schema_version')}'"
        )
    if document.get("document_type") != expected_type:
        report.error(
            f"{expected_type}: document_type must be '{expected_type}', got "
            f"'{document.get('document_type')}'"
        )
    if document.get("status") not in {"draft", "final"}:
        report.error(f"{expected_type}: status must be draft or final")
    if final and document.get("status") != "final":
        report.error(f"{expected_type}: --final requires status 'final'")


def _validate_human_review(
    document: dict[str, Any],
    document_type: str,
    final: bool,
    report: ValidationReport,
) -> None:
    path = f"{document_type}.review"
    review = document.get("review")
    if not isinstance(review, dict):
        if final:
            report.error(f"{path}: final artifact requires approved human review")
        else:
            report.error(f"{path}: must be an object")
        return

    status = review.get("status")
    if status not in REVIEW_STATUSES:
        report.error(f"{path}.status: unsupported value '{status}'")
    if not final:
        return
    if status != "approved":
        report.error(f"{path}: final artifact requires approved human review")
        return
    for field_name in ("reviewed_by", "reviewed_at", "reference"):
        value = review.get(field_name)
        if not isinstance(value, str) or not value.strip():
            report.error(
                f"{path}.{field_name}: approved human review requires "
                "a non-empty value"
            )


def validate_customer_baseline(
    document: dict[str, Any],
    final: bool,
    report: ValidationReport,
) -> dict[str, set[str]]:
    _validate_document_header(document, "customer-baseline", final, report)
    _validate_human_review(document, "customer-baseline", final, report)
    _require(
        document,
        [
            "project",
            "source_documents",
            "outcomes",
            "explicit_scope",
            "constraints",
            "assumptions",
            "approvals",
        ],
        "customer-baseline",
        report,
    )
    source_ids = _validate_ids(
        document.get("source_documents"), "customer-baseline.source_documents", report
    )
    outcome_ids = _validate_ids(
        document.get("outcomes"), "customer-baseline.outcomes", report
    )
    scope_ids = _validate_ids(
        document.get("explicit_scope"), "customer-baseline.explicit_scope", report
    )
    _validate_ids(document.get("constraints"), "customer-baseline.constraints", report)
    _validate_ids(document.get("assumptions"), "customer-baseline.assumptions", report)
    _validate_ids(document.get("approvals"), "customer-baseline.approvals", report)
    for index, outcome in enumerate(document.get("outcomes") or []):
        if isinstance(outcome, dict):
            _require(
                outcome,
                [
                    "id",
                    "title",
                    "problem",
                    "desired_result",
                    "users",
                    "success_measures",
                    "provenance",
                ],
                f"customer-baseline.outcomes[{index}]",
                report,
            )
    for index, scope in enumerate(document.get("explicit_scope") or []):
        if isinstance(scope, dict):
            _require(
                scope,
                ["id", "title", "description", "included", "provenance"],
                f"customer-baseline.explicit_scope[{index}]",
                report,
            )
    if final and not source_ids:
        report.error("customer-baseline.source_documents: final artifact cannot be empty")
    if final and not outcome_ids:
        report.error("customer-baseline.outcomes: final artifact cannot be empty")
    _validate_provenance(document, final, report)
    return {"sources": source_ids, "outcomes": outcome_ids, "scope": scope_ids}


def validate_field_discovery(
    document: dict[str, Any],
    final: bool,
    report: ValidationReport,
    outcome_ids: set[str] | None = None,
) -> dict[str, set[str]]:
    _validate_document_header(document, "field-discovery", final, report)
    _validate_human_review(document, "field-discovery", final, report)
    _require(
        document,
        ["project", "discoveries", "solution_decisions", "open_questions"],
        "field-discovery",
        report,
    )
    discovery_ids = _validate_ids(
        document.get("discoveries"), "field-discovery.discoveries", report
    )
    decision_ids = _validate_ids(
        document.get("solution_decisions"),
        "field-discovery.solution_decisions",
        report,
    )
    _validate_ids(
        document.get("open_questions"), "field-discovery.open_questions", report
    )
    for index, discovery in enumerate(document.get("discoveries") or []):
        if not isinstance(discovery, dict):
            continue
        _require(
            discovery,
            [
                "id",
                "title",
                "statement",
                "affected_outcome_ids",
                "validation_status",
                "provenance",
            ],
            f"field-discovery.discoveries[{index}]",
            report,
        )
        for ref in discovery.get("affected_outcome_ids") or []:
            if outcome_ids is not None and ref not in outcome_ids:
                report.error(
                    f"field-discovery.discoveries[{index}]: unknown outcome ref '{ref}'"
                )
    for index, decision in enumerate(document.get("solution_decisions") or []):
        if not isinstance(decision, dict):
            continue
        _require(
            decision,
            [
                "id",
                "title",
                "discovery_ids",
                "selected_solution",
                "alternatives",
                "rationale",
                "status",
                "provenance",
            ],
            f"field-discovery.solution_decisions[{index}]",
            report,
        )
        for ref in decision.get("discovery_ids") or []:
            if ref not in discovery_ids:
                report.error(
                    f"field-discovery.solution_decisions[{index}]: "
                    f"unknown discovery ref '{ref}'"
                )
    if final and not discovery_ids:
        report.error("field-discovery.discoveries: final artifact cannot be empty")
    _validate_provenance(document, final, report)
    return {"discoveries": discovery_ids, "decisions": decision_ids}


def validate_as_built(
    document: dict[str, Any],
    final: bool,
    report: ValidationReport,
    outcome_ids: set[str] | None = None,
    decision_ids: set[str] | None = None,
) -> dict[str, set[str]]:
    _validate_document_header(document, "as-built-evidence", final, report)
    _require(
        document,
        [
            "project",
            "evidence_boundary",
            "git_evidence",
            "implementation_items",
            "limitations",
        ],
        "as-built-evidence",
        report,
    )
    implementation_ids = _validate_ids(
        document.get("implementation_items"),
        "as-built-evidence.implementation_items",
        report,
    )
    for index, item in enumerate(document.get("implementation_items") or []):
        if not isinstance(item, dict):
            continue
        _require(
            item,
            [
                "id",
                "title",
                "description",
                "delivery_status",
                "change_type",
                "related_outcome_ids",
                "related_decision_ids",
                "verification",
                "provenance",
            ],
            f"as-built-evidence.implementation_items[{index}]",
            report,
        )
        for ref in item.get("related_outcome_ids") or []:
            if outcome_ids is not None and ref not in outcome_ids:
                report.error(
                    f"as-built-evidence.implementation_items[{index}]: "
                    f"unknown outcome ref '{ref}'"
                )
        for ref in item.get("related_decision_ids") or []:
            if decision_ids is not None and ref not in decision_ids:
                report.error(
                    f"as-built-evidence.implementation_items[{index}]: "
                    f"unknown decision ref '{ref}'"
                )
    git_evidence = document.get("git_evidence")
    if not isinstance(git_evidence, dict):
        report.error("as-built-evidence.git_evidence: must be an object")
    else:
        _require(
            git_evidence,
            [
                "head",
                "commit_count",
                "first_commit_at",
                "last_commit_at",
                "fingerprint",
                "commits",
            ],
            "as-built-evidence.git_evidence",
            report,
        )
    if final and not implementation_ids:
        report.error(
            "as-built-evidence.implementation_items: final artifact cannot be empty"
        )
    _validate_provenance(document, final, report)
    return {"implementation": implementation_ids}


def validate_estimation_policy(
    document: dict[str, Any],
    final: bool,
    report: ValidationReport,
) -> dict[str, set[str]]:
    _validate_document_header(document, "estimation-policy", final, report)
    _validate_human_review(document, "estimation-policy", final, report)
    _require(
        document,
        [
            "currency",
            "locale",
            "valid_from",
            "valid_until",
            "rate_sources",
            "roles",
            "cost_rules",
            "estimation_method",
        ],
        "estimation-policy",
        report,
    )
    source_ids = _validate_ids(
        document.get("rate_sources"), "estimation-policy.rate_sources", report
    )
    source_by_id: dict[str, dict[str, Any]] = {}
    role_ids = _validate_ids(document.get("roles"), "estimation-policy.roles", report)
    for index, source in enumerate(document.get("rate_sources") or []):
        if not isinstance(source, dict):
            continue
        path = f"estimation-policy.rate_sources[{index}]"
        _require(
            source,
            [
                "id",
                "title",
                "publisher",
                "location",
                "retrieved_at",
                "source_type",
                "seniority_levels",
                "compensation_scope",
            ],
            path,
            report,
        )
        source_id = source.get("id")
        if isinstance(source_id, str) and source_id:
            source_by_id[source_id] = source
        for field_name in (
            "title",
            "publisher",
            "location",
            "retrieved_at",
            "compensation_scope",
        ):
            value = source.get(field_name)
            if not isinstance(value, str) or not value.strip():
                report.error(f"{path}.{field_name}: must be a non-empty string")
        source_type = source.get("source_type")
        if source_type not in RATE_SOURCE_TYPES:
            report.error(f"{path}.source_type: unsupported value '{source_type}'")
        levels = source.get("seniority_levels")
        if not isinstance(levels, list):
            report.error(f"{path}.seniority_levels: must be an array")
        else:
            for level in levels:
                if level not in SENIORITY_LEVELS:
                    report.error(
                        f"{path}.seniority_levels: unsupported value '{level}'"
                    )
    for index, role in enumerate(document.get("roles") or []):
        if not isinstance(role, dict):
            continue
        path = f"estimation-policy.roles[{index}]"
        _require(
            role,
            [
                "id",
                "title",
                "occupation",
                "seniority",
                "seniority_confirmed",
                "monthly_rate",
                "rate_method",
                "source_ids",
                "rate_evidence",
                "rate_rationale",
            ],
            path,
            report,
        )
        seniority = role.get("seniority")
        if seniority not in SENIORITY_LEVELS:
            report.error(f"{path}.seniority: unsupported value '{seniority}'")
        for field_name in ("title", "occupation", "rate_rationale"):
            value = role.get(field_name)
            if not isinstance(value, str) or not value.strip():
                report.error(f"{path}.{field_name}: must be a non-empty string")
        seniority_confirmed = role.get("seniority_confirmed")
        if not isinstance(seniority_confirmed, bool):
            report.error(f"{path}.seniority_confirmed: must be boolean")
            if final:
                report.error(
                    f"{path}: final policy requires user-confirmed seniority"
                )
        elif final and not seniority_confirmed:
            report.error(f"{path}: final policy requires user-confirmed seniority")
        rate_method = role.get("rate_method")
        if rate_method not in RATE_METHODS:
            report.error(f"{path}.rate_method: unsupported value '{rate_method}'")
        role_source_ids = role.get("source_ids")
        referenced_sources: list[dict[str, Any]] = []
        role_source_id_set: set[str] = set()
        if not isinstance(role_source_ids, list):
            report.error(f"{path}.source_ids: must be an array")
        else:
            if final and not role_source_ids:
                report.error(f"{path}.source_ids: final role requires a rate source")
            for source_id in role_source_ids:
                if not isinstance(source_id, str) or not source_id:
                    report.error(
                        f"{path}.source_ids: references must be non-empty strings"
                    )
                    continue
                if source_id in role_source_id_set:
                    report.error(f"{path}.source_ids: duplicate source reference")
                    continue
                role_source_id_set.add(source_id)
                source = source_by_id.get(source_id)
                if source is None:
                    report.error(f"{path}: unknown rate source '{source_id}'")
                else:
                    referenced_sources.append(source)
        rate_evidence = role.get("rate_evidence")
        evidence_source_ids: set[str] = set()
        if not isinstance(rate_evidence, list):
            report.error(f"{path}.rate_evidence: must be an array")
        else:
            for evidence_index, evidence in enumerate(rate_evidence):
                evidence_path = f"{path}.rate_evidence[{evidence_index}]"
                if not isinstance(evidence, dict):
                    report.error(f"{evidence_path}: must be an object")
                    continue
                _require(
                    evidence,
                    [
                        "source_id",
                        "observed_value",
                        "observed_unit",
                        "normalized_monthly_rate",
                        "normalization_note",
                    ],
                    evidence_path,
                    report,
                )
                evidence_source_id = evidence.get("source_id")
                if evidence_source_id in evidence_source_ids:
                    report.error(
                        f"{evidence_path}.source_id: duplicate evidence source"
                    )
                if isinstance(evidence_source_id, str):
                    evidence_source_ids.add(evidence_source_id)
                if evidence_source_id not in role_source_id_set:
                    report.error(
                        f"{evidence_path}.source_id: must appear in role source_ids"
                    )
                if evidence.get("observed_unit") not in {
                    "monthly",
                    "annual",
                    "daily",
                    "hourly",
                }:
                    report.error(
                        f"{evidence_path}.observed_unit: unsupported value "
                        f"'{evidence.get('observed_unit')}'"
                    )
                note = evidence.get("normalization_note")
                if not isinstance(note, str) or not note.strip():
                    report.error(
                        f"{evidence_path}.normalization_note: must be "
                        "a non-empty string"
                    )
                for amount_field in ("observed_value", "normalized_monthly_rate"):
                    try:
                        if decimal(evidence.get(amount_field)) < 0:
                            report.error(
                                f"{evidence_path}.{amount_field}: cannot be negative"
                            )
                    except Exception:
                        report.error(
                            f"{evidence_path}.{amount_field}: must be numeric"
                        )
            if final and evidence_source_ids != role_source_id_set:
                report.error(
                    f"{path}.rate_evidence: final role requires one normalized "
                    "observation for every cited source"
                )
        if rate_method == "kosa-seniority":
            kosa_matches = [
                source
                for source in referenced_sources
                if source.get("source_type") == "kosa"
                and seniority in (source.get("seniority_levels") or [])
            ]
            if not kosa_matches:
                report.error(
                    f"{path}: kosa-seniority requires a KOSA source that "
                    f"explicitly covers seniority '{seniority}'"
                )
        elif rate_method == "web-estimate":
            web_matches = [
                source
                for source in referenced_sources
                if source.get("source_type") in WEB_RATE_SOURCE_TYPES
                and seniority in (source.get("seniority_levels") or [])
            ]
            if not web_matches:
                report.error(
                    f"{path}: web-estimate requires a dated web source that "
                    f"covers seniority '{seniority}'"
                )
            elif not any(
                source.get("source_type") == "government-statistics"
                for source in web_matches
            ):
                publishers = {
                    source.get("publisher")
                    for source in web_matches
                    if source.get("publisher")
                }
                if len(publishers) < 2:
                    report.error(
                        f"{path}: web-estimate without government statistics "
                        "requires two independent publishers"
                    )
        elif rate_method == "customer-provided":
            if not any(
                source.get("source_type") == "customer-policy"
                and seniority in (source.get("seniority_levels") or [])
                for source in referenced_sources
            ):
                report.error(
                    f"{path}: customer-provided requires a customer-policy "
                    f"source that covers seniority '{seniority}'"
                )
        try:
            if decimal(role.get("monthly_rate")) < 0:
                report.error(f"{path}.monthly_rate: cannot be negative")
        except Exception:
            report.error(f"{path}.monthly_rate: must be numeric")
    rules = document.get("cost_rules")
    if not isinstance(rules, dict):
        report.error("estimation-policy.cost_rules: must be an object")
    else:
        required_rates = [
            "overhead_rate_on_direct",
            "technical_fee_rate_on_direct_plus_overhead",
            "profit_rate_on_cost",
            "risk_rate_on_cost",
            "discount_rate",
            "tax_rate",
        ]
        _require(
            rules,
            required_rates + ["rounding_unit", "rounding_mode"],
            "estimation-policy.cost_rules",
            report,
        )
        for key in required_rates:
            try:
                rate = decimal(rules.get(key))
                if rate < 0:
                    report.error(f"estimation-policy.cost_rules.{key}: cannot be negative")
                if key in {"discount_rate", "tax_rate"} and rate > 1:
                    report.error(
                        f"estimation-policy.cost_rules.{key}: cannot exceed 1"
                    )
            except Exception:
                report.error(f"estimation-policy.cost_rules.{key}: must be numeric")
        if rules.get("rounding_mode") not in ROUNDING:
            report.error("estimation-policy.cost_rules.rounding_mode: unsupported mode")
        try:
            if int(rules.get("rounding_unit")) < 1:
                raise ValueError
        except Exception:
            report.error(
                "estimation-policy.cost_rules.rounding_unit: must be a positive integer"
            )
    method = document.get("estimation_method")
    if isinstance(method, dict):
        low = decimal(method.get("confidence_low_percent", 0))
        high = decimal(method.get("confidence_high_percent", 0))
        if low > high:
            report.error(
                "estimation-policy.estimation_method: confidence low exceeds high"
            )
    if final and not role_ids:
        report.error("estimation-policy.roles: final artifact cannot be empty")
    return {"rate_sources": source_ids, "roles": role_ids}


def validate_traceability(
    document: dict[str, Any],
    final: bool,
    report: ValidationReport,
    baseline_ids: set[str] | None = None,
    discovery_ids: set[str] | None = None,
    implementation_ids: set[str] | None = None,
    role_ids: set[str] | None = None,
) -> dict[str, set[str]]:
    _validate_document_header(document, "scope-traceability", final, report)
    _validate_human_review(document, "scope-traceability", final, report)
    _require(
        document,
        ["project", "items", "unresolved_questions"],
        "scope-traceability",
        report,
    )
    item_ids = _validate_ids(
        document.get("items"), "scope-traceability.items", report
    )
    for index, item in enumerate(document.get("items") or []):
        if not isinstance(item, dict):
            continue
        _require(
            item,
            [
                "id",
                "title",
                "classification",
                "rationale",
                "customer_confirmed",
                "baseline_refs",
                "discovery_refs",
                "implementation_refs",
                "allocations",
            ],
            f"scope-traceability.items[{index}]",
            report,
        )
        classification = item.get("classification")
        if classification not in CLASSIFICATIONS:
            report.error(
                f"scope-traceability.items[{index}].classification: "
                f"unsupported value '{classification}'"
            )
        if classification == "explicit-baseline" and not item.get("baseline_refs"):
            report.error(
                f"scope-traceability.items[{index}]: explicit-baseline requires "
                "a baseline reference"
            )
        if classification == "field-validated":
            if not item.get("discovery_refs"):
                report.error(
                    f"scope-traceability.items[{index}]: field-validated requires "
                    "a discovery reference"
                )
            if not item.get("customer_confirmed"):
                report.error(
                    f"scope-traceability.items[{index}]: field-validated requires "
                    "customer_confirmed"
                )
        if (
            classification in {"supplier-initiated", "unresolved"}
            and item.get("customer_confirmed")
        ):
            report.warn(
                f"scope-traceability.items[{index}]: consider field-validated "
                "classification for a customer-confirmed item"
            )
        refs_and_known = [
            ("baseline_refs", baseline_ids),
            ("discovery_refs", discovery_ids),
            ("implementation_refs", implementation_ids),
        ]
        for field_name, known_ids in refs_and_known:
            refs = item.get(field_name)
            if not isinstance(refs, list):
                report.error(
                    f"scope-traceability.items[{index}].{field_name}: must be an array"
                )
                continue
            if known_ids is not None:
                for ref in refs:
                    if ref not in known_ids:
                        report.error(
                            f"scope-traceability.items[{index}].{field_name}: "
                            f"unknown ref '{ref}'"
                        )
        allocations = item.get("allocations")
        if not isinstance(allocations, list):
            report.error(
                f"scope-traceability.items[{index}].allocations: must be an array"
            )
            continue
        allocation_keys: set[tuple[Any, Any]] = set()
        for alloc_index, allocation in enumerate(allocations):
            path = f"scope-traceability.items[{index}].allocations[{alloc_index}]"
            if not isinstance(allocation, dict):
                report.error(f"{path}: must be an object")
                continue
            _require(
                allocation,
                [
                    "scenario",
                    "role_id",
                    "effort_mm",
                    "commercial_status",
                    "include_in_estimate",
                    "note",
                ],
                path,
                report,
            )
            scenario = allocation.get("scenario")
            if scenario not in SCENARIOS:
                report.error(f"{path}.scenario: unsupported value '{scenario}'")
            role_id = allocation.get("role_id")
            allocation_key = (scenario, role_id)
            if allocation_key in allocation_keys:
                report.error(
                    f"{path}: duplicate role/scenario allocation for '{role_id}' "
                    f"and '{scenario}'"
                )
            allocation_keys.add(allocation_key)
            if role_ids is not None and role_id not in role_ids:
                report.error(f"{path}.role_id: unknown role '{role_id}'")
            try:
                if decimal(allocation.get("effort_mm")) < 0:
                    report.error(f"{path}.effort_mm: cannot be negative")
            except Exception:
                report.error(f"{path}.effort_mm: must be numeric")
            commercial_status = allocation.get("commercial_status")
            if commercial_status not in {
                "reference-only",
                "proposed",
                "confirmed",
                "excluded",
            }:
                report.error(
                    f"{path}.commercial_status: unsupported value "
                    f"'{commercial_status}'"
                )
            if (
                scenario == "change-adjustment"
                and commercial_status == "confirmed"
                and not item.get("approval_reference")
            ):
                report.error(
                    f"{path}: confirmed change-adjustment requires approval_reference"
                )
            if (
                scenario == "change-adjustment"
                and allocation.get("include_in_estimate")
                and classification in {"supplier-initiated", "unresolved"}
            ):
                report.warn(
                    f"{path}: {classification} change-adjustment must remain a "
                    "proposal unless independently approved"
                )
            if scenario == "change-adjustment" and classification == "future-option":
                report.error(
                    f"{path}: future-option cannot be a completed "
                    "change-adjustment"
                )
            if (
                allocation.get("commercial_status") == "excluded"
                and allocation.get("include_in_estimate")
            ):
                report.error(
                    f"{path}: excluded allocation cannot enter the estimate"
                )
    if final and not item_ids:
        report.error("scope-traceability.items: final artifact cannot be empty")
    return {"trace_items": item_ids}


def project_name(document: dict[str, Any]) -> str | None:
    project = document.get("project")
    if isinstance(project, dict):
        name = project.get("name")
        return name if isinstance(name, str) else None
    if isinstance(project, str):
        return project
    return None


def validate_package(
    customer: dict[str, Any] | None = None,
    discovery: dict[str, Any] | None = None,
    as_built: dict[str, Any] | None = None,
    policy: dict[str, Any] | None = None,
    traceability: dict[str, Any] | None = None,
    final: bool = False,
) -> ValidationReport:
    report = ValidationReport()
    baseline_ids: set[str] | None = None
    outcome_ids: set[str] | None = None
    discovery_ids: set[str] | None = None
    decision_ids: set[str] | None = None
    implementation_ids: set[str] | None = None
    role_ids: set[str] | None = None
    documents = [
        item
        for item in (customer, discovery, as_built, policy, traceability)
        if item is not None
    ]
    names = {name for doc in documents if (name := project_name(doc))}
    if len(names) > 1:
        report.error(f"package project names do not match: {sorted(names)}")
    if customer is not None:
        ids = validate_customer_baseline(customer, final, report)
        baseline_ids = ids["scope"] | ids["outcomes"]
        outcome_ids = ids["outcomes"]
    if discovery is not None:
        ids = validate_field_discovery(discovery, final, report, outcome_ids)
        discovery_ids = ids["discoveries"]
        decision_ids = ids["decisions"]
    if as_built is not None:
        ids = validate_as_built(
            as_built,
            final,
            report,
            outcome_ids=outcome_ids,
            decision_ids=decision_ids,
        )
        implementation_ids = ids["implementation"]
    if policy is not None:
        ids = validate_estimation_policy(policy, final, report)
        role_ids = ids["roles"]
    if traceability is not None:
        validate_traceability(
            traceability,
            final,
            report,
            baseline_ids=baseline_ids,
            discovery_ids=discovery_ids,
            implementation_ids=implementation_ids,
            role_ids=role_ids,
        )
    return report


def calculate_scenarios(
    traceability: dict[str, Any],
    policy: dict[str, Any],
) -> list[dict[str, Any]]:
    role_map = {role["id"]: role for role in policy["roles"]}
    rules = policy["cost_rules"]
    unit = int(rules["rounding_unit"])
    mode = str(rules["rounding_mode"])
    scenario_rows: dict[str, list[dict[str, Any]]] = {}
    for item in traceability["items"]:
        for allocation in item["allocations"]:
            if not allocation["include_in_estimate"]:
                continue
            role = role_map[allocation["role_id"]]
            effort = decimal(allocation["effort_mm"])
            rate = decimal(role["monthly_rate"])
            scenario_rows.setdefault(allocation["scenario"], []).append(
                {
                    "scope_item_id": item["id"],
                    "scope_title": item["title"],
                    "classification": item["classification"],
                    "role_id": role["id"],
                    "role_title": role["title"],
                    "role_occupation": role["occupation"],
                    "role_seniority": role["seniority"],
                    "rate_method": role["rate_method"],
                    "rate_source_ids": role["source_ids"],
                    "effort_mm": money_number(effort),
                    "monthly_rate": money_number(rate),
                    "direct_labor": money_number(round_money(effort * rate, unit, mode)),
                    "commercial_status": allocation["commercial_status"],
                    "note": allocation.get("note", ""),
                }
            )

    results: list[dict[str, Any]] = []
    for scenario in sorted(scenario_rows):
        lines = scenario_rows[scenario]
        direct = sum(decimal(line["direct_labor"]) for line in lines)
        overhead = round_money(
            direct * decimal(rules["overhead_rate_on_direct"]), unit, mode
        )
        technical_base = direct + overhead
        technical = round_money(
            technical_base
            * decimal(rules["technical_fee_rate_on_direct_plus_overhead"]),
            unit,
            mode,
        )
        cost = direct + overhead + technical
        profit = round_money(cost * decimal(rules["profit_rate_on_cost"]), unit, mode)
        risk = round_money(
            (cost + profit) * decimal(rules["risk_rate_on_cost"]), unit, mode
        )
        pre_discount = cost + profit + risk
        discount = round_money(
            pre_discount * decimal(rules["discount_rate"]), unit, mode
        )
        supply = pre_discount - discount
        tax = round_money(supply * decimal(rules["tax_rate"]), unit, mode)
        total = supply + tax
        results.append(
            {
                "scenario": scenario,
                "effort_mm": money_number(
                    sum(decimal(line["effort_mm"]) for line in lines)
                ),
                "direct_labor": money_number(direct),
                "overhead": money_number(overhead),
                "technical_fee": money_number(technical),
                "profit": money_number(profit),
                "risk": money_number(risk),
                "discount": money_number(discount),
                "supply_amount": money_number(supply),
                "tax": money_number(tax),
                "total": money_number(total),
                "lines": lines,
            }
        )
    return results
