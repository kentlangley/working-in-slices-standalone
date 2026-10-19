# working-in-slices-standalone

A Claude skill for finishing work when AI makes doing cheap. It has your agent plan in slices: shippable increments, each named for what a person can do once it ships, with one owner and a done test that proves it. Then it holds the agent to them, one slice at a time.

By [Kent Langley](https://kentlangley.com). Built on Harshal Dhir's open-source [slice-discipline](https://github.com/unixguru2k/slice-discipline), from the essay ["Own the Slice"](https://www.kentlangley.com/blog/own-the-slice/).

## What it covers

- **Plan in slices.** Every plan for approval is a list of slices with Ships, Touches, Done test, and Owner (`self` or `delegate(task=..., verify=...)`). A plan with no done tests is not a plan.
- **Delegate with done tests.** Every delegation prompt ends with a `Verify:` line. The subagent runs it before reporting done, and the orchestrator re-runs it before accepting the work.
- **Verify before done.** An implementation turn is complete only when its done test has passed, or the agent says plainly that verification wasn't possible and why. One slice per turn; you gate the next.
- **Record progress.** After each slice, one small edit to `plans/<slug>.md`: the status, the command and its outcome, and what was deferred or discovered. Finished plans move to `plans/archive/`.
- **Execute from briefs.** Each slice carries a short execution brief with its decisions frozen, so the agent does the slice instead of re-arguing the design.
- **Slices beyond code.** The same method for sales, finance, hiring, and support queues, plus a prompt that has a model argue with your slice before it ships.
- **A plan linter.** `scripts/check_plan.py` checks every field, flags slice names written in implementation language, and tells you when a plan is ready to archive.

## Install

**Claude Code.** Clone the repo into your skills folder:

```
git clone https://github.com/kentlangley/working-in-slices-standalone.git ~/.claude/skills/working-in-slices-standalone
```

Or download `working-in-slices-standalone-1.0.0.zip` from the [latest release](https://github.com/kentlangley/working-in-slices-standalone/releases/latest) and unzip it into `~/.claude/skills/`. To use it in one project only, put it in that project's `.claude/skills/` folder instead.

**claude.ai.** Download `working-in-slices-standalone-1.0.0.zip` from the [latest release](https://github.com/kentlangley/working-in-slices-standalone/releases/latest) and upload it under Skills in your settings. Use that attached zip. GitHub's "Source code" archives name their folder with the version number, and the skill expects its folder to match its name.

**Other agents.** Any agent that reads SKILL.md skills can use it: copy the folder into that agent's skill directory.

## Start here

Ask your agent to plan a feature. It will come back with slices. Approve the plan, and it will save it to `plans/<slug>.md` and build the first slice only. When the work is not code, fill in `templates/slice-card.md` first. To check a plan by hand:

```
python3 ~/.claude/skills/working-in-slices-standalone/scripts/check_plan.py plans/<slug>.md
```

## What's inside

| Path | What it holds |
|---|---|
| `SKILL.md` | The skill: when it triggers, the five disciplines, and the checklist |
| `references/` | What a slice is, how to cut one, the plan format, and done tests |
| `templates/` | The plan skeleton, the one-slice card, and the delegation brief |
| `scripts/check_plan.py` | The plan linter, Python standard library only |

## Version

1.0.0, adapted from slice-discipline 1.4.1 (commit 259ecfa).

## License

MIT. See [LICENSE](LICENSE). Keep both copyright lines, Harshal Dhir's (unixguru2k) and Kent Langley's, with every copy.
