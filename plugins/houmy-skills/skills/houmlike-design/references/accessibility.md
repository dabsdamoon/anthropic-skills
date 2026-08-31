# Houm Accessibility Floor

Read this before shipping any interactive surface.

The target is **WCAG 2.2 Level AA**. For Korean-market surfaces, **KWCAG 2.2** applies additionally and is tied to the 장애인차별금지법, which makes it a legal obligation rather than a quality preference.

WCAG 2.2 has been a W3C Recommendation since October 2023. Claiming "WCAG 2.1 AA" is claiming a superseded bar.

---

## What WCAG 2.2 added

Nine new success criteria; the Level A and AA ones are binding here. It also **removed** 4.1.1 Parsing, which no longer needs testing.

| SC | Level | Requirement |
|---|---|---|
| **2.4.11 Focus Not Obscured (Minimum)** | AA | The focused element must not be **entirely** hidden by author content — a sticky header, a cookie bar, a floating action button. |
| **2.5.7 Dragging Movements** | AA | Anything achievable by dragging must also be achievable with a single pointer without dragging. Every reorderable list needs move-up / move-down controls or an equivalent. |
| **2.5.8 Target Size (Minimum)** | AA | Pointer targets at least **24 x 24 CSS px**, or spaced so a 24px circle centred on each does not overlap a neighbour's. |
| **3.2.6 Consistent Help** | A | If help exists (contact link, chat, help page), it appears in the same relative order on every page that has it. |
| **3.3.7 Redundant Entry** | A | Do not ask for the same information twice in one process. Auto-populate it or offer it for selection. |
| **3.3.8 Accessible Authentication (Minimum)** | AA | No cognitive function test (remembering a password, transcribing a code, solving a puzzle) without an alternative. **Password fields must accept paste.** |

2.4.12, 2.4.13, and 3.3.9 are AAA and not required, but 2.4.13 Focus Appearance is a good default to aim at anyway.

---

## Contrast

| What | Ratio |
|---|---|
| Body text | 4.5:1 |
| Large text (18.66px bold, or 24px) | 3:1 |
| Control boundaries, focus indicators, meaningful graphics (SC 1.4.11) | 3:1 |
| Pure decoration, disabled controls | exempt |

Two failures recur across Houm surfaces, both from the same cause — a colour chosen in a mockup and never measured:

1. **A brand colour used as text on a light ground.** Houm Green on Houm Beige measures 3.91:1. It is an action fill, not body ink; `--houm-green-strong` is the text-safe green.
2. **A hairline used as a control boundary.** `--houm-hairline` measures 1.04:1 on beige and `--op-divider` 1.79:1 on the operator ground. Neither is a legal input border. Use `--houm-border` (3.33) or `--op-border-control` (3.50).

Measure, do not assume:

```bash
node scripts/check-contrast.mjs "#2F6238" "#F0E5C4"
node scripts/check-contrast.mjs --palette
```

"Disabled controls are exempt" is not permission to make disabled states invisible — an unreadable disabled control still fails usability, and if the state carries meaning it must not be conveyed by dimming alone.

---

## Focus

```css
:focus-visible {
  outline: 2px solid var(--houm-green-strong);
  outline-offset: 2px;
  border-radius: inherit;
}
:focus:not(:focus-visible) { outline: none; }
```

- Never `outline: none` without a replacement.
- The indicator needs 3:1 against **both** the component and its adjacent ground.
- Test with a sticky header present. A header that covers the focused row fails 2.4.11; give scroll containers `scroll-padding-block-start` equal to the header height.
- Focus order follows visual order. If a CSS `order` or `grid-area` reshuffle breaks that, the layout is wrong, not the tab order.

---

## Targets and pointers

- 24 x 24 CSS px minimum; 44 x 44 for anything primary or touch-first.
- An icon-only button needs padding, not just a large glyph.
- Dense operator tables still qualify: 32px rows clear 24px with room.
- Every drag interaction needs a non-drag equivalent (SC 2.5.7).
- Nothing depends on hover alone — hover has no keyboard or touch equivalent.

---

## Status and meaning

Colour is never the only carrier. Every status needs a second channel: an icon, a label, a shape, or a position.

```html
<span class="status status--blocked">
  <svg aria-hidden="true">...</svg>
  차단됨
</span>
```

Confirm this by viewing the page in `forced-colors: active` (Windows High Contrast) — author colours are stripped there, and anything that becomes ambiguous was relying on colour alone.

---

## Motion

```css
@media (prefers-reduced-motion: reduce) {
  *, *::before, *::after {
    animation-duration: 0.01ms !important;
    animation-iteration-count: 1 !important;
    transition-duration: 0.01ms !important;
    scroll-behavior: auto !important;
  }
}
```

Mandatory. Nothing auto-plays, auto-scrolls, or parallaxes without this. Anything that moves for more than five seconds needs a pause control (SC 2.2.2).

---

## Forms

- Every input has a real `<label>`, not a placeholder standing in for one.
- Errors identify the field, say what is wrong, and say how to fix it. Not "Invalid input."
- Errors are announced — `aria-describedby` on the field, `role="alert"` or `aria-live="polite"` on the message.
- Do not re-ask for information already given (SC 3.3.7).
- Allow paste everywhere, especially password and code fields (SC 3.3.8).
- Required is marked in text, not only with a red asterisk.

---

## KWCAG 2.2

The Korean guideline: **4 principles, 14 guidelines, 33 checkpoints**. It tracks WCAG closely, so meeting WCAG 2.2 AA covers most of it. Points where KWCAG is explicit and teams commonly miss:

- **자막 제공** — Korean captions for pre-recorded audio and video, not auto-generated only.
- **표의 구성** — data tables declare `<caption>`, `<th>`, and `scope`. Layout tables are not acceptable.
- **반복 영역 건너뛰기** — a skip-to-content link before repeated navigation, and it must be reachable and visible on focus.
- **제목 제공** — every page a unique, meaningful `<title>`; every frame a `title`.
- **기본 언어 표시** — `<html lang="ko">`, and `lang="en"` on English passages inside it. This also drives the `:lang(ko)` typography rules.
- **콘텐츠 선형 구조** — reading order remains meaningful with CSS off.

**KRDS** (https://www.krds.go.kr) publishes KWCAG 2.2-conformant component and typography specs. It is the right citation when a Korean accessibility decision needs external backing.

---

## Verification

Automated checks catch roughly a third of issues. Run them, then do the manual pass.

```bash
pnpm add -D @axe-core/playwright
```

```ts
import AxeBuilder from "@axe-core/playwright";

const results = await new AxeBuilder({ page })
  .withTags(["wcag2a", "wcag2aa", "wcag21a", "wcag21aa", "wcag22aa"])
  .analyze();
expect(results.violations).toEqual([]);
```

Manual pass, every time:

1. Tab through the entire page. Everything reachable, focus always visible, order matches the layout.
2. Tab with a sticky header present — nothing fully obscured.
3. Zoom to 200% and to 400% at 1280px wide. No horizontal page scroll, no clipped content.
4. `forced-colors: active`. Nothing becomes ambiguous.
5. `prefers-reduced-motion: reduce`. Nothing still moves.
6. Narrow to the smallest supported width. No Korean word splits mid-word.
7. Screen reader over one complete task — not just the landing view.

Report what was actually verified. An unrun check is not a passing check.
