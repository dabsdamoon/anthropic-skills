---
name: houm-cohort
description: Derive obstetric cohort and quality metrics (delivery mode, caesarean rate, VBAC, perineal trauma, intervention rates) from the Houm Smart-NC mirror over an arbitrary date window, with the denominator rules and coding caveats that make the numbers defensible. Use when asked for 분만 통계, 제왕절개율, VBAC, 회음 열상, 코호트 지표, The Farm 비교, lecture or audit evidence from the EMR, or when filling a cohort data request for external presentation.
---

# Houm cohort metrics

Derive obstetric outcome metrics from the Smart-NC mirror (`smart_rpa.db`) for a
date window. The queries are the easy part. **The reason this skill exists is the
set of traps between a query result and a number you can defend in front of
clinicians** — every one of them below was hit in practice, not anticipated.

Aggregate output only. Never select name, chart number, RRN, or birth date.
Mask any cell under 5 as `<5` before it leaves the machine.

## The denominator problem — read before anything else

A request will usually ask for **"all mothers who booked antenatal care here and
planned to deliver here, transfers included."** That is the methodologically
correct denominator, and it is **not derivable from a single-institution EMR.**

- Intent to deliver here is not a structured field.
- A mother who transfers **delivers elsewhere**, so no delivery record ever
  reaches this EMR. She is invisible by construction.
- Transfer itself is not coded. Check before promising: search the diagnosis
  codes for transfer/referral concepts over the window. In this EMR the answer
  has been zero.

Say this plainly rather than substituting a denominator that looks similar.
What you **can** offer:

| Instead of | Offer | Framing |
|---|---|---|
| Mothers planning to deliver here | Visits where a delivery completed | Rename the metric; state the substitution |
| Transfer rate | Bounded share who delivered elsewhere | **Upper bound**, never a transfer rate |
| "% delivered as planned" | Same, among mothers who completed a full antenatal course | **Lower bound** |

### The upper bound, and why it usually cannot be published

`transferred < (antenatal cohort) − (delivered here)`. True, but the raw
difference mixes in ongoing pregnancies, single-visit patients, pregnancy loss,
and mothers who simply chose another hospital. Tighten it by excluding
pregnancy-loss codes, requiring the antenatal course to have ended early enough
that a delivery would have been recorded, and requiring a minimum number of
antenatal visits.

**Then sweep the visit threshold and look at whether it converges.** In practice
it does not — the answer moves several-fold from a 1-visit floor to a 12-visit
floor, because the threshold *is* the definition of "was this mother ours". A
figure that swings that far on an arbitrary cut is not a statistic.

Report the sweep, not a single number, and state the direction of the error. The
bound sits **above** the true transfer rate, so placing it beside a published
transfer rate from another cohort misrepresents the clinic **unfavourably**.
That failure mode is easy to miss when everyone is watching for numbers that
flatter.

The statement that does survive: among mothers who completed a full antenatal
course and reached delivery timing, the share who delivered here — a lower bound
on "delivered as planned", because some of the remainder chose to leave.

## Counting a delivery

A birth is **one visit**, not one diagnosis row. Several diagnosis rows are
routinely recorded for a single birth.

```sql
-- a visit is a birth if any attached diagnosis is a completed delivery
SUBSTR(code,1,3) IN ('O80','O81','O82','O83','O84') OR code = 'O757'
```

**Group on the full four-column visit key** — `(organization_id,
customer_number, insurance_seq_no, medical_clinic_seq_no)`. A looser key bleeds
across insurance sequences and silently changes the count.

Report both the visit count and the distinct-mother count. They differ, and
which one the requester wants is usually unstated.

## Check the era before quoting a cumulative total

Delivery volume and coding practice can both shift under you. Before honouring a
"since opening" window, run delivery visits per year **and** visits-per-mother
per year.

A visits-per-mother ratio well above 1 means the delivery code was also being
applied to postpartum follow-ups, so counts from that era are inflated relative
to a later era where the ratio sits near 1. Two eras with different ratios
cannot share a definition. Recommend the later window and say why — a cumulative
figure spanning both is the first thing an external reviewer will pull apart.

## Code map

| Concept | Codes |
|---|---|
| Delivery (any) | `O80*`–`O84*`, `O757` |
| Caesarean | `O82*`, `O842` |
| Caesarean, elective / emergency | `O820` / `O821` |
| Vaginal | `O80*`, `O840`, `O841`, `O81*`, `O83*`, `O757` |
| Assisted vaginal | `O81*`, `O83*`, `O841` |
| VBAC (successful) | `O757` |
| Prior caesarean scar | `O342*` |
| Perineal tear, 1–4° | `O700`, `O701`, `O702`, `O703` |
| Postpartum haemorrhage | `O72*` |
| Uterine rupture | `O71*` |
| Maternal death | `O95`–`O97` |
| Stillbirth | `P95` |
| Pre-eclampsia | `O13`–`O15` |
| Multiple gestation | `O30*` |
| Vaginal breech | `O801` |
| Antenatal supervision (cohort marker) | `Z34*`, `Z35*` |
| Pregnancy loss (exclude from bounds) | `O00`–`O08` |

Caesarean subtypes **overlap** — a visit can carry both `O820` and `O821`. Apply
a precedence rule (emergency wins) so the subtypes partition the total, and say
in the notes how many were resolved that way.

Procedures are **not** diagnoses. Episiotomy, epidural, and oxytocin come from
the prescription/charge table by order name, not from `diagnoses`.

## Traps that produce wrong-but-plausible numbers

**Perineal trauma is not comparable across record systems.** A "no trauma" rate
derived here counts visits with no tear code *and* no episiotomy charge. It will
look far worse than a midwife-record cohort, because a billing EMR codes 2°
tears routinely to justify the repair charge. Check the 2° coding rate; if it is
high, the gap is a coding artefact, not a clinical one. Recommend dropping the
comparison rather than footnoting it.

**Denominators built from `O342*` can be smaller than their own numerator.**
Successful-VBAC coding (`O757`) and prior-scar coding (`O342*`) are applied
inconsistently, so a VBAC "success rate" can exceed 100%. When it does, do not
pick a different denominator — report TOLAC metrics as underivable and flag the
contradiction as the finding.

**TOLAC attempts that failed are invisible.** A mother who laboured and
converted to caesarean is coded as a caesarean with a prior scar,
indistinguishable from a planned repeat. Any TOLAC denominator is a guess.

**Oxytocin cannot be split by purpose.** Third-stage prophylaxis is routine, so
a raw oxytocin count is not an augmentation rate. Leave the metric blank and
report the raw count in a note instead.

**Charge-derived process measures under-count.** Water birth, delivery position,
and similar only appear if they carry a billable line. A near-zero result means
"not separately charged", not "not done". Say which it is, or say you cannot
tell.

**Absence of a code is not absence of the event.** For anything reported as zero,
state whether the event would have been recorded here at all — neonatal
outcomes, for instance, may sit in another institution's record entirely.

## Reporting

- Give **numerator and denominator**, never a ratio alone. The same ratio means
  different things under different denominators, and the requester needs to print
  the denominator beside it.
- Blank beats estimated. A blank cell with `EMR에 구조화 저장하지 않음` is
  actionable — it names the next measurement gap. An estimate is not.
- Name the denominator per metric. Perineal metrics sit on vaginal births, not
  all births. VBAC-over-all-births and VBAC-over-prior-caesarean are different
  numbers with the same name.
- State the mirror sync time. Reference tables (`std_*`) affect name lookups
  only; counts come from `diagnoses`, `medical_clinics`, and `prescriptions`, so
  a stale reference table does not invalidate a count — but say so rather than
  leaving the reader to wonder.

`references/metric-map.md` carries the per-metric derivability table for the
2026 cohort request, including which items were blank and the reason for each.

`scripts/derive_cohort_metrics.py` computes the derivable set for a window.
Run it against a copy of the mirror; it opens the SQLite file read-only through
DuckDB and prints an aggregate table with `<5` masking applied.
