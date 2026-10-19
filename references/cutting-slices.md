# Cutting Slices

Slices are everywhere. Every stuck project, open loop, and recurring complaint has one inside it, waiting to be named. This file shows how to find one, cut it to size, argue with it before you build, and write it into a plan. It works for any kind of work, including work with no code in it.

## Queue items and slices

The same work, written two ways. The queue item names an activity. The slice names something a person can do or see when the work is finished, and you can check it from across the room.

| Where | Queue item | Slice |
|---|---|---|
| Product | Add `payment_methods` table | Customers can pay with a card they have used before |
| Infrastructure | Merge the kernel migration | After update, every supported machine boots the new kernel |
| Support | Tag billing tickets | A customer with an expired card can fix it without writing to support |
| Sales | Update CRM fields | A prospect who asks for pricing gets a quote the same day |
| Finance | Reconcile accounts | The business owner sees cash runway every Monday without asking |
| Hiring | Post the job description | A strong candidate goes from first call to offer in ten days |
| Home | Clean the garage | The car fits in the garage |

## The nine steps

1. **Find the pile.** Look for where work waits: unreviewed changes, parked plans, a support queue, a step everyone routes around. The constraint sits just downstream, and your first slice should pass through it.
2. **Start from a complaint someone actually made.** Support tickets, a client's frustration, the thing your team keeps apologizing for. A backlog item is at least one step removed from a real person.
3. **Name the outcome in their words.** Use the form "<who> can <do what>". If the sentence mentions a table, an endpoint, or a ticket, keep rewriting until it describes a person doing something.
4. **Write the done test.** One observable check that someone other than you can run: a customer completes a payment, `uname -r` prints the right kernel, the car fits. If you cannot write the test, you have found a topic and still need to find the slice.
5. **Draw the line.** List what is in (five items or fewer) and what is out for now. The out list is the most important thing you will write. It protects the slice from you, your manager, and the model.
6. **Size it.** Could one person finish this in a week or less with AI doing the mechanical work? If not, split it by outcome. "Customers can see saved cards" and "customers can pay with one" are two slices. Frontend and backend are layers.
7. **Name the judgment you need.** Design, data, security, legal, a teammate's approval. Write down who, and bring each of them the slice itself: the need, the done test, and the out list.
8. **Put one name on it, in public.** One owner, stated where the team can see it. Help is welcome. Ownership stays put.
9. **Ship, run the test, stop.** When the done test passes, the slice is finished. Tell the person who complained. Then shape the next one.

## Arguing with the slice

A slice is a claim: *if we ship this, <who> can <do what>.* Claims can be tested. Stephen Toulmin's model of argument, from *The Uses of Argument* (1958), maps onto a slice almost exactly, and each part gives you a question to ask before you build.

| Part | Question it asks of the slice |
|---|---|
| Claim | What will be true for a person once this ships? |
| Grounds | What evidence says it will be true? |
| Warrant | What assumption connects that evidence to the outcome? |
| Rebuttal | Under which paths, users, or conditions is the claim false? |
| Qualifier | Where exactly does the claim hold? |
| Revised slice | The slice rewritten so the claim survives the rebuttal. |

Here is a real case. Omarchy, an Arch-based Linux distribution, made its own kernel the default in September 2026. Every task-level check passed, and machines kept booting the old kernel along two separate paths.

| Part | The Omarchy kernel slice |
|---|---|
| Claim | Shipping this migration means every supported x86 machine runs linux-omarchy. |
| Grounds | The package installs, and BOOT_ORDER lists the new kernel first. |
| Warrant | Machines boot whatever BOOT_ORDER lists first. |
| Rebuttal | Unless the Limine template overrides the default entry, or firmware direct boot skips Limine entirely. |
| Qualifier | On every boot path we actually test after a reboot. |
| Revised slice | Every supported x86 install boots linux-omarchy on the Limine path and on direct boot. Done when `uname -r` says so on both. |

The warrant is where both bugs hid. Attack the warrant first. It is the assumption everyone shares and nobody checks.

## Using a model to find piles and argue

AI helps with more than the typing inside a slice. A capable model can read a codebase, a support queue, or a year of meeting notes and point to where work is piling up. It is also good at the part people most often skip: finding what a slice forgot. Use this sequence.

1. **Have the model find the piles.** Point it at tickets, support threads, pull requests, or notes, and ask where work waits and why.
2. **State the slice as a claim.** Write "if we ship this, <who> can <do what>", with your done test.
3. **Ask for the grounds and the warrant.** What evidence supports the claim, and what assumption connects the evidence to the outcome?
4. **Ask for the strongest rebuttal.** Which paths, users, or conditions would make the claim false? Ask for the case you would be most embarrassed to have missed.
5. **Revise the scope or the qualifier.** Either bring the missed path into the slice, or state plainly that the slice excludes it and add it to the out list.
6. **Decide.** The model argues. The builder chooses what ships and answers for it.

## A prompt to try

Fill in the brackets and paste it into a capable model.

```text
Here is a slice I plan to ship: [outcome], done when [test].
Treat it as an argument. State its claim, grounds, and warrant.
Then give me the three strongest rebuttals: the paths, users, or
conditions under which the claim would be false after it ships.
For each, tell me whether to bring it into scope or name it as
out of scope.
```

## From a cut slice to a plan entry

When the work runs from a written plan, each cut slice becomes one `### Slice N:` entry. The full format and a worked example are in `references/plan-format.md`. The nine steps map onto the plan like this.

| Step | Goes into |
|---|---|
| 1 and 2: the pile and the complaint | The plan's `## Problem` section |
| 3: the outcome in their words | The slice heading `### Slice N: <who can do what>` and the `Ships:` line |
| 4: the done test | `Done test:` on the slice, repeated word for word as `Done test:` in its `#### Execute (Slice N)` brief |
| 5: what is in | `Touches:` (the layers or files the in list reaches) and the Execute steps |
| 5: what is out for now | `Out for now:` (write `nothing` if the list is empty) |
| 6: the size check | One slice per entry; split any entry that fails the size check before the plan goes for approval |
| 7: the judgment you need | `## Open questions`, or `Notes:` on the slice |
| 8: one name on it | `Owner: self` or `Owner: delegate(task=..., verify=...)` |
| 9: ship, run the test, stop | `Status: done <date>` and `Proved by:` with the command and its outcome |

Two templates carry this into practice:

- `templates/slice-card.md` is a one-slice worksheet. Use it to cut a single slice by hand, with or without a plan around it.
- `templates/slice-plan.md` is the plan document. Use it when a piece of work needs several slices, an approval, and a running record.

Run `scripts/check_plan.py` on the finished plan before you present it. It flags missing done tests, placeholder values, and slice names that read like implementation language.
