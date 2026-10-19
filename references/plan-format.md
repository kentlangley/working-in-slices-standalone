# Plan format

The plan document is the running record of a piece of work. It holds the design for the people who plan and review, a brief for whoever executes each slice, and a log of what shipped. This page defines the format, the lifecycle, and the linter that enforces it. A complete example that passes the linter is at the end.

## Location and lifecycle

- Active plans live at `plans/<slug>.md` in the project root. The slug is lowercase and hyphenated, for example `plans/saved-cards-at-checkout.md`.
- A plan that exists only in the conversation is lost to the next session. If someone pastes a plan, or the plan predates this convention, save it to `plans/<slug>.md` first, then work from the file.
- When the final slice's done test passes, move the plan to `plans/archive/<slug>.md`. A fully shipped plan left in `plans/` reads as open work.
- A plan with deferred slices stays in `plans/`. Its Status line names what remains, so the next session sees at a glance what is left and why.

## Document shape

A plan has a title (`# <Plan title>`), a Status line, then three design sections (`## Problem`, `## Design`, `## Open questions`), then `## Slices`. Each slice is a `### Slice N: name` heading, a list of fields, and a `#### Execute (Slice N)` brief.

Fields are Markdown list items written `- Field: value` (a `*` bullet works too). Field names are case-sensitive and must be spelled as shown below. Code inside fenced blocks is ignored, so a plan can quote code or other plans without confusing the linter.

## Fields

A placeholder is an empty value, a value wholly inside angle brackets, or one of `TBD`, `TODO`, `?`, `...`, or the single ellipsis character. Placeholders count as missing.

| Field | Required | Rule |
|-|-|-|
| Plan `Status:` line | Warning if missing | Free text. It is the first `Status:` line before the first slice heading. It must name what remains when slices are deferred. |
| `### Slice N: name` | Error if the plan has no slices | N is an integer. The name is in domain language, "who can do what". |
| `Ships:` | Error | What the user can do after this slice that they could not before. Not empty, not a placeholder. |
| `Touches:` | Error | The layers or files the slice changes. Not empty, not a placeholder. |
| `Done test:` | Error | The command or check that proves the slice. Not empty, not a placeholder. |
| `Owner:` | Error | Exactly `self`, or `delegate(task=<text>, verify=<text>)` with both parts filled in. |
| `Out for now:` | Warning if missing | What the slice leaves out. `nothing` is allowed. |
| `Status:` (slice) | Warning if missing | One of the values below. |
| `Proved by:` | Error when Status is done and this is missing | The command and its outcome. |
| `Notes:` | Optional | What actually shipped if it differs, plus anything deferred or discovered. |
| `#### Execute (Slice N)` | Error if missing for any slice | N matches the slice. |
| Execute `Done test:` | Error if missing | A warning if it differs from the slice's Done test. |
| Execute `Decisions frozen:` | Error if missing | Names what applies as written. |

### Slice names

A slice name reads as an outcome in the user's words: "Customers can pay with a saved card". The linter warns when a name contains a backtick, a snake_case or camelCase identifier, or one of the words table, column, endpoint, ticket, refactor, schema, or migration. Those words describe how the work is built. Rewrite the name as "who can do what". The camelCase rule also catches brand names such as iPhone or eBay; the result is only a warning, so leave a name like that as it is.

### Owner

`self` means you implement the slice in this session. `delegate(task=..., verify=...)` means a subagent does the work. The task says what it builds. The verify part is the command the subagent runs before reporting done, and the same command you re-run to confirm the result. A delegate with an empty task or an empty verify is an error.

### Slice status values

| Value | Meaning |
|-|-|
| `planned` | Not started. |
| `in progress` | Started, done test not yet passing. |
| `done` | Done test passed. May be followed by a date, for example `done 2026-10-19`. Requires Proved by. |
| `deferred` | Parked on purpose. May be followed by a reason. The plan stays in `plans/` and its Status line names what remains. |

## The Execute brief

Every slice carries a short brief under `#### Execute (Slice N)`. It holds imperative steps that point at design sections instead of restating them, the exact Done test command, and a `Decisions frozen:` line.

The brief exists because the design sections (Problem, Design, Open questions) are written for planning and review. During execution they cost context and invite second-guessing of settled decisions. So while executing:

- Read only the current slice's brief, plus any design section the brief points to.
- Do not re-derive intent from the full plan.
- Do not re-open open questions.
- Do not redesign mid-slice.
- If the brief is wrong or incomplete, stop and report the discrepancy. The person who owns the plan decides what changes.

## Recording progress

After each slice's done test passes, make one small edit to that slice in the plan file. It is an edit to the record, with no status report to write.

1. Set the slice Status to `done` with the date.
2. Fill in Proved by with the command and its outcome, for example `` `pytest tests/test_checkout.py` -> 14 passed ``.
3. Use Notes for what actually shipped if it differs from the plan, and for anything deferred or discovered: new constraints, follow-ups, open questions.
4. Update the plan Status line (how many slices are done, what is next).
5. If that was the last slice, move the plan to `plans/archive/`.

The plan file is what the next session reads. It replaces digging through the git log to find out where things stand.

## The linter

Run it from the project root, pointing at the script inside the installed skill folder:

`python3 <skill folder>/scripts/check_plan.py plans/<slug>.md`

For a skill installed for every project in Claude Code, `<skill folder>` is usually under `~/.claude/skills/`.

You can pass several files. It needs Python 3.9 or later and nothing else. It only reads: it never moves or edits a file.

| Flag | Effect |
|-|-|
| `--json` | Prints a JSON list with one object per file: `path`, `slices`, `done`, `errors`, `warnings`, `ready_to_archive`. |
| `--strict` | Treats warnings as failures. |
| `-h`, `--help` | Prints usage. |

| Exit code | Meaning |
|-|-|
| 0 | No errors. Warnings are allowed unless `--strict` is set. |
| 1 | At least one error, or at least one warning under `--strict`. |
| 2 | Usage error or a file that cannot be read. |

Each finding prints on one line, starting with `ERROR` or `WARN`, then the slice number when there is one, then the fix. A summary line ends each file, for example `plans/saved-cards.md: 3 slices, 1 done, 0 errors, 1 warning`.

What it checks:

- Slice headings, and that the plan has at least one.
- Ships, Touches, Done test, and Owner on every slice, with the Owner grammar above.
- Out for now and Status, as warnings.
- Proved by on every slice marked done.
- An Execute brief for every slice, with its own Done test and Decisions frozen.
- Slice names that read like implementation language, as warnings.
- The plan Status line, as a warning.
- Location: the file belongs in `plans/`, or in `plans/archive/` once finished. A plan in the archive with a slice that is neither done nor deferred is an error. When every slice is done and the plan is still in `plans/`, it prints the `mkdir -p` and `mv` command that archives it.

A template copied straight from `templates/slice-plan.md` fails the linter until the placeholders are replaced. That is the intended behavior.

## Worked example

The plan below passes the linter with exit 0. Save it as `plans/saved-cards-at-checkout.md` to try it.

````markdown
# Saved cards at checkout

Status: active, 1 of 3 slices done. Next: Slice 2.

## Problem

Returning customers retype their card on every order. Support hears about it weekly and about one in five carts is abandoned at the payment step.

## Design

Store a processor token for each card, never the card number. The checkout page lists saved cards first and falls back to the card form. Removal deletes the token at the processor, then the local row.

## Open questions

- Resolved: tokens come from the existing payment processor, no second vendor.
- Resolved: customers may save up to five cards.

## Slices

### Slice 1: Customers can see the cards they saved
- Ships: A signed-in customer sees their saved cards (brand and last four digits) on the checkout page.
- Touches: payments service, checkout page
- Done test: pytest tests/test_saved_cards_list.py
- Owner: self
- Out for now: Paying with a saved card, removing a card
- Status: done 2026-10-19
- Proved by: `pytest tests/test_saved_cards_list.py` -> 6 passed
- Notes: Shipped as planned. The five-card limit is enforced in Slice 2.

#### Execute (Slice 1)
- Add the saved-card list to the checkout page, following the Design section.
- Read cards through the payments service, never the processor directly.
- Done test: pytest tests/test_saved_cards_list.py
- Decisions frozen: design sections and resolved open questions apply as written.

### Slice 2: Customers can pay with a saved card
- Ships: A customer picks a saved card and completes the order without retyping anything.
- Touches: payments service, checkout page, order confirmation
- Done test: pytest tests/test_pay_with_saved_card.py
- Owner: delegate(task=add the pay-with-saved-card action and the charge call, verify=pytest tests/test_pay_with_saved_card.py passes)
- Out for now: Removing a card
- Status: in progress
- Notes: Charge call is written. The test for a declined card is still failing.

#### Execute (Slice 2)
- Add a pay action to each saved card on the checkout page.
- Charge the stored token through the payments service and record the order.
- Show the existing decline message when the processor refuses the charge.
- Done test: pytest tests/test_pay_with_saved_card.py
- Decisions frozen: design sections and resolved open questions apply as written.

### Slice 3: Customers can remove a saved card
- Ships: A customer deletes a saved card and it no longer appears at checkout.
- Touches: payments service, account page
- Done test: pytest tests/test_remove_saved_card.py
- Owner: self
- Out for now: Editing a card's expiry date
- Status: planned

#### Execute (Slice 3)
- Add a remove button to each card on the account page.
- Delete the token at the processor first, then the local row, as the Design section says.
- Done test: pytest tests/test_remove_saved_card.py
- Decisions frozen: design sections and resolved open questions apply as written.
````

When all three slices are done, run the linter again. It will print the command that moves the file to `plans/archive/`.
