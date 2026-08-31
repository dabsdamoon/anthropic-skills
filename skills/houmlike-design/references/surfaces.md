# Houm Surfaces and Themes

Read this before writing any token set, adding a theme, or building a dense internal screen.

Houm runs **two** surface families. They are not light and dark variants of one another; they exist for different jobs and have different densities.

| Family | Ground | Job |
|---|---|---|
| **Brand** | Houm Beige `#F0E5C4` | Customer-facing product, marketing, documents. Warm, spacious, editorial. |
| **Operator** | Near-black green `#08100c` | Internal consoles and dense tooling. Long sessions, high information density, low eye strain. |

Pick the family from the surface's job, not from the viewer's OS preference. A marketing page does not become an operator console because the viewer prefers dark mode, and an operator console does not turn beige because they prefer light.

Within a family, still honour `prefers-color-scheme` where a genuine light/dark pair exists.

---

## Brand family

The full token set is in `SKILL.md`. Two rules that are easy to get wrong:

**`body` must paint an explicit background.** A transparent body borrows whatever ground the host paints, which is how a page ends up with one theme's text on the other theme's ground.

```css
body {
  background: var(--houm-canvas);
  color: var(--houm-text);
}
```

**A white card on Houm Beige measures 1.26:1.** That is not a violation — a card is not a control — but it does mean the card has no edge of its own. Give it `--shadow-soft` or a `--houm-hairline` border, or it will read as a shapeless lighter patch.

---

## Operator family

For internal consoles: dark, dense, sans and mono only. Green is the sole action colour, the warm accent is pre-warning and never a button, the cool accent marks confirmed states, red marks blocking states.

Every foreground below is measured against all four operator grounds; the figure is the **worst** of the four.

```css
:root[data-theme="operator"] {
  color-scheme: dark;

  /* Grounds */
  --op-canvas:           #08100c;
  --op-surface:          #0f1512;
  --op-surface-raised:   #131a16;
  --op-surface-card:     #151c18;
  --op-surface-hover:    #1b241e;

  /* Ink — worst-case ratio across all four grounds */
  --op-text:             #e7ede8;  /* 13.41 */
  --op-text-secondary:   #c3d1c7;  /* 10.07 */
  --op-text-muted:       #94a89a;  /*  6.32 */
  --op-text-faint:       #7e9184;  /*  4.76 */
  --op-text-disabled:    #3a4740;  /* below AA by design; never load-bearing */

  /* Lines */
  --op-hairline:         #1f2922;  /* decoration only */
  --op-divider:          #263028;  /* decoration only */
  --op-border-control:   #6A7A6C;  /* control boundaries, worst 3.50 */

  /* Action and status */
  --op-green:            #57a867;  /* fill; --op-canvas on it: 6.61 */
  --op-green-hover:      #4a9459;
  --op-green-light:      #8fcb9b;  /* text, 8.49; focus ring */
  --op-mustard:          #d6a93b;  /* fill; --op-canvas on it: 8.81 */
  --op-mustard-text:     #e2c078;  /* 9.14 */
  --op-blue:             #9fc4e3;
  --op-blue-text:        #bfd8ec;  /* 10.81 */
  --op-red:              #d46950;  /* fill; --op-canvas on it: 5.45 */
  --op-red-text:         #e7a392;  /* 7.63 */

  --font-op: 'Pretendard Variable', Pretendard, 'Noto Sans KR', system-ui, sans-serif;
  --shadow-frame:   0 18px 44px rgb(0 0 0 / 45%);
  --shadow-hero:    0 24px 60px rgb(0 0 0 / 50%);
  --shadow-popover: 0 8px 20px rgb(0 0 0 / 40%);
}
```

### The two border tokens are not interchangeable

`--op-hairline` (1.35:1) and `--op-divider` (1.79:1) are **decoration**. They separate regions visually and carry no information.

`--op-border-control` (3.50:1) is what an input, checkbox, radio, or any focusable boundary must use. WCAG 1.4.11 requires 3:1 for the visual boundary of a control; the decorative tokens do not reach it on any operator ground.

This is the same mistake the brand family makes with `#E4EBE4`. A hairline that looks right in a mockup is almost never contrasty enough to be a control boundary.

### Operator density

- Base text 13–14px, not 16px. The 16px floor is a reading-comfort rule for prose; a data grid trades it for density and compensates with generous line height and column spacing.
- Line height 1.5 minimum even at 13px, and 1.6+ for any Korean text.
- `font-variant-numeric: tabular-nums` on every numeric column, without exception.
- Row height at least 32px so the 24px target minimum is met with padding to spare.
- Disabled is not a colour-only state. Pair `--op-text-disabled` with `aria-disabled` and a cursor change.

---

## Deriving tints with OKLCH

Do not eyeball a lighter or darker variant. Hold hue and chroma, move lightness — OKLCH is perceptually uniform, so equal lightness steps look equal.

The brand green sits at hue **~148** across every variant:

```
--houm-green-strong  #2F6238   oklch(44.9% 0.087 147.9)
--houm-green         #3D7E48   oklch(53.6% 0.107 147.6)
--houm-green-tint    #8FB498   oklch(73.5% 0.057 152.2)
--op-green           #57a867   oklch(66.3% 0.125 148.6)
--op-green-light     #8FCB9B   oklch(78.8% 0.092 150.1)
```

To add a step, keep `H` and pick an `L`:

```css
--houm-green-050: oklch(96% 0.02 148);
--houm-green-600: oklch(48% 0.10 148);
```

For a one-off blend, `color-mix()` is simpler and needs no conversion:

```css
background: color-mix(in oklab, var(--houm-green) 12%, var(--houm-surface));
border-color: color-mix(in oklab, var(--houm-border) 60%, transparent);
```

**Deriving a colour does not exempt it from measurement.** Perceptual uniformity is not contrast conformance. Run `scripts/check-contrast.mjs` on anything new.

---

## Theming mechanics

The viewer has three states, not two: an explicit choice stamps `data-theme` on the root, and the default "system" setting stamps nothing — there, only `prefers-color-scheme` separates light from dark.

```css
/* 1. Complete light palette on bare :root — always applies */
:root { color-scheme: light; --ground: #F0E5C4; --ink: #1F2937; }

/* 2. Dark OS preference, unless the viewer explicitly chose light */
@media (prefers-color-scheme: dark) {
  :root:not([data-theme="light"]) { color-scheme: dark; --ground: #0f1512; --ink: #e7ede8; }
}

/* 3. Explicit dark choice wins over a light OS */
:root[data-theme="dark"] { color-scheme: dark; --ground: #0f1512; --ink: #e7ede8; }
```

Style components through the tokens, never inside the media or attribute block. A colour whose only definition sits behind `[data-theme]` never applies in the un-stamped state, and that is the classic unreadable-page bug.

Where a value genuinely has just two states and no explicit toggle is needed, `light-dark()` collapses the whole pattern:

```css
:root { color-scheme: light dark; }
.panel { background: light-dark(#FFFFFF, #151c18); }
```

Before publishing, scan the stylesheet for any colour declared **only** inside a media or `[data-theme]` block. That is the bug.

---

## Forced colours

Windows High Contrast strips author colours. Do not fight it — make sure nothing load-bearing was carried by colour alone.

```css
@media (forced-colors: active) {
  .btn { border: 1px solid ButtonBorder; }
  .status-dot { forced-color-adjust: none; }
}
```

If a status is a bare coloured dot, it disappears here. That is the signal it needed a label or an icon all along.
