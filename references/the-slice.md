# The Slice

A slice is the unit of work this skill plans, delegates, and verifies. This file says what one is, how big it should be, who owns it, and where the idea stops working.

## Why the unit of work changed

AI compresses doing, not done. Producing code, or the first draft of almost anything, got cheap. Verifying that output, integrating it with everything around it, and deciding whether it was worth building have barely moved. Those are two different clocks, and most teams only watch the first one.

When typing gets cheap, it becomes easy to pour more work into every change. Larger changes carry more risk and take longer to check. A slice is a batch-size discipline: it caps each change at one outcome a person can notice, so the expensive clock (verify, integrate, decide) runs on something small enough to finish.

## What a slice is

A slice cuts through every layer the work touches and delivers one thing a customer can use, or a stakeholder can watch in a demo.

Name it from the domain, in the form "<who> can <do what>". Anyone who reads the name should know what customers can do once it ships, and what they still cannot.

| Queue item | Slice |
|---|---|
| Add `payment_methods` table | Customers can pay with a card they have used before |
| Merge the kernel migration | After update, every supported machine boots the new kernel |
| Tag billing tickets | A customer with an expired card can fix it without writing to support |

If the name mentions a table, an endpoint, or a ticket, keep rewriting until it describes a person doing something.

## INVEST and the two additions

A well-written user story is close to a slice. Bill Wake introduced the INVEST checklist in 2003, in a short article titled "INVEST in Good Stories, and SMART Tasks". Mike Cohn's book *User Stories Applied* (2004) spread it across agile teams.

| Letter | Quality | Meaning |
|---|---|---|
| I | Independent | Can be built and shipped without waiting on another story |
| N | Negotiable | Describes a need and leaves room to decide how to meet it |
| V | Valuable | Delivers something a user or customer cares about |
| E | Estimable | Clear enough to size |
| S | Small | Fits comfortably inside one iteration |
| T | Testable | Has a check that shows when it is done |

A slice keeps all six and adds two things INVEST leaves out:

1. **One named owner.** A single person (or, in an agent plan, a single assignment) answers for the outcome from start to ship.
2. **A done test that proves the outcome in the real world.** A real customer pays. A real machine boots the right kernel. Task-level checks (package installed, ticket closed, migration marked complete) can all pass while the outcome fails. The done test checks the outcome itself. See `references/done-tests.md`.

Stories usually lose these two after they are written. The team breaks the story into subtasks, hands them to different people, and the story survives only as a parent link nobody opens.

## How big a slice is

**For a person:** one person can finish it in a week or less, with AI doing the mechanical work.

**For an agent working from a plan:** one slice per turn. Implement the next slice only, run its done test, record the result in the plan, then stop and report. The person who approved the plan decides when the next slice starts.

When a slice is too big, split it by outcome. "Customers can see saved cards" and "customers can pay with one" are two slices. Frontend and backend are layers, and a split along layers produces two halves that neither ship nor prove anything on their own.

Keep one slice in flight per person. Every extra item in progress adds a context reload, and the switching cost grows faster than the list.

## Who owns a slice

Help is welcome. Ownership stays put.

Agents can propose scope, flag edge cases, draft the out-of-scope list, and write the code. Accountability is a different matter. When a client calls because a charge went through twice, someone has to answer, and that person should be the one who decided what shipped. Agents write the code. A person answers for it.

In an agent plan, the `Owner:` field takes one of two values:

- `self`: the agent in this session implements the slice.
- `delegate(task=..., verify=...)`: a subagent implements it, and the `verify` command is the done test it runs before reporting done.

Either way, the human who approves the plan answers for what ships. The plan format is in `references/plan-format.md`.

## Where slicing breaks

Three limits apply before you force every piece of work into this shape.

- **Some work does not slice cleanly.** A database migration, a compliance audit, or a platform rebuild may need coordinated specialists and a longer runway.
- **Some slices are too big for one person, even with agents.** Cut them smaller rather than staffing them larger.
- **A builder who works alone becomes the only person who understands the slice.** Every slice needs a short, deliberate handoff at the end, so someone else can run the done test and pick up the next one.

## Sources

- Kent Langley, "Own the Slice" (September 21, 2026): https://www.kentlangley.com/blog/own-the-slice/
- Bill Wake, "INVEST in Good Stories, and SMART Tasks" (XP123, 2003): https://xp123.com/articles/invest-in-good-stories-and-smart-tasks/
- Mike Cohn, *User Stories Applied* (Addison-Wesley, 2004).
- The agent-skill form of this method (plan in slices, delegate with done tests, verify before done) comes from slice-discipline by unixguru2k, MIT license: https://github.com/unixguru2k/slice-discipline
