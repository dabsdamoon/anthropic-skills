# Houm Operational Document Typography

Read this reference when creating or editing Korean or bilingual PDFs, InDesign files, forms, checklists, agreements, or other operational documents.

## Keep Evidence Types Separate

- Treat the 2019 brand-book fonts in `SKILL.md` as the canonical brand identity.
- Treat fonts embedded in maintained `houm-documentation` artifacts as production evidence, not as a retroactive change to the brand book.
- Follow a repository-local design handoff when it explicitly defines typography.
- Preserve an existing document's font metrics unless the user requests a redesign; font substitution can change line breaks, table height, and pagination.

## Observed Production Families

| Artifact family | Observed fonts | How to use the evidence |
|---|---|---|
| Korean/English reception references | **Noto Sans CJK KR Regular/Bold** | Prefer for new dense Korean or bilingual operational documents when no local template says otherwise. One family covers Hangul and Latin consistently. |
| Admission-diagnosis and formal legacy forms | **Adobe Myungjo Std Medium**, often with **Sanchez** | Preserve when editing those templates. Do not make Adobe Myungjo the default for a new document merely because it appears in legacy output. |
| English birth checklists and glucose logs | **Sanchez** headings with **Arial** labels/body | Preserve for existing English templates. For a new brand-led artifact, follow the canonical Sanchez/Noto Sans pairing instead of copying Arial automatically. |
| Early font previews | Nanum Gothic Bold, BM Hanna Air, Times New Roman | Treat as exploratory or historical evidence, not approved defaults. |

Evidence was inspected from these maintained `houm-documentation` outputs:

- `indd/dba_reception_reference_PROOF.pdf` and `indd/dba_reception_reference_en_PROOF.pdf`
- `indd/admission_diagnosis_remark_260702_v2_PROOF.pdf`
- `indd/direct_billing_agreement_PROOF.pdf`
- `indd/birth_procedure_checklist_PROOF.pdf` and `indd/gdm_blood_sugar_log_PROOF.pdf`
- `sample/checklists/PREVIEW_brand-font.pdf` and `sample/checklists/PREVIEW_times-new-roman.pdf`

## Selection Rules

1. For a new Korean or bilingual clinical/admin form, use **Noto Sans CJK KR** for headings, labels, tables, and body unless a maintained template specifies another family.
2. For branded editorial collateral, use the canonical pairing from `SKILL.md`: Sanchez with Nanum Myeongjo for primary copy, and Noto Sans with KoPub Dotum for secondary copy.
3. For an existing formal document using Adobe Myungjo, preserve it when the authoring environment is licensed and the exported PDF embeds it correctly. Do not redistribute the font file.
4. For a digital product UI, follow the product repository's design system first. Do not import print-document fonts into the UI without an explicit decision.
5. In dense bilingual layouts, prefer a family that covers both scripts, such as Noto Sans CJK KR, to reduce baseline and width mismatch.
6. Keep the `Houm` wordmark and any explicitly branded English title in Sanchez even when surrounding operational text uses Noto Sans CJK KR.

## Recommended Fallbacks

```css
:root {
  --font-ko-operational: "Noto Sans CJK KR", "Noto Sans KR", Pretendard, system-ui, sans-serif;
  --font-ko-formal: "Adobe Myungjo Std", "Nanum Myeongjo", "Noto Serif KR", serif;
}
```

Use fallbacks only when substitution is acceptable. For fixed-layout print files, install the intended font or stop and report the missing-font dependency rather than silently reflowing the document.

## Delivery Checks

Before delivering a PDF or print artifact:

1. Run the authoring application's missing-font and overset-text preflight.
2. Inspect the exported PDF with `pdffonts output.pdf` when Poppler is available.
3. Confirm every intended family is embedded or subset-embedded and no unexpected fallback appears.
4. Visually inspect Hangul glyphs, Latin/Hangul baselines, bold weights, table wrapping, page breaks, and form-field alignment.
5. Record any unavoidable substitution in the handoff instead of presenting it as the original typography.
