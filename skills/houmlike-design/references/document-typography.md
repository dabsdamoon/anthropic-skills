# Houm Operational Document Typography

Read this when creating or editing Korean or bilingual PDFs, InDesign files, forms, checklists, agreements, or other operational documents.

Documents are not screens. A fixed-layout print file cannot reflow, so a font substitution that is harmless on the web changes line breaks, table height, and pagination here.

## Keep evidence types separate

- Treat the 2019 brand-book fonts in `SKILL.md` as the canonical brand identity.
- Treat fonts embedded in maintained `houm-documentation` artifacts as production evidence, not as a retroactive change to the brand book.
- Follow a repository-local design handoff when it explicitly defines typography.
- Preserve an existing document's font metrics unless the user requests a redesign.

## Observed production families

| Artifact family | Observed fonts | How to use the evidence |
|---|---|---|
| Korean/English reference sheets | **Noto Sans CJK KR Regular/Bold** | Prefer for new dense Korean or bilingual operational documents when no local template says otherwise. One family covers Hangul and Latin consistently. |
| Formal legacy forms | **Adobe Myungjo Std Medium**, often with **Sanchez** | Preserve when editing those templates. Do not make Adobe Myungjo the default for a new document merely because it appears in legacy output. |
| English checklists and logs | **Sanchez** headings with **Arial** labels/body | Preserve for existing English templates. For a new brand-led artifact, follow the canonical Sanchez / Noto Sans pairing instead of copying Arial automatically. |
| Early font previews | Nanum Gothic Bold, BM Hanna Air, Times New Roman | Exploratory or historical evidence, not approved defaults. |

Evidence was inspected from these maintained `houm-documentation` outputs:

- `indd/dba_reception_reference_PROOF.pdf` and `indd/dba_reception_reference_en_PROOF.pdf`
- `indd/admission_diagnosis_remark_260702_v2_PROOF.pdf`
- `indd/direct_billing_agreement_PROOF.pdf`
- `indd/birth_procedure_checklist_PROOF.pdf` and `indd/gdm_blood_sugar_log_PROOF.pdf`
- `sample/checklists/PREVIEW_brand-font.pdf` and `sample/checklists/PREVIEW_times-new-roman.pdf`

## Selection rules

1. For a new Korean or bilingual operational form, use **Noto Sans CJK KR** for headings, labels, tables, and body unless a maintained template specifies another family.
2. For branded editorial collateral, use the canonical pairing from `SKILL.md`: Sanchez with Nanum Myeongjo for primary copy, Noto Sans with Pretendard for secondary copy.
3. For an existing formal document using Adobe Myungjo, preserve it when the authoring environment is licensed and the exported PDF embeds it correctly. Do not redistribute the font file.
4. For a digital product UI, follow the product repository's design system first. Do not import print-document fonts into a UI without an explicit decision.
5. In dense bilingual layouts, prefer a family that covers both scripts — Noto Sans CJK KR or Pretendard — to avoid baseline and width mismatch on every mixed line.
6. Keep the `Houm` wordmark and any explicitly branded English title in Sanchez even when surrounding operational text uses Noto Sans CJK KR.
7. **Sanchez has one weight (400) and no bold.** Where a document calls for a bold slab heading, substitute Roboto Slab and record the substitution.

## Line breaking still applies

InDesign and most PDF renderers will break Korean between syllable blocks by default, exactly as browsers do. Set the composer to break on 어절 boundaries, or the printed artifact will show the same mid-word breaks described in [`korean-typography.md`](korean-typography.md). Korean leading in print follows the same floor: 1.6 minimum for body copy.

## Recommended fallbacks

```css
:root {
  --font-ko-operational: "Noto Sans CJK KR", "Noto Sans KR", "Pretendard Variable", Pretendard, system-ui, sans-serif;
  --font-ko-formal: "Adobe Myungjo Std", "Nanum Myeongjo", "Noto Serif KR", serif;
}
```

Use fallbacks only when substitution is acceptable. For fixed-layout print files, install the intended font, or stop and report the missing-font dependency rather than silently reflowing the document.

## Delivery checks

Before delivering a PDF or print artifact:

1. Run the authoring application's missing-font and overset-text preflight.
2. Inspect the exported PDF with `pdffonts output.pdf` when Poppler is available.
3. Confirm every intended family is embedded or subset-embedded and no unexpected fallback appears.
4. Visually inspect Hangul glyphs, Latin/Hangul baselines, bold weights, table wrapping, page breaks, and form-field alignment.
5. Confirm no Korean word breaks mid-word.
6. Check contrast on any coloured text or filled table header — print and screen PDFs are both read on screen, and the palette roles in `SKILL.md` apply.
7. Record any unavoidable substitution in the handoff instead of presenting it as the original typography.
