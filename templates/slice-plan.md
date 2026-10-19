# <Plan title>

> How to use this file. Save a copy as `plans/<slug>.md` (lowercase, hyphenated slug) and replace everything in angle brackets. Work one slice per turn. When a slice's done test passes, edit that slice: set Status, fill in Proved by with the command and its outcome, and add anything deferred or discovered to Notes. Move the plan to `plans/archive/` when the last slice passes. Check the file at any time with check_plan.py (see `references/plan-format.md`). Delete this note once the plan is saved. The full format is in `references/plan-format.md`.

Status: planned, 0 of 2 slices done. Next: Slice 1.

## Problem

<Who is stuck, on what, and what it costs them today. Two or three sentences.>

## Design

<The approach, the alternatives you rejected, and why. This section is for planning and review. During execution nobody re-reads it except where a slice's brief points to a part of it.>

## Open questions

<Questions that need an answer before the slice that depends on them starts. Mark each one resolved, with the answer, once it is settled.>

## Slices

### Slice 1: <who can do what, in domain language>
- Ships: <what the user can do after this slice that they could not before>
- Touches: <layers or files>
- Done test: <the command or check that proves it>
- Owner: self
- Out for now: <what this slice leaves out, or nothing>
- Status: planned
- Proved by: <fill in once done: the command and its outcome>
- Notes: <what actually shipped if it differs from the plan; anything deferred or discovered>

#### Execute (Slice 1)
- <imperative step, pointing at a Design section instead of restating it>
- <imperative step>
- Done test: <the exact command>
- Decisions frozen: design sections and resolved open questions apply as written.

### Slice 2: <who can do what, in domain language>
- Ships: <what the user can do after this slice that they could not before>
- Touches: <layers or files>
- Done test: <the command or check that proves it>
- Owner: delegate(task=<what the subagent builds>, verify=<the command that proves it>)
- Out for now: <what this slice leaves out, or nothing>
- Status: planned
- Proved by: <fill in once done: the command and its outcome>
- Notes: <what actually shipped if it differs from the plan; anything deferred or discovered>

#### Execute (Slice 2)
- <imperative step, pointing at a Design section instead of restating it>
- <imperative step>
- Done test: <the exact command>
- Decisions frozen: design sections and resolved open questions apply as written.
