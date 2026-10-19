---
name: working-in-slices-standalone
description: Work in slices. Decompose implementation plans into shippable increments, each named in domain language with one owner and a done test that proves the outcome in the real world. Delegate with Verify lines, verify before calling a turn done, ship one slice per turn, record each slice's proof in plans/<slug>.md and archive the plan when it ships, and execute from a compact per-slice brief. Also cuts slices out of work beyond code (sales, finance, hiring, support) and argues with a slice before it ships. Includes a plan linter, scripts/check_plan.py. Use when planning implementation work, breaking a feature or project into steps, delegating sub-tasks to agents or people, deciding whether a turn or task is done, or keeping a plan document current and archiving it when the work ships.
license: "MIT. See LICENSE."
metadata:
  version: "1.0.0"
  author: "Kent Langley"
  author-url: "https://kentlangley.com"
  based-on: "slice-discipline 1.4.1 by Harshal Dhir (https://github.com/unixguru2k/slice-discipline)"
---

# Working in Slices (Standalone)

By [Kent Langley](https://kentlangley.com). Built on Harshal Dhir's open-source [slice-discipline](https://github.com/unixguru2k/slice-discipline) skill.

AI cut the cost of doing. Verifying, integrating, and deciding whether the work was worth building still cost what they always did. The slice is the working unit that closes that gap: a shippable increment with one named owner and a done test that proves the outcome in the real world. It keeps all six INVEST qualities of a good user story and adds the two things INVEST leaves out, the named owner and the real-world done test.

This skill holds five disciplines for agent work (plan, delegate, verify, record, execute from briefs) and the method for cutting slices out of any business work, code or not. Every stuck project, open loop, and recurring complaint has a slice inside it.

## How It Works With Your Other Skills

Nothing else needs installing. Every rule, reference, template, and the linter ship in this folder. It sits well beside other skills you may have:

- **Agent loops.** A loop runs one slice to done. The slice's done test is the loop's judge, and its `Verify:` line is the machine check the loop can trust.
- **Review and quality checks.** The done test is validation stated before the work starts. Add a review step when a slice's outcome needs more than one command to prove.
- **Multi-agent fan-out.** Every delegated slice carries its own done test, so the orchestrator re-runs one command per slice instead of reading every diff.
- **Planning tools.** Plan mode, or any plan-presentation tool, gets slices in the format below. The plan file in `plans/` is the record the next session reads.

## Triggers

- "Plan this feature" / "write an implementation plan" / "break this into steps" / "slice this"
- Presenting any plan for approval in plan mode or a plan-presentation tool
- Delegating a sub-task to a subagent, a contractor, or a team member
- Deciding whether a coding turn, a task, or a project is complete ("is this done?", "what's the done test?")
- Working from an existing plan document, or one the user pasted ("keep the plan current", "archive the plan")
- A project that keeps sprawling, a feature that is "almost done" for weeks, or work split into subtasks that nobody can tie back to an outcome
- Business work stuck in a queue: support tickets, CRM cleanup, reconciliations, hiring pipelines
- "Own the slice" / "slice discipline" / "work in slices" / "one slice per turn"

## Core Directives

### What a Slice Is

- A slice cuts through every layer the work touches and delivers one thing a customer can use, or a stakeholder can watch in a demo.
- MUST name every slice in domain language, in the form "<who> can <do what>". If the name mentions a table, an endpoint, a column, or a ticket, rewrite it until it describes a person doing something.
- MUST give every slice one named owner and one done test: an observable check that someone other than the worker can run, proving the outcome rather than the activity.
- SHOULD split by outcome, never by layer. "Customers can see saved cards" and "customers can pay with one" are two slices. Frontend and backend are layers.
- SHOULD size a person's slice so one person finishes it in a week or less with AI doing the mechanical work. An agent working from a plan takes one slice per turn.

Full definition, INVEST, sizing, and ownership: `references/the-slice.md`.

### 1. Plan in Slices

- When presenting an implementation plan for approval (plan mode, or your agent's plan-presentation tool), MUST decompose the work into slices, each in this shape:

```markdown
### Slice N: <name in domain language, such as "Customers can pay with a saved card"; a name like "Add billing column" fails>
- Ships: <what the user can do after this that they couldn't before>
- Touches: <layers or files>
- Done test: <the command or check that proves it: test command, build, /health after a deploy>
- Owner: self | delegate(task=..., verify=...)
- Out for now: <what this slice leaves out>
- Status: planned
```

- `self` means you implement the slice in this session.
- `delegate(task=..., verify=...)` means a subagent takes the slice through your agent's delegation tool (Task, spawn_subagent, or equivalent). The `verify` command is the slice's done test, and the subagent runs it before reporting done.
- MUST give every slice a done test. A plan with no done tests is not a plan. If you cannot name how a slice will be proven, research more before presenting.
- SHOULD write the out-for-now list for every slice. It protects the slice from the builder, the manager, and the model.

Full field rules, status values, and a worked plan: `references/plan-format.md`. Skeleton: `templates/slice-plan.md`.

### 2. Delegate with Done Tests

- A delegated sub-task is incomplete without a done test. The subagent's bounded context makes the done test the only cheap verification interface between orchestrator and worker: you re-run one command to confirm instead of reading everything it touched.
- MUST end every delegation prompt with a `Verify:` line holding the exact command or check that proves the deliverable:

```text
Verify: pytest tests/test_auth.py passes
```

- MUST tell the subagent to run the `Verify:` line itself before reporting done (it has shell access unless denied).
- MUST re-run the `Verify:` command yourself before accepting delegated work. The worker's report is a claim; the command is the proof.

Brief to copy: `templates/delegation-brief.md`. Done tests by type of work: `references/done-tests.md`.

### 3. Verify Before Done

- A turn that implements or changes something is not complete until its done test has run and passed. Run the tests (your shell tool with the project's test command), a build, or, after a deploy, check the live `/health`.
- MUST state the done test up front, before starting the work.
- If no done test exists or it cannot run, MUST say so explicitly instead of claiming completion, in the form "verification wasn't possible because ...".
- **Scope:** implementation turns only. Pure conversation, research, and read-only ask-mode turns are exempt. Do not force test runs on questions and answers.
- **Pacing:** one slice per turn. When working from a plan, implement the next slice only: run its done test, record progress (discipline 4), then stop and report. The user gates the next slice. MUST never roll several slices into one turn to save time; each slice exists so it can be verified and reviewed on its own.

### 4. Record Progress After Every Slice

- A slice that ships but leaves no record is invisible to the next session. After each slice's done test passes, MUST update the plan document (or the tracking issue) before moving on:
  - Mark the slice done (`Status: done <date>`) and note what actually shipped, which may differ from the plan.
  - Record the done test that proved it, the command and its outcome, in `Proved by:`.
  - Note anything deferred or discovered (new constraints, follow-ups, open questions) in `Notes:`, so the next slice starts from reality.
- This is one small edit per slice, not a status report. The plan file is the running record. The next session, or the next owner, reads it instead of re-deriving state from git log.
- **Where the plan lives:** MUST keep plan documents in the project's `plans/` folder as `plans/<slug>.md` (lowercase, hyphenated slug). When you start working from a plan that is not saved there yet (the user pasted it, or it predates the convention), save it to `plans/<slug>.md` first, then record each slice's outcome in that file. A plan that exists only in the conversation is lost to the next session.
- **When the plan is done:** once the final slice's done test passes, MUST move the plan from `plans/` to `plans/archive/`. Active plans live in `plans/`; finished ones in `plans/archive/`. A fully shipped plan left in `plans/` reads as open work to the next session. A plan with deferred slices stays put until those land, and its `Status:` line says what remains.
- SHOULD run the linter after each update, from the project root: `python3 <skill folder>/scripts/check_plan.py plans/<slug>.md`, where `<skill folder>` is wherever this skill is installed. It checks every field, flags names written in implementation language, and prints the archive command when every slice is done.

### 5. Execute from the Slice Brief

- The plan's design sections (problem, rationale, alternatives, open questions) exist for planning and review. During execution they are noise: re-reading them every turn burns context and invites the model to re-litigate settled decisions instead of doing the slice.
- MUST give each slice a compact execution brief:

```markdown
#### Execute (Slice N)
- <imperative steps, pointing at design sections instead of restating them>
- Done test: <the exact command>
- Decisions frozen: design sections and resolved open questions apply as written.
```

- During execution, MUST read only the current slice's brief, plus a design section when the brief points to one. Do not re-derive intent from the full plan, do not re-open open questions, and do not redesign mid-slice.
- If the brief is wrong or incomplete, MUST stop and report the discrepancy to the user instead of improvising a new design.

### Slicing Work Outside Code

- The same disciplines run any business work. Turn queue items into slices: "Reconcile accounts" becomes "The owner sees cash runway every Monday without asking". "Post the job description" becomes "A strong candidate goes from first call to offer in ten days".
- MUST start from a complaint someone actually made, and write the done test before the work starts. A backlog item is one step removed from a real person.
- SHOULD use the nine steps in `references/cutting-slices.md` and the one-slice worksheet in `templates/slice-card.md`, then carry the card into the plan fields.
- MUST put one name on each slice, stated where the team can see it. Help is welcome; ownership stays put.

### Arguing With the Slice

- A slice is a claim: "if we ship this, <who> can <do what>". Before a slice with real risk ships, SHOULD ask a model to state its claim, grounds, and warrant (Toulmin) and to find the three strongest rebuttals. Bring each rebuttal into scope or name it in the out-for-now list.
- The model argues. The owner decides what ships and answers for it.

Method, worked example, and the prompt: `references/cutting-slices.md`.

### Where Slicing Breaks

- Some work does not slice cleanly: a database migration, a compliance audit, or a platform rebuild may need coordinated specialists and a longer runway. In an agent plan the work still gets one slice entry with a done test; the slice is larger, and its Notes say why. Do not cut it into layer-sized pieces that prove nothing.
- A slice too big for one person, even with agents, gets cut smaller rather than staffed larger.
- A lone builder becomes the only person who understands the slice. MUST end each slice with a short, deliberate handoff: the plan entry, the proof, and the notes.

## Checklist

Before calling a plan, a turn, or a delegation complete, confirm:
- [ ] Every slice is named in domain language ("<who> can <do what>") and carries Ships, Touches, Done test, Owner, and an out-for-now list.
- [ ] Every done test is a command or observable check that someone other than the worker can run, and it proves the outcome rather than the activity.
- [ ] Every delegation prompt ended with a `Verify:` line, the delegate ran it, and the orchestrator re-ran it before accepting the work.
- [ ] The turn's done test was stated up front, ran, and passed, or the report says plainly that verification wasn't possible and why.
- [ ] Only one slice was implemented this turn, and the report stops for the user to gate the next.
- [ ] The plan at `plans/<slug>.md` records Status and Proved by (the command and its outcome) for every finished slice, and Notes whenever what shipped differed or anything was deferred or discovered.
- [ ] `scripts/check_plan.py` exits 0 on the plan.
- [ ] A fully shipped plan sits in `plans/archive/`; a plan with deferred slices stays in `plans/` and names what remains.
- [ ] For business work, the slice has one named owner, and it moves an outcome off the business owner's desk rather than routing it back through them.
- [ ] The next session or the next owner can resume from the plan file alone, without reading git history or the conversation.

## Files

| Path | What it holds |
|---|---|
| `references/the-slice.md` | What a slice is, INVEST plus the two additions, naming in domain language, sizing, ownership, where slicing breaks, sources |
| `references/cutting-slices.md` | Queue items versus slices, the nine steps to cut a first slice, arguing with the slice (Toulmin), using a model to find piles and rebuttals |
| `references/plan-format.md` | The plan document, every field and status value, execution briefs, recording progress, the plans/ and plans/archive/ lifecycle, the linter, a worked plan |
| `references/done-tests.md` | What makes a good done test, done tests by type of work, Verify lines for delegation, verifying before done, recording the proof |
| `templates/slice-plan.md` | Plan document skeleton, saved as `plans/<slug>.md` |
| `templates/slice-card.md` | One-slice worksheet for any kind of work, with the argue-with-it prompt |
| `templates/delegation-brief.md` | Copy-paste brief for a subagent, ending with the `Verify:` line |
| `scripts/check_plan.py` | Lints a plan against the format, standard library only. `python3 <skill folder>/scripts/check_plan.py plans/<slug>.md [--json] [--strict]`. Exit 0 clean, 1 errors, 2 usage error. |

## Source and Credit

- Method: "Own the Slice" by Kent Langley (https://www.kentlangley.com/blog/own-the-slice/), September 2026. The slice is INVEST (Bill Wake, 2003) plus a named owner and a real-world done test.
- Agent-skill form: slice-discipline 1.4.1 by Harshal Dhir (GitHub: unixguru2k), published by MACHAAO for MACH-AI, MIT License (https://github.com/unixguru2k/slice-discipline). The five disciplines above follow it rule for rule.
- License: MIT. See `LICENSE`. Keep both copyright lines when you share or adapt this skill.
