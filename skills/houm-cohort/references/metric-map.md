# Metric derivability map

Worked against the Smart-NC mirror for a 44-metric cohort request (2026-08).
Tiers follow that request: Tier 1 lecture-critical, Tier 2 care characteristics,
Tier 3 curriculum extensions.

**No results are recorded here** — only whether a metric can be derived and, when
it cannot, why. Results belong in the response document for a specific window,
not in a skill, and not in a public repository before institutional publication
approval.

## Tier 1

| ID | Metric | Derivable | Source / reason |
|---|---|---|---|
| A01 | Cohort size | **Redefine** | Intent to deliver here is not a field. Substitute completed-delivery visits and say so. |
| A02 | Delivered as planned | **Lower bound** | Among mothers completing a full antenatal course who reached delivery timing. |
| A03 | Transfer, all | No | No transfer/referral code exists. Midwife handover is not digitised. |
| A04 | Transfer, emergency | No | As A03. |
| A05 | Primipara | No | Parity is not structured. |
| A06 | Multipara | No | As A05. |
| A07 | Caesarean, all | Yes | `O82*`, `O842` |
| A08 | Caesarean, elective | Yes | `O820`, after precedence against `O821` |
| A09 | Caesarean, emergency | Yes | `O821` |
| A10 | TOLAC attempted | No | Failed attempts are indistinguishable from planned repeat caesarean. |
| A11 | VBAC success | No | Denominator (A10) unavailable; `O757` count can exceed `O342*` count. |
| A12 | VBAC over all births | Yes | `O757` over delivery visits. Documentation ratio, not success rate. |
| A13 | Uterine rupture | Count only | `O71*`. No denominator without A10. |
| A14 | No perineal trauma | Yes, **do not compare** | No tear code and no episiotomy charge, over vaginal births. Coding-practice artefact — see SKILL.md. |
| A15 | 3° tear | Yes | `O702` over vaginal births |
| A16 | 4° tear | Yes | `O703` over vaginal births |
| A17 | Maternal death | Yes | `O95`–`O97` |
| A18 | Neonatal death | **Partial** | `P95` (stillbirth) only. Congenital-anomaly exclusion not possible; deaths occurring elsewhere never reach this EMR. |

## Tier 2

| ID | Metric | Derivable | Source / reason |
|---|---|---|---|
| B01 | Episiotomy | Yes | Procedure charge, over vaginal births |
| B02 | Induction | No | No structured induction marker |
| B03 | Oxytocin, augmentation | No | Cannot separate augmentation from third-stage prophylaxis. Report raw count in a note. |
| B04 | Epidural | Yes | Procedure charge |
| B05 | PPH > 500 mL | No | Estimated blood loss not recorded as a value. `O72*` diagnosis exists but carries no volume. |
| B06 | PPH ≥ 1000 mL | No | As B05 |
| B07–B09 | Delivery position | No | Not recorded |
| B10 | Water birth | Charge only | Under-counts if not separately billable |
| B11 | Cord clamping ≥ 60 s | No | Clamp time not recorded |
| B12 | Cord clamp time recorded | Yes | Reports as zero — which is the evidence for B11 being underivable |
| B13 | Phototherapy | No | Neonatal care not charged here |
| B14 | Skin-to-skin within 1 h | No | Not recorded |
| B15 | Breastfeeding initiated | No | Not recorded |
| B16 | Exclusive breastfeeding at 6 mo | No | No follow-up data |

## Tier 3

| ID | Metric | Derivable | Source / reason |
|---|---|---|---|
| C01 | 1:1 midwife assignment | No | Not structured |
| C02 | Doula present | No | Not recorded |
| C03 | Oral intake in labour | No | Not recorded |
| C04 | Preterm < 37 wk | No | Gestational age not structured. Threatened-preterm-labour codes are a diagnosis, not a delivery. |
| C05 | Pre-eclampsia | Yes | `O13`–`O15` |
| C06 | Twin vaginal birth | Yes | `O30*` denominator, vaginal flag numerator |
| C07 | Vaginal breech | Yes | `O801` |
| C08 | EPDS screened | No | Not structured. Intake-form responses exist only from 2025-04, so they cannot cover a five-year window. |
| C09 | EPDS positive | No | As C08 |
| C10 | Foreign national | No | **No nationality field on the patient table** |

## Where the gaps cluster

The metrics that would best characterise a midwifery-led model — delivery
position, 1:1 midwife assignment, doula presence, cord-clamping practice,
skin-to-skin — are precisely the ones a billing-oriented EMR does not capture.
That is a reportable finding in itself: what an institution measures reveals
what its record system was built to bill for.
