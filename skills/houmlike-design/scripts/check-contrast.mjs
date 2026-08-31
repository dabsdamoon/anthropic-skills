#!/usr/bin/env node
// Measure WCAG contrast for the Houm palette.
//
//   node check-contrast.mjs "#2F6238" "#F0E5C4"   one pair
//   node check-contrast.mjs --palette             audit every declared role
//
// --palette exits 1 if any declared role fails its own duty, so it can gate CI.

const HELP = `Usage:
  check-contrast.mjs <foreground> <background> [--large|--nontext]
  check-contrast.mjs --palette

  --large     grade against 3.0 (18.66px bold or 24px text)
  --nontext   grade against 3.0 (control boundaries, meaningful graphics)
  --palette   audit the full Houm palette and exit non-zero on any failure
`;

function parseHex(value) {
  let hex = String(value).trim().replace(/^#/, "");
  if (hex.length === 3) hex = [...hex].map((c) => c + c).join("");
  if (!/^[0-9a-fA-F]{6}$/.test(hex)) {
    throw new Error(`Not a hex colour: ${value}`);
  }
  return [0, 2, 4].map((i) => parseInt(hex.slice(i, i + 2), 16));
}

function relativeLuminance(hex) {
  const [r, g, b] = parseHex(hex).map((channel) => {
    const c = channel / 255;
    return c <= 0.03928 ? c / 12.92 : ((c + 0.055) / 1.055) ** 2.4;
  });
  return 0.2126 * r + 0.7152 * g + 0.0722 * b;
}

export function contrast(a, b) {
  const [hi, lo] = [relativeLuminance(a), relativeLuminance(b)].sort((x, y) => y - x);
  return (hi + 0.05) / (lo + 0.05);
}

// The grounds a foreground must survive. A token is only as good as its worst.
const LIGHT_GROUNDS = {
  canvas: "#f0e5c4",
  "surface-soft": "#f5efdf",
  surface: "#ffffff",
};

const OPERATOR_GROUNDS = {
  surface: "#0f1512",
  raised: "#131a16",
  card: "#151c18",
  hover: "#1b241e",
};

// duty: "text" needs 4.5, "large" and "nontext" need 3.0, "decor" is exempt.
// on: an explicit background, used where the token is a fill rather than ink.
const PALETTE = [
  { token: "--houm-text", hex: "#1f2937", grounds: LIGHT_GROUNDS, duty: "text" },
  { token: "--houm-text-muted", hex: "#5a6560", grounds: LIGHT_GROUNDS, duty: "text" },
  { token: "--houm-green-strong", hex: "#2f6238", grounds: LIGHT_GROUNDS, duty: "text" },
  { token: "--houm-accent-warm-text", hex: "#6e5210", grounds: LIGHT_GROUNDS, duty: "text" },
  { token: "--houm-accent-cool-text", hex: "#1b5478", grounds: LIGHT_GROUNDS, duty: "text" },
  { token: "--houm-success-text", hex: "#2f6238", grounds: LIGHT_GROUNDS, duty: "text" },
  { token: "--houm-warning-text", hex: "#6e5210", grounds: LIGHT_GROUNDS, duty: "text" },
  { token: "--houm-danger-text", hex: "#a02017", grounds: LIGHT_GROUNDS, duty: "text" },
  { token: "--houm-info-text", hex: "#1b5478", grounds: LIGHT_GROUNDS, duty: "text" },
  { token: "--houm-border", hex: "#71806f", grounds: LIGHT_GROUNDS, duty: "nontext" },
  { token: "--houm-hairline", hex: "#e4ebe4", grounds: LIGHT_GROUNDS, duty: "decor" },

  { token: "white on --houm-green", hex: "#ffffff", on: { fill: "#3d7e48" }, duty: "text" },
  { token: "white on --houm-green-strong", hex: "#ffffff", on: { fill: "#2f6238" }, duty: "text" },
  { token: "--houm-text on --houm-accent-warm", hex: "#1f2937", on: { fill: "#d6a93b" }, duty: "text" },
  { token: "--houm-text on --houm-accent-warm-soft", hex: "#1f2937", on: { fill: "#e8c97a" }, duty: "text" },
  { token: "--houm-text on --houm-accent-cool", hex: "#1f2937", on: { fill: "#b4d0e7" }, duty: "text" },
  { token: "--houm-text on --houm-accent-cool-soft", hex: "#1f2937", on: { fill: "#d6e5f2" }, duty: "text" },
  { token: "--houm-text on --houm-green-tint", hex: "#1f2937", on: { fill: "#8fb498" }, duty: "text" },

  { token: "--op-text", hex: "#e7ede8", grounds: OPERATOR_GROUNDS, duty: "text" },
  { token: "--op-text-secondary", hex: "#c3d1c7", grounds: OPERATOR_GROUNDS, duty: "text" },
  { token: "--op-text-muted", hex: "#94a89a", grounds: OPERATOR_GROUNDS, duty: "text" },
  { token: "--op-text-faint", hex: "#7e9184", grounds: OPERATOR_GROUNDS, duty: "text" },
  { token: "--op-green", hex: "#57a867", grounds: OPERATOR_GROUNDS, duty: "text" },
  { token: "--op-green-light", hex: "#8fcb9b", grounds: OPERATOR_GROUNDS, duty: "text" },
  { token: "--op-mustard-text", hex: "#e2c078", grounds: OPERATOR_GROUNDS, duty: "text" },
  { token: "--op-blue-text", hex: "#bfd8ec", grounds: OPERATOR_GROUNDS, duty: "text" },
  { token: "--op-red-text", hex: "#e7a392", grounds: OPERATOR_GROUNDS, duty: "text" },
  { token: "--op-border-control", hex: "#6a7a6c", grounds: OPERATOR_GROUNDS, duty: "nontext" },
  { token: "--op-divider", hex: "#263028", grounds: OPERATOR_GROUNDS, duty: "decor" },
];

const THRESHOLD = { text: 4.5, large: 3.0, nontext: 3.0, decor: 0 };

function auditPalette() {
  let failures = 0;
  console.log(
    "Worst-case contrast per token. Light grounds: canvas, surface-soft, surface.",
  );
  console.log("Operator grounds: surface, raised, card, hover.\n");
  console.log(
    `${"token".padEnd(40)} ${"hex".padEnd(9)} ${"worst".padStart(6)}  ${"need".padStart(5)}  duty      result`,
  );
  console.log("-".repeat(88));

  for (const entry of PALETTE) {
    const grounds = entry.grounds ?? entry.on;
    const ratios = Object.values(grounds).map((g) => contrast(entry.hex, g));
    const worst = Math.min(...ratios);
    const need = THRESHOLD[entry.duty];
    const ok = worst >= need;
    if (!ok) failures += 1;

    const verdict = entry.duty === "decor" ? "exempt" : ok ? "pass" : "FAIL";
    console.log(
      `${entry.token.padEnd(40)} ${entry.hex.padEnd(9)} ${worst.toFixed(2).padStart(6)}  ` +
        `${(need || "-").toString().padStart(5)}  ${entry.duty.padEnd(8)}  ${verdict}`,
    );
  }

  console.log("");
  if (failures > 0) {
    console.error(`${failures} token(s) fail their declared duty.`);
    console.error("Fix the value or change its declared role. Do not lower the threshold.");
    return 1;
  }
  console.log("All tokens meet their declared duty.");
  console.log("This checks colour only. Targets, focus, motion, and Korean");
  console.log("line breaking still need the manual pass in references/accessibility.md.");
  return 0;
}

function main(argv) {
  if (argv.includes("-h") || argv.includes("--help")) {
    console.log(HELP);
    return 0;
  }
  if (argv.includes("--palette")) return auditPalette();

  const flags = argv.filter((a) => a.startsWith("--"));
  const colours = argv.filter((a) => !a.startsWith("--"));
  if (colours.length !== 2) {
    console.error(HELP);
    return 1;
  }

  const [fg, bg] = colours;
  const duty = flags.includes("--large")
    ? "large"
    : flags.includes("--nontext")
      ? "nontext"
      : "text";
  const ratio = contrast(fg, bg);
  const need = THRESHOLD[duty];
  const ok = ratio >= need;

  console.log(`${fg} on ${bg}`);
  console.log(`  ratio  ${ratio.toFixed(2)}`);
  console.log(`  need   ${need.toFixed(1)}  (${duty})`);
  console.log(`  ${ok ? "pass" : "FAIL"}`);

  if (!ok && duty === "text" && ratio >= 3.0) {
    console.log("");
    console.log("  Clears 3.0, so it is usable at 18.66px bold or 24px only.");
    console.log("  It is not a body-text colour.");
  }
  return ok ? 0 : 1;
}

process.exit(main(process.argv.slice(2)));
