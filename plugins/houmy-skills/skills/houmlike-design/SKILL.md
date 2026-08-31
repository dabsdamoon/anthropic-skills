---
name: houmlike-design
description: Create web UI, operator consoles, landing pages, and design artifacts for Houm. Applies Houm's brand identity, design tokens, Korean-first typography, and accessibility floor. Use when designing or building any visual or interactive surface for Houm — customer-facing product, internal tooling, or print and PDF collateral.
license: Complete terms in LICENSE.txt
---

# Houmlike Design

Houm's design system for every digital and printed surface: customer-facing product, internal operator tooling, and the documents that pass between them.

The system is **domain-neutral**. It supplies colour, type, spacing, motion, and an accessibility floor. It does not supply subject-matter guidance, and nothing in it should be read as constraining what Houm builds.

---

## Source Precedence

Apply typography and visual rules in this order:

1. Follow an explicit design handoff or design system in the target repository. Treat it as the product source of truth.
2. When editing an existing artifact, preserve its established typefaces and metrics unless the user asks for a redesign.
3. Use the canonical rules below when no artifact-specific rule exists.

Do not replace a repository's product typography merely to make it look more "Houm-like." Brand guidance supplies defaults; it does not override a documented product decision.

### Relationship to `artifact-design`

When both this skill and the bundled `artifact-design` skill are in play, they divide as follows:

- **houmlike-design supplies the constants**: palette, type stack, tokens, Korean typography rules, and the accessibility floor. These are not negotiable per-page.
- **artifact-design supplies the judgment**: how much design investment a request warrants, composition, hierarchy, when to be utilitarian versus editorial.

Follow `artifact-design`'s process, and draw every colour and typeface from this skill's tokens instead of inventing a new palette. Where `artifact-design` warns against a generic look, the differentiator here is the framed wordmark, the slab serif, and the green-centred palette.

---

## Reference Files

Read the relevant reference before starting work in that area. Each is short and self-contained.

| Reference | Read it before |
|---|---|
| [`references/surfaces.md`](references/surfaces.md) | Writing any token set, theming, or dark/dense UI |
| [`references/korean-typography.md`](references/korean-typography.md) | Any Korean or bilingual interface |
| [`references/accessibility.md`](references/accessibility.md) | Any interactive surface; contains the WCAG 2.2 and KWCAG 2.2 checklist |
| [`references/interaction-patterns.md`](references/interaction-patterns.md) | Consent flows, decision aids, dense data screens, destructive actions |
| [`references/document-typography.md`](references/document-typography.md) | Korean/bilingual PDF, InDesign, forms, checklists, agreements |

---

## Canonical Design System

Derived from the original 2019 Houm brand book, with colour roles corrected against measured contrast.

### Brand Mark

The official Houm brand mark is the wordmark **`Houm`** in Sanchez (slab serif) enclosed in a thin-stroke rectangular frame with small corner ticks, accompanied by a small superscript `®`. The mark is always rendered in Houm Green on Houm Beige, on white, or reversed on a dark ground. Never combine the brand mark with the Korean signature `호움` — the two are used independently.

**Ready-to-use asset:** [`assets/houm-mark.svg`](assets/houm-mark.svg) ships the canonical vector mark with the Sanchez Latin subset embedded as base64 woff2 — self-contained, and renders identically via `<img src>`, `<object>`, or inline. The mark is `currentColor`-driven: inlined, the stroke and text inherit `color` from the container; via `<img>`, the default `color="#3D7E48"` attribute renders canonical Houm Green. To theme it for a dark ground, inline the SVG and set the parent's `color`.

**Reference renders from the 2019 brand book:**
- [`assets/brand-mark-construction.png`](assets/brand-mark-construction.png) — construction grid, ® placement
- [`assets/brand-palette.png`](assets/brand-palette.png) — official mark on the four brand colours

**Reference HTML:**
```html
<span class="houm-brandmark">
  <span class="houm-brandmark__text">Houm<sup>®</sup></span>
</span>
```
```css
.houm-brandmark {
  display: inline-flex;
  align-items: center;
  border: 1.5px solid currentColor;
  border-radius: 3px;
  padding: 0.3em 0.7em 0.25em;
  color: var(--houm-green-strong);
}
.houm-brandmark__text {
  font-family: 'Sanchez', 'Roboto Slab', Georgia, serif;
  font-size: 1.5rem;
  letter-spacing: 0.01em;
}
.houm-brandmark__text sup {
  font-size: 0.42em;
  margin-left: 0.15em;
  transform: translateY(-0.4em);
}
```

The frame inherits `currentColor`, so setting one `color` themes both stroke and text. Use `--houm-green-strong` on light grounds — plain `--houm-green` on Houm Beige measures 3.91:1, below the 4.5 floor at wordmark body sizes.

---

### Colour roles, not just hex

**The single most common failure with this palette is treating every brand colour as a text colour.** It is not. Houm Green is a fill; the mustard and the soft blue are tints. Each colour below carries a role, and the role is binding.

Every ratio in this section is measured against the three light grounds this system uses — Houm Beige `#F0E5C4`, Beige Soft `#F5EFDF`, and white — and the figure shown is the **worst** of the three. Re-verify with `scripts/check-contrast.mjs` after any palette change.

#### Roles

| Role | Token | Hex | May be used as |
|---|---|---|---|
| Identity / action fill | `--houm-green` | `#3D7E48` | Button and badge **fills**, wordmark on white. White text on it: **4.91**. Not body text on beige (3.91). |
| Text-safe green | `--houm-green-strong` | `#2F6238` | **Green text and links on any light ground** (worst **5.71**), hover fill for `--houm-green`. |
| Green tint | `--houm-green-tint` | `#8FB498` | **Surface tints and decorative fills only.** Never text (2.30 on white), never a control border (1.83 on beige). |
| Warm accent fill | `--houm-accent-warm` | `#D6A93B` | Badge and highlight **fills**, with `--houm-text` on top (**6.71**). Never white text (2.19). Never a primary action. |
| Warm accent tint | `--houm-accent-warm-soft` | `#E8C97A` | Soft backgrounds, with `--houm-text` on top (**9.13**). |
| Warm accent text | `--houm-accent-warm-text` | `#6E5210` | Warning text and icons on light grounds (worst **5.81**). |
| Cool accent fill | `--houm-accent-cool` | `#B4D0E7` | Tag and panel **fills**, with `--houm-text` on top (**9.17**). Never white text (1.60). |
| Cool accent tint | `--houm-accent-cool-soft` | `#D6E5F2` | Quiet washes, with `--houm-text` on top (**11.43**). |
| Cool accent text | `--houm-accent-cool-text` | `#1B5478` | Informational text and icons on light grounds (worst **6.46**). |

The 2019 brand book names the two accents **Houm Baby Green** (Pantone 110C) and **Houm Baby Blue** (Pantone 277C). Those names are preserved as brand provenance, but **write code against the role tokens** — `--houm-accent-warm` / `--houm-accent-cool` — so the palette carries no assumption about what it is describing.

#### Grounds and ink

| Token | Hex | Notes |
|---|---|---|
| `--houm-canvas` | `#F0E5C4` | Houm Beige. Canonical page ground. Pantone 7499C. |
| `--houm-surface` | `#FFFFFF` | Cards and modals. Only 1.26:1 against the beige ground, so a card needs a shadow or a border to read as a distinct plane. |
| `--houm-surface-soft` | `#F5EFDF` | Softer section ground. |
| `--houm-text` | `#1F2937` | Body ink. **11.68** on beige. |
| `--houm-text-muted` | `#5A6560` | Secondary ink, worst **4.82**. Replaces `#6B7280`, which measured **3.85** on beige and failed the body floor. |
| `--houm-border` | `#71806F` | **Control boundaries** — inputs, checkboxes, focusable outlines. Worst **3.33**, clearing the 3:1 required by WCAG 1.4.11. |
| `--houm-hairline` | `#E4EBE4` | **Decoration only** — section rules, table zebra edges. At 1.04:1 on beige it carries no information; never use it as a control boundary. |

#### Status

| Token | Hex | Worst ratio |
|---|---|---|
| `--houm-success-text` | `#2F6238` | 5.71 |
| `--houm-warning-text` | `#6E5210` | 5.81 |
| `--houm-danger-text` | `#A02017` | 6.16 |
| `--houm-info-text` | `#1B5478` | 6.46 |

Semantic status is a separate axis from the brand accent. A warning is not "the mustard brand colour"; it is `--houm-warning-text` on `--houm-accent-warm-soft`. Never encode status in colour alone — pair it with an icon, a label, or a shape.

#### Token definitions

```css
:root {
  color-scheme: light;

  /* Grounds */
  --houm-canvas:            #F0E5C4;
  --houm-surface:           #FFFFFF;
  --houm-surface-soft:      #F5EFDF;

  /* Ink */
  --houm-text:              #1F2937;
  --houm-text-muted:        #5A6560;

  /* Lines */
  --houm-border:            #71806F;  /* control boundaries, >= 3:1 */
  --houm-hairline:          #E4EBE4;  /* decoration only */

  /* Identity */
  --houm-green:             #3D7E48;  /* fill */
  --houm-green-strong:      #2F6238;  /* text + hover fill */
  --houm-green-tint:        #8FB498;  /* tint only */

  /* Accents — role names; brand book calls these Baby Green / Baby Blue */
  --houm-accent-warm:       #D6A93B;
  --houm-accent-warm-soft:  #E8C97A;
  --houm-accent-warm-text:  #6E5210;
  --houm-accent-cool:       #B4D0E7;
  --houm-accent-cool-soft:  #D6E5F2;
  --houm-accent-cool-text:  #1B5478;

  /* Status */
  --houm-success-text:      #2F6238;
  --houm-warning-text:      #6E5210;
  --houm-danger-text:       #A02017;
  --houm-info-text:         #1B5478;
}
```

For the dark, dense **operator theme** used by internal consoles, and for deriving tints in `oklch`, read [`references/surfaces.md`](references/surfaces.md).

> **Legacy note:** Earlier iterations of the web app used `#668e67` as the primary green and a Terracotta (`#CCA893`) warm accent. Both are deprecated — migrate to `--houm-green` and the role accents above. `#6B7280` as muted text and `#E4EBE4` as a control border are also deprecated; both fail their contrast duty.

---

### Typography

The 2019 brand book defines four typefaces, split by language and tier:

| Tier | Language | Font | Fallback | Usage |
|------|----------|------|----------|-------|
| **Primary** | English | **Sanchez** | Roboto Slab, Georgia, serif | Headcopy, brand wordmark |
| Primary | Korean | **나눔명조 (Nanum Myeongjo)** | Noto Serif KR, serif | Headcopy |
| **Secondary** | English | **Noto Sans** | system-ui, sans-serif | Long-form bodycopy, dense text |
| Secondary | Korean | **Pretendard** | Noto Sans KR, system-ui, sans-serif | Bodycopy, all UI |

Sanchez is a warm slab serif — friendly-editorial, not institutional. Nanum Myeongjo is its Korean counterpart; pair the two when both languages appear. Drop to the secondary tier for long blocks of running text where the serif's texture becomes heavy.

**Sanchez ships one weight (400) plus an italic. There is no Sanchez Bold** — `fonts.googleapis.com/css2?family=Sanchez:wght@700` returns HTTP 400. Build heading hierarchy with size, colour, and spacing, not weight. When a genuinely bold slab is required, substitute Roboto Slab and say so in the handoff.

**Pretendard is the Korean UI default**, promoted from fallback. It is the de facto standard for Korean product interfaces, covers Latin and Hangul in one family with matched metrics, and needs no optical correction. KoPub돋움체 remains acceptable where a maintained template already specifies it, but it is not on Google Fonts and should not be introduced into new work. See [`references/korean-typography.md`](references/korean-typography.md) for the line-breaking, leading, and subsetting rules that matter far more than the family choice.

**Font loading (web):**
```html
<link rel="preconnect" href="https://fonts.googleapis.com" />
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin />
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Sanchez:ital@0;1&family=Nanum+Myeongjo:wght@400;700;800&family=Noto+Sans:wght@400;500;700&display=swap" />
```

Pretendard is not on Google Fonts. Load the dynamic-subset build, which serves only the glyphs a page uses:
```html
<link rel="stylesheet" href="https://cdn.jsdelivr.net/gh/orioncactus/pretendard@v1.3.9/dist/web/variable/pretendardvariable-dynamic-subset.min.css" />
```

**CSS variables:**
```css
:root {
  /* Each stack carries BOTH scripts within one brand tier. A Latin-only
     stack does not fail loudly on Korean text -- it silently falls back to
     whatever system face has Hangul, which differs per OS. */
  --font-heading: 'Sanchez', 'Nanum Myeongjo', 'Roboto Slab', 'Noto Serif KR', Georgia, serif;
  --font-body:    'Noto Sans', 'Pretendard Variable', Pretendard, 'Noto Sans KR', system-ui, sans-serif;

  /* Single-script stacks, for surfaces that are only one language. */
  --font-en-primary:   'Sanchez', 'Roboto Slab', Georgia, serif;
  --font-en-secondary: 'Noto Sans', system-ui, sans-serif;
  --font-ko-primary:   'Nanum Myeongjo', 'Noto Serif KR', serif;
  --font-ko-secondary: 'Pretendard Variable', Pretendard, 'Noto Sans KR', system-ui, sans-serif;
}

html[lang="ko"] {
  --font-heading: var(--font-ko-primary);
  --font-body:    var(--font-ko-secondary);
}
```

Note that a per-language override like the block above is **not** sufficient on
its own. A utility class (Tailwind's `font-display`) lands in a later cascade
layer than `@layer base` and wins, so the stack itself must cover both scripts.
Verify the *rendered* face, not the declared one.

**Typography principles:**
- Minimum 16px body text. Set the scale in `rem` and let it respond with `clamp()` rather than fixed breakpoint jumps.
- Line height 1.5–1.7 for English, **1.6–1.8 for Korean** — Hangul needs more leading.
- Build hierarchy with size, colour, and spacing. Sanchez has no bold; Nanum Myeongjo has 400/700/800.
- For mixed EN/KO lines, stay in one tier — Sanchez pairs with Nanum Myeongjo, Noto Sans pairs with Pretendard. Do not pair Sanchez with Pretendard in the same heading.
- Keep running text near 65 characters. `text-wrap: balance` on headings, `text-wrap: pretty` on paragraphs.
- Avoid decorative faces. Clarity first.

**Canvas fonts for static output (posters, PDFs):**
`canvas-fonts/` ships seven families for work without web font access. Sanchez and Nanum Myeongjo are **not** bundled.

- **Canonical-aligned**: CrimsonPro or Roboto Slab (heading) + WorkSans (body)
- **Editorial**: CrimsonPro + InstrumentSans
- **Modern warm**: Lora + WorkSans
- **Modern approachable**: Outfit + WorkSans

LibreBaskerville is kept for legacy alignment only and is not the brand serif.

---

### Spacing, radius, elevation, motion

Spacing runs on a 4px base. Prefer layout `gap` over per-element margins.

| Element | Radius |
|---|---|
| Buttons | 12px |
| Cards | 16px |
| Inputs | 8px |
| Badges, pills | full |
| Avatars | full |

Vary radius by role rather than applying one value everywhere — uniform rounding is one of the tells listed under Design Judgment.

```css
:root {
  --shadow-soft:   0 2px 8px rgb(0 0 0 / 8%);
  --shadow-medium: 0 4px 16px rgb(0 0 0 / 12%);
  --shadow-glow:   0 0 20px rgb(61 126 72 / 18%);

  --ease-out:    cubic-bezier(0.16, 1, 0.3, 1);
  --ease-in-out: cubic-bezier(0.65, 0, 0.35, 1);
  --dur-fast:    120ms;
  --dur-base:    200ms;
  --dur-slow:    320ms;
}

@media (prefers-reduced-motion: reduce) {
  *, *::before, *::after {
    animation-duration: 0.01ms !important;
    animation-iteration-count: 1 !important;
    transition-duration: 0.01ms !important;
    scroll-behavior: auto !important;
  }
}
```

The reduced-motion block is mandatory on every artifact, not optional polish.

---

## Accessibility Floor

Every Houm surface targets **WCAG 2.2 AA**, and every Korean-market surface additionally targets **KWCAG 2.2**, which is tied to the 장애인차별금지법. WCAG 2.1 is no longer the bar.

The non-negotiables:

- Contrast: 4.5:1 body text, 3:1 large text (18.66px bold / 24px), 3:1 for control boundaries and meaningful graphics.
- Pointer targets at least **24 x 24 CSS px** (WCAG 2.2 SC 2.5.8). 44px is the comfortable default for primary controls.
- A focus indicator that is visible, at least 3:1 against its surroundings, and **never fully obscured** by sticky headers or footers (SC 2.4.11).
- Do not require memorised secrets or transcription to authenticate; allow paste (SC 3.3.8).
- Status is never colour alone.
- Semantic HTML, real labels, error text that says what to fix.

The full checklist, the KWCAG mapping, and how to verify are in [`references/accessibility.md`](references/accessibility.md).

---

## Modern CSS Baseline

These are Baseline as of 2026 and should be used directly rather than reached for via JavaScript or a library:

- **Container queries** for component-level responsiveness. A card that adapts to its container is more reusable than one that adapts to the viewport.
- **`:has()`** for parent-state styling.
- **Cascade layers (`@layer`)** to keep resets, tokens, components, and utilities from fighting on specificity.
- **`light-dark()`** and `color-scheme` for theme values without duplicated blocks.
- **`color-mix()` and `oklch()`** for deriving tints and shades that stay perceptually even — see [`references/surfaces.md`](references/surfaces.md).
- **View transitions** (same-document) for state changes that benefit from continuity. Cross-document transitions and `@position-try` still need a fallback path.
- **`text-wrap: balance` / `pretty`**, `font-variant-numeric: tabular-nums` wherever digits align in columns.

Do not ship a JavaScript solution for something CSS now does natively.

---

## Workflows

### 1. React web artifact

```bash
bash scripts/init-artifact.sh <project-name>
cd <project-name>
pnpm dev
```

Scaffolds React 19 + TypeScript + Vite 8 + Tailwind CSS v4 + shadcn/ui, with Houm tokens wired into Tailwind's CSS-first `@theme` and both themes defined.

Bundle to a single self-contained HTML file:
```bash
bash scripts/bundle-artifact.sh
```

**Stack:**
- React 19, TypeScript, Vite 8 (Rolldown)
- Tailwind CSS v4 via `@tailwindcss/vite` — CSS-first `@theme`, no `tailwind.config.js`, no PostCSS or Autoprefixer
- shadcn/ui via its CLI, on the unified `radix-ui` package, `tw-animate-css`, warm `stone` base
- `vite-plugin-singlefile` for the single-file bundle

Components are fetched by the CLI at scaffold time, so they arrive current instead of frozen in a tarball.

### 2. Static design artifact

1. **Define intent** — purpose, audience, single key message.
2. **Choose type** from `canvas-fonts/` using a pairing above.
3. **Compose** — visual hierarchy through colour and scale, generous whitespace, one focal element.
4. **Output** PNG or PDF, then verify: palette roles respected, contrast measured not assumed, no fallback fonts silently substituted.

For Korean and bilingual documents, read [`references/document-typography.md`](references/document-typography.md) first — it carries the preflight and font-embedding checks.

---

## Component Styling

Reference values for a Tailwind v4 or plain-CSS build. Every pairing below is measured.

- **Primary button**: `--houm-green` fill, white label (4.91), `--houm-green-strong` on hover (7.18).
- **Secondary button**: transparent fill, `--houm-border` outline, `--houm-green-strong` label (5.71). Do **not** fill with `--houm-green-tint` — white on it measures 2.30.
- **Page ground**: `--houm-canvas`. **Card**: `--houm-surface` with `--shadow-soft`, since white on beige is only 1.26:1 on its own.
- **Input**: `--houm-border` boundary (3.33), `--houm-text` value, `--houm-text-muted` placeholder, `--houm-green-strong` focus ring at 2px with a 2px offset.
- **Badge, warm**: `--houm-accent-warm` fill with `--houm-text` label (6.71), or `--houm-accent-warm-soft` fill with `--houm-accent-warm-text` label.
- **Badge, cool**: `--houm-accent-cool` fill with `--houm-text` label (9.17).
- **Section rule**: `--houm-hairline`, decoration only.

---

## Design Judgment

**Avoid — the 2026 generated-design cluster:**
- Warm cream ground plus serif display plus terracotta accent. This is the closest generic look to Houm's palette, so it is the one to actively differentiate from: the differentiators are the **framed wordmark**, the **slab** serif rather than a fashionable didone, and green rather than terracotta as the accent.
- Near-black with a single acid-green or vermilion pop.
- Purple-to-blue gradient hero on white.
- Inter or Space Grotesk applied flat across an entire page.
- Emoji as section markers; everything centred; identical rounding on every element; an accent bar on every rounded card.
- Numbered eyebrows (01 / 02 / 03) on content that is not actually a sequence.
- Generic stock imagery, elaborate animation, cluttered density.

**Prefer:**
- Asymmetric, intentional layout with real whitespace.
- Hierarchy from size, colour, and spacing — Sanchez gives no bold to lean on.
- Radius varied by role.
- One deliberate accent, kept quiet everywhere else.
- Structural devices that encode something true about the content.
- Motion that serves a state change, respecting `prefers-reduced-motion`.
- Copy written from the reader's side of the screen: active voice, controls that name what happens, errors that say how to fix.

---

## Brand Provenance

Recorded from the 2019 brand book. This is **provenance, not design constraint** — the visual system above stands on its own and must not be applied as subject-matter guidance.

`Houm` / `호움` combines **호 (戶)**, the household, with **움**, a new sprout. The English transliteration also evokes "home." The 2019 book records four values — **생명 (Life)**, **관계 (Relationship)**, **결속 (Bonding)**, **회복 (Recovery)** — and centres green on the grounds that *"초록색은 생명력을 회복시키고 마음에 평안을 준다."*

The operational design principles those values translate into are general:

1. **Informed by default** — transparency and clear communication. Clear information hierarchy, readable typography, navigation that does not hide consequences.
2. **Evidence-grounded** — professional, trustworthy, structured. Credible visual language over decoration.
3. **Collaborative** — warm and supportive. Inclusive imagery, partnership-focused messaging.
4. **Minimal intervention** — thoughtful and intentional. Avoid over-design; every element earns its place.

---

## Quality Bar

Before delivering, confirm:

1. Colour roles respected — no text on a tint, no white on an accent fill.
2. Contrast **measured**, not assumed. Run `scripts/check-contrast.mjs` on any new pairing.
3. WCAG 2.2 AA met, including 24px targets and unobscured focus.
4. Korean text sets `word-break: keep-all`; Korean line height at or above 1.6.
5. Both themes defined at token level; `body` paints an explicit background.
6. `prefers-reduced-motion` honoured.
7. No deprecated values: `#668e67`, `#CCA893`, `#6B7280` as text, `#E4EBE4` as a control border.
8. Nothing from the generated-design cluster above.

---

## Resources

- **Brand assets** — `assets/houm-mark.svg` (canonical framed wordmark, `currentColor`-driven), `assets/brand-mark-construction.png`, `assets/brand-palette.png`
- **Canvas fonts** — `canvas-fonts/`: Lora, InstrumentSans, InstrumentSerif, WorkSans, Outfit, CrimsonPro, LibreBaskerville. Sanchez and Nanum Myeongjo are not bundled; load from Google Fonts for web, substitute CrimsonPro or Roboto Slab for static output.
- **Scripts** — `scripts/init-artifact.sh`, `scripts/bundle-artifact.sh`, `scripts/check-contrast.mjs`
- **shadcn/ui** — https://ui.shadcn.com/docs/components
- **Tailwind v4 theme** — https://tailwindcss.com/docs/theme
- **KRDS (Korea Design System)** — https://www.krds.go.kr — KWCAG 2.2-conformant Korean typography and component specs
