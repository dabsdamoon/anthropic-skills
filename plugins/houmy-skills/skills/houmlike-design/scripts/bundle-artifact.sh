#!/bin/bash
# Bundle a Houm React artifact into one self-contained HTML file.
#
# Uses vite-plugin-singlefile, which the project's own vite.config.ts enables
# when HOUM_SINGLE_FILE=1. There is no second bundler and no second config.

set -euo pipefail

if [ ! -f "package.json" ]; then
  echo "Error: no package.json here. Run this from the project root." >&2
  exit 1
fi

if [ ! -f "index.html" ]; then
  echo "Error: no index.html here. This build needs an HTML entry point." >&2
  exit 1
fi

if ! grep -q "HOUM_SINGLE_FILE" vite.config.ts 2>/dev/null; then
  echo "Error: vite.config.ts does not read HOUM_SINGLE_FILE." >&2
  echo "This project was not scaffolded by init-artifact.sh. Add the plugin:" >&2
  echo "" >&2
  echo "  import { viteSingleFile } from \"vite-plugin-singlefile\";" >&2
  echo "  plugins: [..., ...(process.env.HOUM_SINGLE_FILE === \"1\" ? [viteSingleFile({ removeViteModuleLoader: true })] : [])]" >&2
  exit 1
fi

echo "Cleaning previous build"
rm -rf dist

echo "Building"
HOUM_SINGLE_FILE=1 pnpm exec vite build

if [ ! -f "dist/index.html" ]; then
  echo "Error: build finished but dist/index.html is missing." >&2
  exit 1
fi

# The whole point is one file. A stray asset only matters if index.html still
# points at it — an unreferenced copy (shadcn presets drop one in public/) is
# harmless, so check references rather than crying wolf over every file.
REFERENCED=""
UNREFERENCED=""
while IFS= read -r asset; do
  [ -n "$asset" ] || continue
  if grep -qF "$(basename "$asset")" dist/index.html; then
    REFERENCED="$REFERENCED  $asset"$'\n'
  else
    UNREFERENCED="$UNREFERENCED  $asset"$'\n'
  fi
done <<EOF
$(find dist -type f ! -name "index.html")
EOF

if [ -n "$REFERENCED" ]; then
  echo "" >&2
  echo "dist/index.html is NOT self-contained. It still references:" >&2
  printf "%s" "$REFERENCED" >&2
  echo "" >&2
  echo "Common causes: an asset over the inline size limit, or a runtime" >&2
  echo "fetch() of a file in public/. Embed it as a data: URI or import it" >&2
  echo "so the bundler can inline it." >&2
  exit 1
fi

if [ -n "$UNREFERENCED" ]; then
  echo ""
  echo "Note: the build copied files nothing references. index.html is still"
  echo "self-contained; ship it alone and drop these."
  printf "%s" "$UNREFERENCED"
fi

SIZE=$(du -h dist/index.html | cut -f1)
echo ""
echo "Done. dist/index.html ($SIZE)"
echo ""
echo "Open it directly in a browser, or share it as an artifact."
echo "Before sharing, check contrast and the accessibility pass:"
echo "  node <skill-path>/scripts/check-contrast.mjs --palette"
