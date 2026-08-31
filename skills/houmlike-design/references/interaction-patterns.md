# Interaction Patterns for High-Consequence Surfaces

Read this when building a flow where the reader is agreeing to something, choosing between options that are hard to reverse, or working a dense screen where a misread has cost.

These are general patterns. They apply to a consent screen, a plan comparison, a settlement ledger, a bulk delete, or a permissions grant equally.

---

## The failure these patterns exist to prevent

The consistent finding across research on digital decision aids is that they fail **not** because they withhold information but because they impose too much of it at once. A screen that presents every option, every caveat, and every disclosure simultaneously is legally complete and practically useless: the reader scrolls, gives up, and accepts the default.

Comprehension is the goal, not disclosure. A record that someone clicked "agree" is not evidence they understood.

---

## 1. Progressive disclosure, not progressive hiding

Show what the reader needs to decide **now**. Put detail one interaction away — never behind a link that leaves the page.

- Lead with the decision and its consequence in one sentence.
- Offer detail inline: a `<details>` disclosure, an expandable row, a "왜 이게 필요한가요?" affordance next to the term that prompts the question.
- The disclosure control names what is inside it. "자세히" tells the reader nothing; "보관 기간과 삭제 방법" tells them whether to open it.
- Never hide something the reader must know to answer. Progressive disclosure sequences information; it does not conceal it.

```html
<details class="disclosure">
  <summary>이 정보가 어디에 사용되나요</summary>
  <p>...</p>
</details>
```

`<details>` is keyboard-accessible and screen-reader-announced by default. A hand-rolled accordion usually is not.

---

## 2. Plain language

Someone cannot agree to what they cannot parse. This is a design constraint, not a copywriting preference.

- Name things as the reader recognises them, not as the system models them. A person manages **알림**, not **webhook 설정**.
- One idea per sentence. Active voice.
- Expand a term the first time it appears, or link its definition inline.
- Numbers in the form the reader thinks in: "10명 중 1명" over "10%" for frequencies; absolute counts alongside percentages, never a percentage alone.
- Say what happens, not what the system does. "이 기록은 3년 후 삭제됩니다" over "보존 정책이 적용됩니다."

For Korean, keep sentences short enough to survive `word-break: keep-all` at the narrowest supported width — a long clause that wraps badly reads as harder than it is.

---

## 3. Make the choice symmetric

An interface that styles one option as a primary button and the other as faint text has made the choice for the reader. When two options are genuinely available, present them as genuinely available.

- Equal visual weight for equally valid options.
- No pre-ticked consent. Ever.
- "지금은 넘어가기" is a real option with a real control, not grey text in a corner.
- Never place a destructive action where a confirming one usually sits.

Reserve the primary button for when there truly is a recommended path, and say why it is recommended.

---

## 4. State the consequence at the point of action

The consequence belongs on the control, not in a paragraph above it.

- Button labels name the outcome: "동의하고 계속" over "확인"; "3개 항목 영구 삭제" over "삭제".
- Irreversible actions say so before the click, not in the toast afterwards.
- Confirmation dialogs restate what is about to happen, including scope and count. "정말 삭제하시겠습니까?" is not a confirmation; "케이스 3건과 첨부 12개를 삭제합니다. 되돌릴 수 없습니다." is.
- Prefer undo over confirm where the action is reversible. A confirm dialog on a reversible action trains people to dismiss dialogs.

---

## 5. Show the state of the record

For anything the reader is agreeing to or that was decided earlier, the surface should reconstruct: **what was agreed, when, by whom, and on what version.**

- Show the version or effective date of the terms that were accepted, not just the current ones.
- Show when consent was given and by which account.
- Make withdrawal as easy to find as the original agreement was. If agreeing took one click, withdrawing must not take a support ticket.
- Never show a decision without showing what it was made against.

---

## 6. Dense data screens

- Summary before detail. The reader should see what needs attention before scrolling.
- Encode state in form as well as colour — a pill, a chip, a severity stripe — so it survives `forced-colors` and colour vision differences.
- `font-variant-numeric: tabular-nums` on every aligned numeric column.
- Sort and filter state is visible and undoable. A filtered view that looks like an unfiltered one produces wrong conclusions.
- Empty is not the same as zero, and neither is the same as unknown. Three different renderings.
- Wide tables scroll inside their own `overflow-x: auto` container. The page body never scrolls sideways.

---

## 7. Errors and recovery

- Say what went wrong and what to do. No apologies, no vagueness, no error codes as the whole message.
- Preserve what the reader entered. Losing a form on validation failure is the single most common recoverable-made-unrecoverable failure.
- Do not re-ask for information already provided in the same process (WCAG 2.2 SC 3.3.7).
- Validate at submit or on blur, not on every keystroke — mid-typing errors read as accusations.

---

## 8. Before shipping the flow

1. Can a reader unfamiliar with the system state, in their own words, what they just agreed to?
2. Is every option that is genuinely available also visually available?
3. Does every irreversible action name its consequence **before** the click?
4. Is withdrawing or undoing as reachable as doing?
5. Does the screen work at 400% zoom, in forced colours, with reduced motion?
6. Does Korean text wrap at word boundaries at the narrowest supported width?
7. Is anything pre-selected that the reader should have chosen?

Item 7 is the one that most often survives review, and it is the one that most reliably invalidates the agreement it was meant to record.
