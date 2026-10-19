# Slice card

One slice, one page. It works for any kind of work: code, a campaign, a hiring process, a client delivery. Fill the nine fields in order. If you cannot answer one, that is the next thing to find out, and you should do that before you plan anything else. For how to cut work into slices, see `references/cutting-slices.md`. For writing the done test, see `references/done-tests.md`.

## The card

1. Where does work pile up?
   <the place where things wait, queue, or get redone>

2. Whose complaint is it?
   <the person or group who feels it, by name or role>

3. The outcome, written as "<who> can <do what>"
   <who> can <do what>

4. Done test
   <the command, check, or observation that proves the outcome in the real world>

5. In scope (five items or fewer)
   - <item>
   - <item>

6. Out for now
   - <what this slice leaves for later>

7. Size check
   One person, a week or less, with AI doing the mechanical work. If it is bigger, split it by outcome, so each piece serves a different user or produces a different result.
   <fits as written | split into: ...>

8. Judgment needed, and from whom
   <the decision that only a person can make, and who makes it>

9. Owner (one name)
   <one name>

## Argue with it

Before you commit, give the card to your agent and let it attack the claim. Paste this, with the outcome and the done test filled in:

```text
Here is a slice I plan to ship: [outcome], done when [test]. Treat it as an argument. State its claim, grounds, and warrant. Then give me the three strongest rebuttals: the paths, users, or conditions under which the claim would be false after it ships. For each, tell me whether to bring it into scope or name it as out of scope.
```

Bring a rebuttal into scope only if it fits the size check. Everything else goes under Out for now, in writing, so the next session knows it was a decision.

## Turn it into a plan entry

Once the card holds up, copy it into `templates/slice-plan.md` as a slice. The fields map like this:

| Card field | Plan field |
|-|-|
| 1 Where work piles up, 2 Whose complaint | Problem section |
| 3 Outcome | Slice heading (`### Slice N: <who> can <do what>`) and Ships |
| 4 Done test | Done test, and the Done test line in the Execute brief |
| 5 In scope | Touches, and the steps in the Execute brief |
| 6 Out for now | Out for now |
| 7 Size check | A slice that fails it becomes two slices |
| 8 Judgment needed | Open questions, resolved before the slice starts and then frozen in the brief |
| 9 Owner | Owner (`self`, or `delegate(task=..., verify=...)` when a subagent does the work) |

Then run check_plan.py (see `references/plan-format.md`) to confirm the entry is complete. The full format is in `references/plan-format.md`.
