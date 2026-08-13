---
name: houmlike-design
description: Create web UI, interfaces, landing pages, and design artifacts for Houm, a maternity care service provider. This skill should be used when designing or building any visual or interactive elements for Houm's digital presence, applying Houm's brand identity, values, and design philosophy.
license: Complete terms in LICENSE.txt
---

# Houmlike Design

To create designs and interfaces for Houm, use this skill. Houm is a maternity care service provider committed to transforming the maternity care experience through informed consent, evidence-based care, companion support, and mindful intervention.

---

## Source Precedence

Apply typography and visual rules in this order:

1. Follow an explicit design handoff or design system in the target repository. Treat it as the product source of truth.
2. When editing an existing artifact, preserve its established typefaces and metrics unless the user asks for a redesign.
3. Use the canonical 2019 brand-book rules below when no artifact-specific rule exists.

Do not replace a repository's product typography merely to make it look more “Houm-like.” Brand guidance supplies defaults; it does not override a documented product decision.

For Korean or bilingual PDF, InDesign, form, checklist, agreement, or other operational-document work, read [`references/document-typography.md`](references/document-typography.md) before choosing or changing fonts. It distinguishes canonical brand fonts from typefaces observed in shipped Houm documents.

## Canonical Design System

**This section defines THE standard, derived directly from the original 2019 Houm brand book. Use these values for consistency across all Houm properties.**

### Brand Mark

The official Houm brand mark is the wordmark **`Houm`** in Sanchez (slab serif) enclosed in a thin-stroke rectangular frame with small corner ticks, accompanied by a small superscript `®`. The mark is always rendered in Houm Green on Houm Beige (or on white). Never combine the brand mark with the Korean signature `호움` — the two are used independently.

**Ready-to-use asset:** [`assets/houm-mark.svg`](assets/houm-mark.svg) ships the canonical vector mark with the Sanchez Latin subset embedded as base64 woff2 — the file is self-contained and renders identically via `<img src>`, `<object>`, or inline. The mark is `currentColor`-driven: when inlined, the stroke and text inherit `color` from the container; when used via `<img>`, the default `color="#3D7E48"` attribute on the SVG renders the canonical Houm Green. To theme for use on green or other dark backgrounds, inline the SVG and set the parent's `color`.

**Reference renders from the 2019 brand book:**
- [`assets/brand-mark-construction.png`](assets/brand-mark-construction.png) — construction grid, ® placement
- [`assets/brand-palette.png`](assets/brand-palette.png) — official mark on the four brand colors

**Reference HTML (web rendering of the framed wordmark):**
```html
<span class="houm-brandmark">
  <span class="houm-brandmark__text">Houm<sup>®</sup></span>
</span>
```
```css
.houm-brandmark {
  display: inline-flex;
  align-items: center;
  border: 1.5px solid var(--houm-green);
  border-radius: 3px;
  padding: 0.3em 0.7em 0.25em;
  color: var(--houm-green);
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

### Canonical Typography

The 2019 brand book defines four typefaces, split by language and tier:

| Tier | Language | Font | Fallback | Usage |
|------|----------|------|----------|-------|
| **Primary** | English | **Sanchez** | Roboto Slab, Georgia, serif | Headcopy, bodycopy, brand wordmark |
| Primary | Korean | **나눔명조 (Nanum Myeongjo)** | Noto Serif KR, serif | Headcopy |
| **Secondary** | English | **Noto Sans** | system-ui, sans-serif | Long-form bodycopy, dense text |
| Secondary | Korean | **KoPub돋움체 (KoPub Dotum)** | Pretendard, Noto Sans KR, sans-serif | Bodycopy |

Sanchez is a warm slab serif — friendly-editorial, not clinical. Nanum Myeongjo is the Korean serif counterpart; pair the two when both languages appear together. Drop to Noto Sans / KoPub Dotum for long blocks of running text where the serif's texture would become heavy.

**Font Loading (Web):**
```html
<link rel="preconnect" href="https://fonts.googleapis.com" />
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin />
<link href="https://fonts.googleapis.com/css2?family=Sanchez:ital@0;1&family=Nanum+Myeongjo:wght@400;700;800&family=Noto+Sans:wght@400;500;700&family=Noto+Sans+KR:wght@400;500;700&display=swap" rel="stylesheet" />
```

KoPub돋움체 is not on Google Fonts; load via [webfontworld](https://github.com/webfontworld/kopubworld) or substitute with Pretendard / Noto Sans KR.

**CSS Variables:**
```css
:root {
  --font-en-primary:   'Sanchez', 'Roboto Slab', Georgia, serif;
  --font-en-secondary: 'Noto Sans', system-ui, sans-serif;
  --font-ko-primary:   'Nanum Myeongjo', 'Noto Serif KR', serif;
  --font-ko-secondary: 'Pretendard', 'Noto Sans KR', system-ui, sans-serif;

  /* Aliases used by components */
  --font-heading: var(--font-en-primary);
  --font-body:    var(--font-en-secondary);
}

html[lang="ko"] {
  --font-heading: var(--font-ko-primary);
  --font-body:    var(--font-ko-secondary);
}
```

**Tailwind Config:**
```javascript
fontFamily: {
  serif:  ['Sanchez', 'Roboto Slab', 'Georgia', 'serif'],          // EN primary
  myeong: ['Nanum Myeongjo', 'Noto Serif KR', 'serif'],            // KO primary
  sans:   ['Noto Sans', 'system-ui', 'sans-serif'],                // EN secondary
  kosans: ['KoPub돋움체', 'Pretendard', 'Noto Sans KR', 'sans-serif'], // KO secondary
}
```

### Canonical Colors

The 2019 brand book defines two primaries (Houm Green + Houm Beige) and two accents (Houm Baby Green + Houm Baby Blue). The Pantone references in the brand book map approximately to the hex values below — the exact Pantone-to-screen conversion may need fine-tuning per asset.

**Primary Palette — Houm Green & Houm Beige:**

| Name | Hex | Pantone | Usage |
|------|-----|---------|-------|
| **Houm Green** | `#3D7E48` | 7731C | Brand wordmark, primary buttons, key text, accents |
| Houm Green Dark | `#2F6238` | — | Hover states, deep emphasis |
| Houm Green Light | `#8FB498` | — | Highlights, soft tints, decorative use |
| **Houm Beige** | `#F0E5C4` | 7499C | Canonical page background |
| Houm Beige Soft | `#F5EFDF` | — | Card backgrounds, soft sections |

**Secondary Accent Palette — Houm Baby Green & Houm Baby Blue:**

| Name | Hex | Pantone | Usage |
|------|-----|---------|-------|
| **Houm Baby Green** | `#D6A93B` | 110C | Mustard/ochre accent — warmth, optimism, highlight badges |
| Houm Baby Green Light | `#E8C97A` | — | Soft mustard backgrounds |
| **Houm Baby Blue** | `#B4D0E7` | 277C | Soft sky accent — calm, care, gentle notifications |
| Houm Baby Blue Light | `#D6E5F2` | — | Subtle blue washes |

> **Design Intent (from brand book):** Green centers the palette — *"초록색은 생명력을 회복시키고 마음에 평안을 준다"* (green restores vitality and brings peace of mind). The mustard and soft blue are deliberate counterpoints for warmth and calm, not call-to-action colors. Action and brand identity always remain in Houm Green.

**Neutral Palette:**

| Name | Hex | Usage |
|------|-----|-------|
| Text | `#1F2937` | Body text |
| Text Muted | `#6B7280` | Secondary text |
| Surface White | `#FFFFFF` | Cards, modals |
| Divider | `#E4EBE4` | Hairlines, subtle dividers |

**Color Relationship:**
```
       Houm Green (action, identity)
              ↑
              │
   ────────── ●  ──────────
   │                       │
Baby Green                Baby Blue
(warmth, highlight)       (calm, care)
              │
              ↓
       Houm Beige
       (unifies the palette as the
        canonical background)
```

**CSS Variables (recommended):**
```css
:root {
  /* Houm Green — primary, action, identity */
  --houm-green:       #3D7E48;
  --houm-green-dark:  #2F6238;
  --houm-green-light: #8FB498;

  /* Houm Beige — canonical background */
  --houm-beige:       #F0E5C4;
  --houm-beige-soft:  #F5EFDF;

  /* Houm Baby palette — secondary accents */
  --houm-baby-green:        #D6A93B;
  --houm-baby-green-light:  #E8C97A;
  --houm-baby-blue:         #B4D0E7;
  --houm-baby-blue-light:   #D6E5F2;

  /* Neutrals */
  --houm-text:        #1F2937;
  --houm-text-muted:  #6B7280;
  --houm-surface:     #FFFFFF;
  --houm-divider:     #E4EBE4;
}
```

> **Legacy note:** Earlier iterations of the web app used `#668e67` as the primary green and a Terracotta (`#CCA893`) warm accent. Both are deprecated by the 2019 brand book — migrate to **Houm Green `#3D7E48`** and the **Baby Green / Baby Blue** accents above.

### Canonical Spacing & Radius

| Element | Border Radius | Notes |
|---------|---------------|-------|
| Buttons | `rounded-xl` (12px) | Consistent across all buttons |
| Cards | `rounded-2xl` (16px) | Slightly softer for containers |
| Inputs | `rounded-lg` (8px) | Compact, functional feel |
| Avatars | `rounded-full` | Always circular |

### Canonical Shadows

```css
--shadow-soft: 0 2px 8px rgba(0, 0, 0, 0.08);
--shadow-medium: 0 4px 16px rgba(0, 0, 0, 0.12);
--shadow-glow: 0 0 20px rgba(61, 126, 72, 0.18);    /* Houm Green tint */
```

---

## When to Use This Skill

Use this skill when:
- Designing web UI or interfaces for Houm services
- Creating landing pages or marketing materials for Houm
- Building React-based web applications for Houm
- Designing static visual materials (posters, graphics, PDFs)
- Creating internal tools or dashboards for Houm staff
- Any design work that should reflect Houm's brand identity

## Houm's Brand Identity

### Etymology

`Houm` / `호움` is built from two morphemes:

- **호 (戶)** — household, the dwelling that shelters a family
- **움** — a new sprout, the bud of a fresh life

Together: **"the birth of a family."** The English transliteration also evokes "home," reinforcing the same idea.

### Brand Slogan

> "출산 그 너머, 한 생명을 봅니다. 한 생애가 옵니다."
>
> *Beyond birth, we see a life. A lifetime arrives.*

The slogan signals that Houm's care extends past the delivery moment — it honors the arrival of a person and the family transformation around them.

### Core Brand Values (from the 2019 brand book)

The four canonical values, in the original order:

1. **생명 (Life)** — Honoring every life that enters the world; respecting birth as a meaningful arrival, not a clinical procedure.
2. **관계 (Relationship)** — Treating birth as a relational event for the baby, parents, and supporting team — a moment that recalibrates how people relate to themselves and each other.
3. **결속 (Bonding)** — Protecting the earliest hours of life as the foundation for attachment and the capacity to form healthy relationships.
4. **회복 (Recovery)** — Centering the rebirth of the family unit; postpartum is not a return to baseline but the start of a new equilibrium.

### Design Principles (operational guidance for digital work)

These translate the four values into design decisions:

1. **Full and Informed Consent on Birth** — Promote transparency, clear communication, and understanding. Use clear information hierarchy, readable typography, intuitive navigation.

2. **Holistic Evidence-Based Approach** — Feel professional, trustworthy, grounded. Use structured layouts, credible visual language, evidence-based design patterns.

3. **Team up with Companions** — Feel collaborative, warm, supportive. Use inclusive imagery, friendly interactions, partnership-focused messaging.

4. **Pay Close Attention to Intervention** — Be thoughtful, intentional, natural. Avoid over-design; embrace simplicity and purposeful choices.

### Brand Colors

See **Canonical Colors** above for the authoritative palette. Summary of the brand book intent:

- **Houm Green (`#3D7E48`, Pantone 7731C)** — the identity color. Used for the brand wordmark, primary buttons, key headings, and action accents. Carries the brand's meaning of vitality, recovery, and calm.
- **Houm Beige (`#F0E5C4`, Pantone 7499C)** — the canonical background. A warm cream that softens the green and conveys hospitality.
- **Houm Baby Green (`#D6A93B`, Pantone 110C)** — a mustard accent for warmth and highlight. Use sparingly for badges, soft highlights, and editorial flourishes — not for primary CTAs.
- **Houm Baby Blue (`#B4D0E7`, Pantone 277C)** — a soft sky accent for calm and care. Useful for gentle notifications, baby-related sections, and quiet emphasis.

**Usage Guidelines:**
- **Green for identity and action** — wordmark, primary buttons, headings, links, progress indicators.
- **Mustard for warmth and emphasis** — small badges, accent strokes, "tip" callouts. Never as a primary action color.
- **Soft blue for calm and category** — newborn/baby content, calm informational areas, secondary tags.
- **Beige as the unifying ground** — use as the page background; cards float on top in white or beige-soft.
- Maintain WCAG AA contrast (4.5:1 for body, 3:1 for large text).

**Color Pairing Examples:**
- Hero: Houm Beige background + Houm Green framed wordmark + dark text + green CTA.
- Cards: White surface on beige background + green primary button + mustard "new" badge.
- Newborn / baby-specific module: soft-blue background tint + green headings + dark text.

### Typography

**Canonical Fonts (Web Applications):**
See "Canonical Design System" above for THE standard. Summary:

- **English Primary**: Sanchez (slab serif) — headings, body, brand wordmark
- **Korean Primary**: 나눔명조 (Nanum Myeongjo) — headings
- **English Secondary**: Noto Sans — long-form body, dense text
- **Korean Secondary**: KoPub돋움체 (KoPub Dotum) — long-form body

**Typography Principles:**
- Use clear, readable font sizes (minimum 16px for body text).
- Maintain good line height (1.5–1.7 for EN, 1.6–1.7 for KO — Hangul needs a bit more leading).
- Use font weight to create hierarchy (700 for KO headings in Nanum Myeongjo, 400 for Sanchez headings — Sanchez has only one weight).
- For mixed EN/KO lines, prefer the same tier across both languages (don't pair Sanchez with KoPub Dotum on the same heading).
- Avoid decorative fonts; prioritize clarity and accessibility.

**Canvas Fonts for Static Designs (Posters, PDFs):**
When creating posters, graphics, or PDF designs, use fonts from the `canvas-fonts/` directory.

**Primary Choice (matches the 2019 brand book):**
- A slab serif close in feel to Sanchez (e.g. **Roboto Slab**, **CrimsonPro** for editorial variants).

**Alternative Fonts (for variety in static designs only):**
- **Lora** (Regular, Bold, Italic, BoldItalic) — warm serif, useful when Sanchez is unavailable.
- **WorkSans** (Regular, Bold, Italic, BoldItalic) — friendly sans, substitutes for Noto Sans in print.
- **InstrumentSans** (Regular, Bold, Italic, BoldItalic) — clean modern sans.
- **Outfit** (Regular, Bold) — modern, approachable sans.
- **InstrumentSerif** (Regular, Italic) — refined serif for sophisticated touches.
- **CrimsonPro** (Regular, Bold, Italic) — elegant serif for editorial content.
- **LibreBaskerville** (Regular) — kept for legacy alignment; not the canonical brand serif.

**Font Pairing for Static Designs:**
- **Canonical-aligned**: Sanchez-like slab (or CrimsonPro) for headings + WorkSans for body.
- **Editorial**: CrimsonPro (headings) + InstrumentSans (body).
- **Modern warm**: Lora (headings) + WorkSans (body).

### Design Aesthetic

**Visual Philosophy: "Nurturing Clarity"**

Houm's design aesthetic combines the professionalism of healthcare with the warmth of home care. The philosophy emphasizes:

- **Natural Forms**: Organic shapes, gentle curves, breathing room
- **Calm Palette**: Green-centered color harmony evoking growth and healing
- **Clear Communication**: Strong information hierarchy, readable typography
- **Warm Professionalism**: Trustworthy yet approachable visual language
- **Purposeful Simplicity**: Every element serves a clear function
- **Accessible Design**: High contrast, clear labels, intuitive interactions

**Design Don'ts (Avoiding "AI Slop"):**
- ❌ Excessive centered layouts
- ❌ Purple gradients or neon colors
- ❌ Uniform rounded corners everywhere
- ❌ Generic geometric sans (Inter, etc.) used flat across the whole page — the brand voice is editorial, not techy
- ❌ Generic stock imagery
- ❌ Overly complex animations
- ❌ Cluttered interfaces

**Design Do's:**
- ✅ Asymmetric, intentional layouts
- ✅ Green-based natural color palette
- ✅ Varied border radius (subtle where needed)
- ✅ Typography hierarchy with different weights
- ✅ Authentic, relevant imagery
- ✅ Subtle, purposeful micro-interactions
- ✅ Clean, focused interfaces

## How to Use This Skill

The houmlike-design skill supports two primary workflows:

### 1. Building React-Based Web Artifacts

To create interactive web applications, dashboards, or complex interfaces:

**Step 1: Initialize Project**
```bash
bash scripts/init-artifact.sh <project-name>
cd <project-name>
```

This creates a React + TypeScript + Vite + Tailwind CSS + shadcn/ui project with Houm's design system pre-configured.

**Step 2: Develop the Artifact**
Edit the generated files to build the interface. Apply Houm's brand colors and design principles throughout. See the Tailwind configuration for Houm's color variables.

**Step 3: Bundle to Single HTML File**
```bash
bash scripts/bundle-artifact.sh
```

This creates `bundle.html` - a self-contained artifact ready to share.

**Step 4: Share with User**
Present the bundled HTML file so it can be viewed as an artifact.

**Technical Stack:**
- React 18 + TypeScript + Vite
- Tailwind CSS 3.4.1 (with Houm color palette)
- shadcn/ui components
- Parcel for bundling

### 2. Creating Static Design Artifacts

To create visual designs, posters, graphics, or static materials:

**Step 1: Define Design Intent**
Understand the purpose, audience, and key message of the design.

**Step 2: Select Houm-Appropriate Fonts**
Use fonts from the `canvas-fonts/` directory. Recommended pairings (slab/serif headings + clean sans body, in line with the 2019 brand book):
- **Canonical-aligned**: CrimsonPro or LibreBaskerville (heading) + WorkSans (body)
- **Editorial Elegance**: CrimsonPro + InstrumentSerif
- **Modern Warmth**: Lora + WorkSans
- **Modern Approachable**: Outfit + WorkSans (for lighter, casual collateral)

All fonts support Regular, Bold, and Italic variants for versatile typography. The canvas-fonts set does not ship Sanchez itself — substitute the slab/serif heading fonts above when working without web font access.

**Step 3: Apply "Nurturing Clarity" Philosophy**
Use Houm's green palette, clean typography, and purposeful layouts. Emphasize:
- Visual hierarchy through color and scale
- Breathing room and whitespace
- Natural, organic visual elements
- Clear, accessible communication

**Step 4: Create Visual Output**
Generate PNG or PDF files using Houm's brand colors and design aesthetic. Ensure all designs:
- Use the Houm palette: Green `#3D7E48` (Pantone 7731C), Beige `#F0E5C4` (Pantone 7499C), Baby Green/mustard `#D6A93B` (Pantone 110C), Baby Blue `#B4D0E7` (Pantone 277C)
- Use fonts from `canvas-fonts/` directory for consistent branding (slab/serif heading + clean sans body)
- Maintain high contrast for readability (WCAG AA)
- Reflect maternity care values (warm, professional, supportive)
- Avoid AI slop patterns (see Design Don'ts above)

## Design Components Library

When building React artifacts, leverage these shadcn/ui components styled with Houm's brand:

**Layout**: Card, Container, Separator
**Navigation**: Navigation Menu, Breadcrumb, Tabs
**Forms**: Input, Textarea, Select, Checkbox, Radio Group, Switch
**Feedback**: Alert, Toast, Dialog, Progress
**Data Display**: Table, Badge, Avatar

**Component Styling Guidelines:**
- Primary buttons: `bg-[#3D7E48]` with `hover:bg-[#2F6238]` (Houm Green / Houm Green Dark)
- Secondary buttons: `bg-[#8FB498]` with `hover:bg-[#3D7E48]` (Houm Green Light → Houm Green)
- Page background: Use `bg-[#F0E5C4]` (Houm Beige) or `bg-[#F5EFDF]` (Beige Soft)
- Card surface: `bg-white` floating on the beige page
- Borders: Use `border-[#E4EBE4]` (divider) or `border-[#8FB498]` (green hairline)
- Text: Use `text-[#3D7E48]` for brand headers, `text-[#1F2937]` for body, `text-[#6B7280]` for muted
- Accent badges: `bg-[#D6A93B]` (Baby Green / mustard) for highlights, `bg-[#B4D0E7]` (Baby Blue) for calm/baby categories

## Accessibility Standards

All Houm designs must meet accessibility requirements:

- ✅ WCAG 2.1 AA compliance minimum
- ✅ Color contrast ratios of 4.5:1 for body text, 3:1 for large text
- ✅ Keyboard navigation support
- ✅ Screen reader compatibility
- ✅ Clear focus states
- ✅ Semantic HTML structure
- ✅ Alt text for all images
- ✅ Form labels and error messages

## Examples

**Example 1: Landing Page for Maternity Services**
Create a React-based landing page highlighting Houm's pregnancy care services. Use Houm Beige (`#F0E5C4`) for the page, white cards floating on top, Houm Green (`#3D7E48`) for headings and CTAs, and a single mustard (`#D6A93B`) badge to mark a "New" feature. The framed `Houm®` wordmark sits at top-left of the header. EN headings use Sanchez; KO headings use Nanum Myeongjo.

**Example 2: Internal Dashboard for Healthcare Providers**
Build a React dashboard for Houm staff to track patient care. Beige page background, white card surfaces, Houm Green status indicators, and Baby Blue (`#B4D0E7`) tints for newborn-related panels. Prioritize information hierarchy and quick access to key metrics. Use Noto Sans / KoPub돋움체 for the dense data text.

**Example 3: Educational Poster about Informed Consent**
Design a static PDF poster using the "Nurturing Clarity" philosophy. Use a slab serif (Sanchez, or CrimsonPro/Roboto Slab if Sanchez is unavailable from `canvas-fonts/`) Bold for the main heading in Houm Green Dark (`#2F6238`), and WorkSans Regular for body text. Background in Houm Beige (`#F0E5C4`). One mustard accent stroke to draw the eye to the key statistic. One message, lots of breathing room.

## Quality Standards

Every Houm design should:

1. **Reflect Brand Values** - Embody informed consent, evidence-based care, collaboration, and mindful intervention
2. **Use Brand Colors Consistently** - Apply Houm's green palette appropriately
3. **Maintain Professional Quality** - Appear polished, intentional, and expert-crafted
4. **Prioritize Accessibility** - Meet WCAG standards for inclusive design
5. **Avoid AI Slop** - Follow design best practices, not generic AI patterns
6. **Serve a Clear Purpose** - Every element should have a function
7. **Feel Warm Yet Professional** - Balance healthcare credibility with human warmth

## Resources

- **Brand Assets**: `assets/` directory contains:
  - `houm-mark.svg` — canonical framed `Houm®` wordmark, currentColor-driven (inline the SVG for theming)
  - `brand-mark-construction.png` — reference render of the construction grid + ® placement
  - `brand-palette.png` — reference render of the official mark on Houm Green / Houm Beige / Houm Baby Green / Houm Baby Blue
- **Canvas Fonts**: `canvas-fonts/` directory contains 7 curated font families (Lora, InstrumentSans, InstrumentSerif, WorkSans, Outfit, CrimsonPro, LibreBaskerville) for static design artifacts. The canonical brand serif (Sanchez) and Korean serif (Nanum Myeongjo) are not yet bundled — load via Google Fonts for web work, or substitute with CrimsonPro / Roboto Slab for static design.
- **Operational Document Typography**: `references/document-typography.md` records the Korean/bilingual font selection and PDF preflight rules derived from Houm's maintained document artifacts.
- **Scripts**: `scripts/init-artifact.sh`, `scripts/bundle-artifact.sh` for React artifact workflow
- **Houm Website**: https://houmclinic.com/main/ for brand reference
- **shadcn/ui Docs**: https://ui.shadcn.com/docs/components for component reference
