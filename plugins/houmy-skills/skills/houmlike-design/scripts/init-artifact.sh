#!/bin/bash
# Scaffold a Houm-branded React artifact.
#   React 19 + TypeScript + Vite + Tailwind CSS v4 (CSS-first) + shadcn/ui
# Houm design tokens, both themes, Korean typography, and the accessibility
# floor are written into src/index.css.

set -euo pipefail

usage() {
  cat <<'USAGE'
Usage: init-artifact.sh <project-name> [--skip-shadcn]

  --skip-shadcn   Scaffold Vite + Tailwind + Houm tokens only. Use when the
                  shadcn registry is unreachable, or when the artifact does
                  not need component primitives.
USAGE
}

PROJECT_NAME=""
SKIP_SHADCN=0
for arg in "$@"; do
  case "$arg" in
    --skip-shadcn) SKIP_SHADCN=1 ;;
    -h|--help) usage; exit 0 ;;
    -*) echo "Unknown option: $arg" >&2; usage; exit 1 ;;
    *)
      if [ -z "$PROJECT_NAME" ]; then
        PROJECT_NAME="$arg"
      else
        echo "Unexpected argument: $arg" >&2; exit 1
      fi
      ;;
  esac
done

if [ -z "$PROJECT_NAME" ]; then usage; exit 1; fi
if [ -e "$PROJECT_NAME" ]; then
  echo "Error: '$PROJECT_NAME' already exists." >&2
  exit 1
fi

# Node 20 is the floor. Node 18 reached end of life in April 2025, and neither
# Vite 8 nor the Tailwind v4 toolchain supports it.
NODE_MAJOR=$(node -v | cut -d'v' -f2 | cut -d'.' -f1)
if [ "$NODE_MAJOR" -lt 20 ]; then
  echo "Error: Node.js 20 or higher is required (found $(node -v))." >&2
  exit 1
fi

if ! command -v pnpm >/dev/null 2>&1; then
  echo "Error: pnpm is required. Install it with 'corepack enable' or 'npm i -g pnpm'." >&2
  exit 1
fi

echo "Creating Vite project: $PROJECT_NAME"
pnpm create vite "$PROJECT_NAME" --template react-ts
cd "$PROJECT_NAME"

echo "Installing dependencies"
pnpm install

# Tailwind v4 is CSS-first: no tailwind.config.js, no PostCSS, no Autoprefixer.
echo "Installing Tailwind CSS v4"
pnpm add tailwindcss @tailwindcss/vite tw-animate-css
pnpm add -D @types/node vite-plugin-singlefile

echo "Writing vite.config.ts"
cat > vite.config.ts <<'VITECONFIG'
import { fileURLToPath } from "node:url";
import react from "@vitejs/plugin-react";
import tailwindcss from "@tailwindcss/vite";
import { viteSingleFile } from "vite-plugin-singlefile";
import { defineConfig } from "vite";

// bundle-artifact.sh sets this to inline everything into one dist/index.html.
const singleFile = process.env.HOUM_SINGLE_FILE === "1";

export default defineConfig({
  plugins: [
    react(),
    tailwindcss(),
    ...(singleFile ? [viteSingleFile({ removeViteModuleLoader: true })] : []),
  ],
  resolve: {
    // Not __dirname: Vite 8's native config loader warns on it in ESM.
    alias: { "@": fileURLToPath(new URL("./src", import.meta.url)) },
  },
});
VITECONFIG

echo "Adding the @/* path alias"
node -e '
const fs = require("node:fs");
const strip = (s) =>
  s.split("\n").filter((l) => !l.trim().startsWith("//")).join("\n")
   .replace(/\/\*[\s\S]*?\*\//g, "")
   .replace(/,(\s*[}\]])/g, "$1");
for (const file of ["tsconfig.json", "tsconfig.app.json"]) {
  if (!fs.existsSync(file)) continue;
  const config = JSON.parse(strip(fs.readFileSync(file, "utf8")));
  config.compilerOptions = config.compilerOptions || {};
  // No baseUrl: it is deprecated as of TypeScript 7 and paths already
  // resolve relative to this tsconfig.
  delete config.compilerOptions.baseUrl;
  config.compilerOptions.paths = { "@/*": ["./src/*"] };
  fs.writeFileSync(file, JSON.stringify(config, null, 2) + "\n");
}
'

echo "Setting the Tailwind entry stylesheet"
printf '@import "tailwindcss";\n' > src/index.css

echo "Cleaning the Vite template"
# The template's icon has been vite.svg and favicon.svg at different versions.
sed -i.bak '/<link rel="icon"/d' index.html
sed -i.bak "s|<title>.*</title>|<title>${PROJECT_NAME}</title>|" index.html
sed -i.bak 's|<html lang="en">|<html lang="ko">|' index.html
rm -f index.html.bak src/App.css public/vite.svg public/favicon.svg

COMPONENTS="alert avatar badge button card checkbox dialog dropdown-menu
input label popover progress radio-group select separator sheet
skeleton sonner switch table tabs textarea tooltip"

if [ "$SKIP_SHADCN" -eq 0 ]; then
  # Fetched from the registry at scaffold time, so components arrive current
  # instead of frozen. The CLI wires the unified radix-ui package itself.
  #
  # Every flag here is load-bearing, and -y alone is NOT enough:
  #   -b radix  answers "Select a component library"
  #   -d        answers "Which preset would you like to use?" (Nova)
  #   -y        skips the final confirmation
  # Miss either of the first two and the CLI renders a prompt, reads no input,
  # and EXITS 0 having written nothing. So do not trust the exit code below.
  echo "Initializing shadcn/ui"
  pnpm dlx shadcn@latest init -b radix -d -y </dev/null || true

  if [ ! -f components.json ] || [ ! -f src/lib/utils.ts ]; then
    echo "" >&2
    echo "shadcn init produced no components.json. It most likely hit an" >&2
    echo "interactive prompt this script does not answer." >&2
    echo "Run it yourself and pick the options:" >&2
    echo "  cd $PROJECT_NAME && pnpm dlx shadcn@latest init" >&2
    echo "Or re-scaffold with --skip-shadcn to omit component primitives." >&2
    exit 1
  fi

  echo "Adding component primitives"
  # shellcheck disable=SC2086
  pnpm dlx shadcn@latest add -y $COMPONENTS </dev/null || true

  MISSING=""
  for component in $COMPONENTS; do
    [ -f "src/components/ui/${component}.tsx" ] || MISSING="$MISSING $component"
  done
  if [ -n "$MISSING" ]; then
    echo "" >&2
    echo "shadcn add did not write:$MISSING" >&2
    echo "Add them with:  cd $PROJECT_NAME && pnpm dlx shadcn@latest add$MISSING" >&2
    exit 1
  fi
  echo "  $(ls src/components/ui | wc -l | tr -d ' ') components in src/components/ui"
fi

echo "Appending Houm design tokens"
cat >> src/index.css <<'HOUMCSS'

/* ------------------------------------------------------------------------
   Houm design tokens.

   Appended after the shadcn/ui block so these values win. Every ratio noted
   below is the WORST case across the three light grounds (#F0E5C4, #F5EFDF,
   #FFFFFF) or the four operator grounds. Re-verify with the skill's
   scripts/check-contrast.mjs after changing any value.
   ------------------------------------------------------------------------ */

@theme {
  /* Grounds */
  --color-houm-canvas:           #f0e5c4;
  --color-houm-surface:          #ffffff;
  --color-houm-surface-soft:     #f5efdf;

  /* Ink */
  --color-houm-text:             #1f2937; /* 11.68 on canvas */
  --color-houm-text-muted:       #5a6560; /*  4.82 worst */

  /* Lines */
  --color-houm-border:           #71806f; /*  3.33 worst; control boundaries */
  --color-houm-hairline:         #e4ebe4; /*  1.04; decoration only */

  /* Identity. Green is a fill; green-strong is the text-safe green. */
  --color-houm-green:            #3d7e48; /* white on it: 4.91 */
  --color-houm-green-strong:     #2f6238; /* 5.71 as text, 7.18 with white on it */
  --color-houm-green-tint:       #8fb498; /* tint only; never text, never a border */

  /* Accents. Role names, not subject names. Fills and tints only. */
  --color-houm-accent-warm:      #d6a93b; /* houm-text on it:  6.71 */
  --color-houm-accent-warm-soft: #e8c97a; /* houm-text on it:  9.13 */
  --color-houm-accent-warm-text: #6e5210; /* 5.81 worst */
  --color-houm-accent-cool:      #b4d0e7; /* houm-text on it:  9.17 */
  --color-houm-accent-cool-soft: #d6e5f2; /* houm-text on it: 11.43 */
  --color-houm-accent-cool-text: #1b5478; /* 6.46 worst */

  /* Status. A separate axis from the brand accent. */
  --color-houm-success:          #2f6238;
  --color-houm-warning:          #6e5210;
  --color-houm-danger:           #a02017;
  --color-houm-info:             #1b5478;

  /* Operator theme. Dark and dense, for internal consoles. */
  --color-op-canvas:             #08100c;
  --color-op-surface:            #0f1512;
  --color-op-surface-raised:     #131a16;
  --color-op-surface-card:       #151c18;
  --color-op-surface-hover:      #1b241e;
  --color-op-text:               #e7ede8; /* 13.41 worst */
  --color-op-text-secondary:     #c3d1c7; /* 10.07 worst */
  --color-op-text-muted:         #94a89a; /*  6.32 worst */
  --color-op-text-faint:         #7e9184; /*  4.76 worst */
  --color-op-border-control:     #6a7a6c; /*  3.50 worst */
  --color-op-divider:            #263028; /*  1.35; decoration only */
  --color-op-green:              #57a867;
  --color-op-green-light:        #8fcb9b;
  --color-op-mustard-text:       #e2c078;
  --color-op-blue-text:          #bfd8ec;
  --color-op-red-text:           #e7a392;

  /* Type. Sanchez ships weight 400 only; there is no Sanchez Bold.
     Each stack carries BOTH scripts in the same brand tier: Sanchez covers
     Latin and Nanum Myeongjo covers Hangul, because a Latin-only face does
     not fail loudly on Korean text -- it silently falls back to whatever
     system face has the glyphs, and the page renders in a font nobody chose. */
  --font-display:    "Sanchez", "Nanum Myeongjo", "Roboto Slab", "Noto Serif KR", Georgia, serif;
  --font-body:       "Noto Sans", "Pretendard Variable", Pretendard, "Noto Sans KR", system-ui, sans-serif;
  --font-ko:         "Pretendard Variable", Pretendard, "Noto Sans KR", system-ui, sans-serif;
  --font-ko-display: "Nanum Myeongjo", "Noto Serif KR", serif;

  /* Radius varies by role. Uniform rounding reads as generated. */
  --radius-btn:   12px;
  --radius-card:  16px;
  --radius-input: 8px;

  --shadow-soft:   0 2px 8px rgb(0 0 0 / 8%);
  --shadow-medium: 0 4px 16px rgb(0 0 0 / 12%);

  --ease-out:    cubic-bezier(0.16, 1, 0.3, 1);
  --ease-in-out: cubic-bezier(0.65, 0, 0.35, 1);
}

@layer base {
  :root { color-scheme: light; }

  /* The page composites over a ground the host paints in its own theme, so
     body must set an explicit background or it silently borrows the host's. */
  body {
    background: var(--color-houm-canvas);
    color: var(--color-houm-text);
    font-family: var(--font-body);
  }

  /* Korean line breaking. Without keep-all, browsers break Hangul between
     syllable blocks, which native readers read as broken text. overflow-wrap
     is the safety valve for a long token with no spaces. */
  :lang(ko) {
    word-break: keep-all;
    overflow-wrap: anywhere;
    line-break: strict;
    font-family: var(--font-ko);
    line-height: 1.7;
    letter-spacing: 0;
  }

  :lang(ko) h1,
  :lang(ko) h2,
  :lang(ko) h3 {
    font-family: var(--font-ko-display);
    line-height: 1.4;
    letter-spacing: -0.02em;
  }

  h1, h2, h3 { text-wrap: balance; }
  p { text-wrap: pretty; }

  /* WCAG 2.2 SC 2.4.11 also requires this never be fully obscured by a
     sticky header. Give scroll containers scroll-padding-block-start. */
  :focus-visible {
    outline: 2px solid var(--color-houm-green-strong);
    outline-offset: 2px;
    border-radius: inherit;
  }
  :focus:not(:focus-visible) { outline: none; }

  /* WCAG 2.2 SC 2.5.8: pointer targets at least 24x24 CSS px. */
  button, [role="button"], input, select, textarea, summary {
    min-block-size: 24px;
  }

  table { font-variant-numeric: tabular-nums; }
}

/* Operator theme. Chosen by the surface's job, not the viewer's OS setting:
   an internal console stays dark for a viewer who prefers light, and a
   marketing page stays warm for a viewer who prefers dark. */
@layer base {
  :root[data-theme="operator"] { color-scheme: dark; }

  :root[data-theme="operator"] body {
    background: var(--color-op-canvas);
    color: var(--color-op-text);
    font-family: var(--font-ko);
  }

  :root[data-theme="operator"] :focus-visible {
    outline-color: var(--color-op-green-light);
  }
}

@media (prefers-reduced-motion: reduce) {
  *, *::before, *::after {
    animation-duration: 0.01ms !important;
    animation-iteration-count: 1 !important;
    transition-duration: 0.01ms !important;
    scroll-behavior: auto !important;
  }
}

/* Windows High Contrast strips author colours. Anything that turns ambiguous
   here was relying on colour alone and needs a second channel. */
@media (forced-colors: active) {
  :focus-visible { outline-color: Highlight; }
}
HOUMCSS

echo "Adding web fonts"
node -e '
const fs = require("node:fs");
const links = [
  "<link rel=\"preconnect\" href=\"https://fonts.googleapis.com\" />",
  "<link rel=\"preconnect\" href=\"https://fonts.gstatic.com\" crossorigin />",
  "<link rel=\"stylesheet\" href=\"https://fonts.googleapis.com/css2?family=Sanchez:ital@0;1&family=Nanum+Myeongjo:wght@400;700;800&family=Noto+Sans:wght@400;500;700&display=swap\" />",
  "<link rel=\"stylesheet\" href=\"https://cdn.jsdelivr.net/gh/orioncactus/pretendard@v1.3.9/dist/web/variable/pretendardvariable-dynamic-subset.min.css\" />",
].map((l) => "    " + l).join("\n");
const html = fs.readFileSync("index.html", "utf8")
  .replace(/[ \t]*<\/head>/, links + "\n  </head>");
fs.writeFileSync("index.html", html);
'

cat > src/App.tsx <<'APPTSX'
export default function App() {
  return (
    <main className="mx-auto flex min-h-dvh max-w-2xl flex-col justify-center gap-6 p-8">
      <span className="self-start rounded-[3px] border-[1.5px] border-current px-3 py-1.5 font-display text-2xl leading-none text-houm-green-strong">
        Houm<sup className="ml-0.5 align-super text-[0.42em]">&reg;</sup>
      </span>

      <div className="rounded-card bg-houm-surface p-8 shadow-soft">
        <h1 className="font-display text-3xl text-houm-green-strong">
          디자인 시스템이 연결되었습니다
        </h1>
        <p className="mt-3 text-houm-text-muted">
          토큰, 두 가지 테마, 한글 조판 규칙, 접근성 기준선이 모두 적용된
          상태입니다. <code>src/index.css</code> 끝부분에서 확인하세요.
        </p>

        <div className="mt-6 flex flex-wrap items-center gap-3">
          <button className="rounded-btn bg-houm-green px-5 py-2.5 font-medium text-white transition-colors hover:bg-houm-green-strong">
            기본 동작
          </button>
          <button className="rounded-btn border border-houm-border px-5 py-2.5 font-medium text-houm-green-strong">
            보조 동작
          </button>
          <span className="rounded-full bg-houm-accent-warm px-3 py-1 text-sm text-houm-text">
            강조
          </span>
          <span className="rounded-full bg-houm-accent-cool px-3 py-1 text-sm text-houm-text">
            확인됨
          </span>
        </div>
      </div>
    </main>
  );
}
APPTSX

cat > HOUM.md <<'HOUMMD'
# Houm design system

Tokens live at the end of `src/index.css`. Read the `houmlike-design` skill
before changing them.

## Colour roles are binding

A brand colour is not automatically a text colour.

- `houm-green` is an **action fill**. White on it measures 4.91. As body text
  on the beige canvas it measures 3.91 and fails AA.
- `houm-green-strong` is the **text-safe green** on any light ground (5.71).
- `houm-green-tint`, `houm-accent-warm`, and `houm-accent-cool` are **fills and
  tints only**. Put `houm-text` on them, never white.
- `houm-border` is for **control boundaries** (3.33, clearing WCAG 1.4.11).
  `houm-hairline` is decoration and measures 1.04 on the canvas.

## Themes

The brand theme is the default. Set `data-theme="operator"` on the root element
for the dark, dense internal-console theme. Choose by the surface's job, not by
the viewer's OS preference.

## Before shipping

    node <skill-path>/scripts/check-contrast.mjs --palette

Then the manual pass: tab through the page, zoom to 400%, check forced colours,
check reduced motion, and confirm Korean wraps at word boundaries at the
narrowest supported width. See the skill's `references/accessibility.md`.
HOUMMD

echo ""
echo "Done. $PROJECT_NAME is ready."
echo ""
echo "  cd $PROJECT_NAME"
echo "  pnpm dev"
echo ""
echo "Tokens: src/index.css    Notes: HOUM.md"
echo "Bundle: bash <skill-path>/scripts/bundle-artifact.sh"
