# Korean Web Typography

Read this before building any Korean or bilingual interface. Family choice matters far less than the four rules below; getting these wrong makes good type look broken, and getting them right makes ordinary type look considered.

---

## 1. Line breaking — the single highest-impact rule

Latin text breaks at spaces. Hangul is written with spaces too, but browsers default to `word-break: normal`, which for CJK permits breaking **between any two syllable blocks**. The result is a word split across lines mid-word, which native readers register immediately as broken.

```css
:lang(ko) {
  word-break: keep-all;      /* break at spaces, not inside 어절 */
  overflow-wrap: anywhere;   /* but still break a string with no spaces */
  line-break: strict;        /* do not start a line with a small kana or a closing mark */
}
```

`keep-all` alone will overflow its container when a single unbroken token is wider than the line — a long URL, an ID, a run of Latin. `overflow-wrap: anywhere` is the safety valve; use both, always together.

Apply it via `:lang(ko)` rather than a global rule, so English content keeps normal breaking behaviour in a bilingual page.

For headings and short UI strings, `keep-all` plus `text-wrap: balance` gives the most even result:

```css
:lang(ko) h1, :lang(ko) h2, :lang(ko) .label {
  word-break: keep-all;
  text-wrap: balance;
}
```

---

## 2. Leading

Hangul syllable blocks are visually denser and taller than Latin lowercase. The same `line-height` that reads comfortably in English reads cramped in Korean.

| Context | English | Korean |
|---|---|---|
| Body prose | 1.5–1.7 | **1.6–1.8** |
| Dense UI, tables | 1.4 | **1.5–1.6** |
| Headings | 1.1–1.25 | **1.3–1.4** |

Never take Korean prose below 1.6. In a bilingual layout set the Korean value and let English inherit it — the extra leading costs English nothing, while the reverse is actively uncomfortable.

---

## 3. Letter spacing

Hangul needs slightly negative tracking at display sizes and none at body sizes. Positive letter-spacing on Korean body text is a common and damaging mistake — it breaks the visual integrity of the syllable block.

```css
:lang(ko) { letter-spacing: 0; }
:lang(ko) h1, :lang(ko) h2 { letter-spacing: -0.02em; }
```

The uppercase-label convention (`text-transform: uppercase; letter-spacing: 0.12em`) has no Korean equivalent. For a Korean eyebrow or label, use size, weight, and colour instead.

---

## 4. Font loading and weight

**Pretendard is the default for Korean UI.** It covers Latin and Hangul in one family with matched metrics and vertical rhythm, so a mixed line does not shift baseline or weight mid-sentence.

```html
<link rel="stylesheet" href="https://cdn.jsdelivr.net/gh/orioncactus/pretendard@v1.3.9/dist/web/variable/pretendardvariable-dynamic-subset.min.css" />
```

```css
:root {
  --font-ko: 'Pretendard Variable', Pretendard, 'Noto Sans KR', system-ui, sans-serif;
}
```

**Always use a subset build.** A full Korean font is enormous — the writing system needs roughly 11,172 precomposed syllables, and an unsubsetted family runs into the megabytes. Two acceptable approaches:

- **Dynamic subset** (Pretendard's `-dynamic-subset` build, and how Google Fonts serves Korean): the CSS declares many `@font-face` rules split by `unicode-range`, and the browser downloads only the ranges the page actually uses.
- **Static subset** for a fixed, known string set — a poster, a wordmark, a fixed label set. Generate with `pyftsubset` and embed.

Never link a full `.otf` or `.ttf` Korean family from a web page.

Set `font-display: swap` so text renders in the fallback immediately. With Korean this matters more than with Latin, because the fallback is usually a system Hangul face with different metrics — reserve space with `size-adjust` if the reflow is visible.

### A Latin-only stack does not fail loudly on Korean

This is the trap that survives review, because the page still looks fine.

Set `font-family: "Sanchez", "Roboto Slab", Georgia, serif` on a Korean
heading and nothing errors. Sanchez has no Hangul glyphs, so the browser walks
the stack, finds none of them cover Hangul either, and falls back to whatever
system Korean face it has. The heading renders in a font nobody chose, and it
differs per operating system.

Build every stack so it covers **both scripts within one brand tier**:

```css
/* Tier 1: Sanchez for Latin, Nanum Myeongjo for Hangul */
--font-display: "Sanchez", "Nanum Myeongjo", "Roboto Slab", "Noto Serif KR", Georgia, serif;

/* Tier 2: Noto Sans for Latin, Pretendard for Hangul */
--font-body: "Noto Sans", "Pretendard Variable", Pretendard, "Noto Sans KR", system-ui, sans-serif;
```

Per-script `:lang(ko)` rules are not enough on their own: a utility class
(`font-display` in Tailwind) sits in a later cascade layer than `@layer base`
and overrides them. The stack itself has to be correct.

Verify by reading the **rendered** font, not the declared one — DevTools'
Computed panel names the face actually used, and `document.fonts` reports
`loaded` versus `unloaded` per family.

**Weights:** Pretendard ships a variable axis 100–900. Nanum Myeongjo offers 400/700/800. Sanchez has **one** weight (400) and no bold — build Latin heading hierarchy from size and colour, and do not pair a bold Korean heading with a regular Sanchez one on the same line, since the mismatch reads as an error.

---

## 5. Mixed Korean and English

- Stay in one tier per line. Do not pair the primary serif with the secondary sans in a single heading.
- Prefer a family that covers both scripts (Pretendard, Noto Sans KR) over pairing two families, which introduces baseline and width mismatch on every mixed line.
- Latin inside Korean prose keeps Korean's leading and `keep-all`.
- Numbers and units follow Korean spacing convention: `3개월`, `12주`, `1,200원` — no space before a Korean counter, a space before a Latin unit (`12 kg`).
- `font-variant-numeric: tabular-nums` on every aligned numeric column, in both languages.

---

## 6. Verification

Reading the CSS is not enough. Check the rendered result:

1. Narrow the viewport to the smallest supported width and confirm no Korean word splits mid-word.
2. Put a long unbroken token — a URL or a 40-character ID — in the narrowest container and confirm it wraps rather than overflowing.
3. Confirm the Korean face actually loaded and did not silently fall back: compare against a deliberate `font-family: monospace` render, or check DevTools' rendered-font readout.
4. Confirm Korean line height computes to at least 1.6 at body size.
5. Check a mixed EN/KO line for baseline shift.

---

## Reference

- **KRDS (Korea Design System)** — https://www.krds.go.kr/html/site/style/style_03.html — the government design system's typography spec, built to KWCAG 2.2. A good citation when a Korean type decision needs external backing.
- **Pretendard** — https://github.com/orioncactus/pretendard
