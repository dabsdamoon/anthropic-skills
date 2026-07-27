from __future__ import annotations

import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


PLUGIN_DIR = Path(__file__).resolve().parents[1]
SCRIPTS = PLUGIN_DIR / "scripts"
FIXTURES = Path(__file__).resolve().parent / "fixtures"


def run_script(name: str, *args: object) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [sys.executable, str(SCRIPTS / name), *(str(value) for value in args)],
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )


class EstimateWorkflowTests(unittest.TestCase):
    def test_final_policy_requires_user_confirmed_seniority_for_every_role(
        self,
    ) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            output = Path(temporary)
            policy = json.loads((FIXTURES / "estimation-policy.yaml").read_text())
            policy["roles"][0].pop("seniority_confirmed", None)
            policy_path = output / "unconfirmed-seniority-policy.json"
            policy_path.write_text(json.dumps(policy), encoding="utf-8")

            result = run_script(
                "validate_input_package.py",
                "--estimation-policy",
                policy_path,
                "--final",
                "--output",
                output / "verification.json",
            )

            self.assertNotEqual(result.returncode, 0)
            verification = json.loads((output / "verification.json").read_text())
            self.assertTrue(
                any(
                    "requires user-confirmed seniority" in error
                    for error in verification["errors"]
                )
            )

    def test_kosa_aggregate_cannot_stand_in_for_a_seniority_rate(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            output = Path(temporary)
            policy = json.loads((FIXTURES / "estimation-policy.yaml").read_text())
            policy["rate_sources"] = [
                {
                    "id": "RATE-KOSA",
                    "title": "KOSA aggregate occupation average",
                    "publisher": "KOSA",
                    "location": "fixture://kosa-aggregate",
                    "retrieved_at": "2026-01-01",
                    "source_type": "kosa",
                    "seniority_levels": [],
                    "compensation_scope": "Employer labor cost",
                }
            ]
            role = policy["roles"][0]
            role.update(
                {
                    "occupation": "Business analysis",
                    "seniority": "junior",
                    "seniority_confirmed": True,
                    "rate_method": "kosa-seniority",
                    "source_id": "RATE-KOSA",
                    "source_ids": ["RATE-KOSA"],
                    "rate_evidence": [
                        {
                            "source_id": "RATE-KOSA",
                            "observed_value": 1000,
                            "observed_unit": "monthly",
                            "normalized_monthly_rate": 1000,
                            "normalization_note": "No seniority breakdown.",
                        }
                    ],
                    "rate_rationale": "Use the published occupation average.",
                }
            )
            policy["roles"] = [role]
            policy_path = output / "kosa-aggregate-policy.json"
            policy_path.write_text(json.dumps(policy), encoding="utf-8")

            result = run_script(
                "validate_input_package.py",
                "--estimation-policy",
                policy_path,
                "--final",
                "--output",
                output / "verification.json",
            )

            self.assertNotEqual(result.returncode, 0)
            verification = json.loads((output / "verification.json").read_text())
            self.assertTrue(
                any(
                    "KOSA source that explicitly covers seniority" in error
                    for error in verification["errors"]
                )
            )

    def test_final_human_owned_artifacts_require_approved_review(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            output = Path(temporary)
            cases = [
                ("customer-baseline", "customer-baseline.json"),
                ("field-discovery", "field-discovery.json"),
                ("estimation-policy", "estimation-policy.yaml"),
                ("scope-traceability", "scope-traceability.json"),
            ]
            for option, fixture_name in cases:
                with self.subTest(document_type=option):
                    unreviewed = json.loads((FIXTURES / fixture_name).read_text())
                    unreviewed.pop("review")
                    unreviewed_path = output / f"unreviewed-{option}.json"
                    unreviewed_path.write_text(
                        json.dumps(unreviewed),
                        encoding="utf-8",
                    )
                    verification_path = output / f"{option}-verification.json"

                    result = run_script(
                        "validate_input_package.py",
                        f"--{option}",
                        unreviewed_path,
                        "--final",
                        "--output",
                        verification_path,
                    )

                    self.assertNotEqual(result.returncode, 0)
                    verification = json.loads(verification_path.read_text())
                    self.assertTrue(
                        any(
                            "requires approved human review" in error
                            for error in verification["errors"]
                        )
                    )

    def test_all_skills_use_the_shared_interactive_review_protocol(self) -> None:
        protocol_path = PLUGIN_DIR / "references" / "interactive-review-protocol.md"
        protocol = protocol_path.read_text()
        for gate in range(6):
            self.assertIn(f"GATE-{gate}", protocol)

        skill_paths = sorted((PLUGIN_DIR / "skills").glob("*/SKILL.md"))
        self.assertEqual(len(skill_paths), 6)
        for skill_path in skill_paths:
            with self.subTest(skill=skill_path.parent.name):
                self.assertIn(
                    "../../references/interactive-review-protocol.md",
                    skill_path.read_text(),
                )
        policy_skill = (
            PLUGIN_DIR / "skills" / "define-estimation-policy" / "SKILL.md"
        ).read_text()
        self.assertIn(
            "../../references/workforce-rate-source-rules.md",
            policy_skill,
        )
        for marker in ("entry", "junior", "senior", "KOSA", "web evidence"):
            self.assertIn(marker, policy_skill)

    def test_git_collector_creates_draft_without_author_email_or_effort_claim(
        self,
    ) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            repo = root / "repo"
            repo.mkdir()
            subprocess.run(["git", "-C", str(repo), "init", "-q"], check=True)
            subprocess.run(
                ["git", "-C", str(repo), "config", "user.name", "Fixture Author"],
                check=True,
            )
            subprocess.run(
                [
                    "git",
                    "-C",
                    str(repo),
                    "config",
                    "user.email",
                    "fixture@example.com",
                ],
                check=True,
            )
            (repo / "README.md").write_text("# Fixture\n", encoding="utf-8")
            subprocess.run(
                ["git", "-C", str(repo), "add", "README.md"],
                check=True,
            )
            subprocess.run(
                ["git", "-C", str(repo), "commit", "-q", "-m", "Initial fixture"],
                check=True,
            )
            output = root / "as-built-evidence.json"
            result = run_script(
                "collect_git_evidence.py",
                "--repo",
                repo,
                "--project-name",
                "Temporary Product",
                "--output",
                output,
            )
            self.assertEqual(result.returncode, 0, result.stderr)
            data = json.loads(output.read_text())
            self.assertEqual(data["status"], "draft")
            self.assertEqual(data["git_evidence"]["commit_count"], 1)
            self.assertEqual(data["implementation_items"], [])
            self.assertNotIn("fixture@example.com", output.read_text())
            self.assertTrue(
                any("not hours" in limitation for limitation in data["limitations"])
            )

    def test_scope_renderer_preserves_traceability_fingerprint(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            output = Path(temporary)
            markdown = output / "scope-traceability.md"
            verification = output / "scope-verification.json"
            result = run_script(
                "build_scope_traceability.py",
                "--traceability",
                FIXTURES / "scope-traceability.json",
                "--customer-baseline",
                FIXTURES / "customer-baseline.json",
                "--field-discovery",
                FIXTURES / "field-discovery.json",
                "--as-built-evidence",
                FIXTURES / "as-built-evidence.json",
                "--estimation-policy",
                FIXTURES / "estimation-policy.yaml",
                "--final",
                "--output-md",
                markdown,
                "--verification",
                verification,
            )
            self.assertEqual(result.returncode, 0, result.stderr)
            report = json.loads(verification.read_text())
            self.assertTrue(report["ok"])
            self.assertIn(
                f"<!-- scope-fingerprint:{report['fingerprint']} -->",
                markdown.read_text(),
            )

    def test_valid_package_calculates_independent_scenarios_and_verifies_reports(
        self,
    ) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            output = Path(temporary)
            validation = output / "input-verification.json"
            result = run_script(
                "validate_input_package.py",
                "--customer-baseline",
                FIXTURES / "customer-baseline.json",
                "--field-discovery",
                FIXTURES / "field-discovery.json",
                "--as-built-evidence",
                FIXTURES / "as-built-evidence.json",
                "--estimation-policy",
                FIXTURES / "estimation-policy.yaml",
                "--scope-traceability",
                FIXTURES / "scope-traceability.json",
                "--final",
                "--output",
                validation,
            )
            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertTrue(json.loads(validation.read_text())["ok"])

            calculation = output / "estimate-calculation.json"
            result = run_script(
                "calculate_estimate.py",
                "--scope-traceability",
                FIXTURES / "scope-traceability.json",
                "--estimation-policy",
                FIXTURES / "estimation-policy.yaml",
                "--generated-at",
                "2026-01-05T00:00:00Z",
                "--output",
                calculation,
                "--verification",
                output / "calculation-verification.json",
            )
            self.assertEqual(result.returncode, 0, result.stderr)
            data = json.loads(calculation.read_text())
            totals = {
                scenario["scenario"]: scenario["total"]
                for scenario in data["scenarios"]
            }
            self.assertEqual(
                totals,
                {
                    "change-adjustment": 2200,
                    "remaining-work": 1100,
                    "replacement-value": 1100,
                },
            )

            result = run_script(
                "render_estimate_package.py",
                "--calculation",
                calculation,
                "--customer-baseline",
                FIXTURES / "customer-baseline.json",
                "--field-discovery",
                FIXTURES / "field-discovery.json",
                "--as-built-evidence",
                FIXTURES / "as-built-evidence.json",
                "--scope-traceability",
                FIXTURES / "scope-traceability.json",
                "--estimation-policy",
                FIXTURES / "estimation-policy.yaml",
                "--output-dir",
                output,
            )
            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertIn(
                "See consolidated results",
                (output / "budgetary-estimate.md").read_text(),
            )
            self.assertIn(
                "fixture-fingerprint",
                (output / "basis-of-estimate.md").read_text(),
            )
            basis_text = (output / "basis-of-estimate.md").read_text()
            self.assertIn("## 인력 구성 및 단가 근거", basis_text)
            self.assertIn("junior", basis_text)
            self.assertIn("senior", basis_text)
            self.assertIn("web-estimate", basis_text)
            self.assertIn("Fixture KOSA", basis_text)
            self.assertIn("Aggregate occupation cross-check only", basis_text)
            budgetary_text = (output / "budgetary-estimate.md").read_text()
            self.assertIn("## 인도 및 상업 조건", budgetary_text)
            self.assertIn("approved sample reconciles", budgetary_text)
            self.assertIn("Confirm the commercial treatment", budgetary_text)
            change_text = (output / "change-adjustment.md").read_text()
            self.assertIn("## 최초 기준선과 수행 차이", change_text)
            self.assertIn("decision-2026-01-03", change_text)
            self.assertIn("계약금액 변경 승인과 동일하지 않다", change_text)
            remaining_text = (output / "remaining-work-estimate.md").read_text()
            self.assertIn("## 후속 범위와 확인 상태", remaining_text)
            self.assertIn("future-option", remaining_text)
            self.assertIn("구현 증빙", remaining_text)
            result = run_script(
                "verify_estimate_package.py",
                "--calculation",
                calculation,
                "--output-dir",
                output,
                "--output",
                output / "package-verification.json",
            )
            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertTrue(
                json.loads((output / "package-verification.json").read_text())["ok"]
            )

    def test_unknown_reference_fails_at_public_validation_boundary(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            output = Path(temporary)
            invalid = json.loads(
                (FIXTURES / "scope-traceability.json").read_text()
            )
            invalid["items"][0]["baseline_refs"] = ["OUT-DOES-NOT-EXIST"]
            invalid_path = output / "invalid-traceability.json"
            invalid_path.write_text(json.dumps(invalid), encoding="utf-8")
            result = run_script(
                "validate_input_package.py",
                "--customer-baseline",
                FIXTURES / "customer-baseline.json",
                "--field-discovery",
                FIXTURES / "field-discovery.json",
                "--as-built-evidence",
                FIXTURES / "as-built-evidence.json",
                "--estimation-policy",
                FIXTURES / "estimation-policy.yaml",
                "--scope-traceability",
                invalid_path,
                "--final",
                "--output",
                output / "verification.json",
            )
            self.assertNotEqual(result.returncode, 0)
            verification = json.loads((output / "verification.json").read_text())
            self.assertTrue(
                any("unknown ref" in error for error in verification["errors"])
            )

    def test_confirmed_change_requires_approval_reference(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            output = Path(temporary)
            invalid = json.loads(
                (FIXTURES / "scope-traceability.json").read_text()
            )
            change_item = invalid["items"][2]
            change_item.pop("approval_reference")
            change_item["allocations"][0]["commercial_status"] = "confirmed"
            invalid_path = output / "unapproved-confirmed-change.json"
            invalid_path.write_text(json.dumps(invalid), encoding="utf-8")
            result = run_script(
                "validate_input_package.py",
                "--estimation-policy",
                FIXTURES / "estimation-policy.yaml",
                "--scope-traceability",
                invalid_path,
                "--final",
                "--output",
                output / "verification.json",
            )
            self.assertNotEqual(result.returncode, 0)
            verification = json.loads((output / "verification.json").read_text())
            self.assertTrue(
                any(
                    "requires approval_reference" in error
                    for error in verification["errors"]
                )
            )

    def test_duplicate_role_scenario_allocation_is_rejected(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            output = Path(temporary)
            invalid = json.loads(
                (FIXTURES / "scope-traceability.json").read_text()
            )
            duplicate = dict(invalid["items"][0]["allocations"][0])
            invalid["items"][0]["allocations"].append(duplicate)
            invalid_path = output / "duplicate-allocation.json"
            invalid_path.write_text(json.dumps(invalid), encoding="utf-8")
            result = run_script(
                "validate_input_package.py",
                "--estimation-policy",
                FIXTURES / "estimation-policy.yaml",
                "--scope-traceability",
                invalid_path,
                "--final",
                "--output",
                output / "verification.json",
            )
            self.assertNotEqual(result.returncode, 0)
            verification = json.loads((output / "verification.json").read_text())
            self.assertTrue(
                any(
                    "duplicate role/scenario allocation" in error
                    for error in verification["errors"]
                )
            )

    def test_report_verifier_detects_tampered_total(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            output = Path(temporary)
            calculation = output / "estimate-calculation.json"
            result = run_script(
                "calculate_estimate.py",
                "--scope-traceability",
                FIXTURES / "scope-traceability.json",
                "--estimation-policy",
                FIXTURES / "estimation-policy.yaml",
                "--output",
                calculation,
                "--verification",
                output / "calculation-verification.json",
            )
            self.assertEqual(result.returncode, 0, result.stderr)
            result = run_script(
                "render_estimate_package.py",
                "--calculation",
                calculation,
                "--customer-baseline",
                FIXTURES / "customer-baseline.json",
                "--field-discovery",
                FIXTURES / "field-discovery.json",
                "--as-built-evidence",
                FIXTURES / "as-built-evidence.json",
                "--scope-traceability",
                FIXTURES / "scope-traceability.json",
                "--estimation-policy",
                FIXTURES / "estimation-policy.yaml",
                "--output-dir",
                output,
            )
            self.assertEqual(result.returncode, 0, result.stderr)
            budgetary = output / "budgetary-estimate.md"
            budgetary.write_text(
                budgetary.read_text().replace("2,200 KRW", "9,999 KRW"),
                encoding="utf-8",
            )
            result = run_script(
                "verify_estimate_package.py",
                "--calculation",
                calculation,
                "--output-dir",
                output,
                "--output",
                output / "package-verification.json",
            )
            self.assertNotEqual(result.returncode, 0)
            verification = json.loads(
                (output / "package-verification.json").read_text()
            )
            self.assertTrue(
                any("missing change-adjustment total" in error for error in verification["errors"])
            )

    def test_calculator_rejects_package_with_no_included_scenario(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            output = Path(temporary)
            traceability = json.loads(
                (FIXTURES / "scope-traceability.json").read_text()
            )
            for item in traceability["items"]:
                for allocation in item["allocations"]:
                    allocation["include_in_estimate"] = False
            traceability_path = output / "empty-estimate.json"
            traceability_path.write_text(
                json.dumps(traceability),
                encoding="utf-8",
            )
            result = run_script(
                "calculate_estimate.py",
                "--scope-traceability",
                traceability_path,
                "--estimation-policy",
                FIXTURES / "estimation-policy.yaml",
                "--output",
                output / "estimate-calculation.json",
                "--verification",
                output / "calculation-verification.json",
            )
            self.assertNotEqual(result.returncode, 0)
            verification = json.loads(
                (output / "calculation-verification.json").read_text()
            )
            self.assertTrue(
                any("no allocations" in error for error in verification["errors"])
            )


if __name__ == "__main__":
    unittest.main()
