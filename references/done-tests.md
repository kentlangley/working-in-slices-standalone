# Done Tests

The done test is the contract that closes a slice. Before it passes, the slice is open, however much code exists. After it passes, the slice is finished and the next one can start. This file covers how to write one, examples by type of work, how done tests carry delegation, and how to record the proof.

## What a good done test is

A done test is one observable check that someone other than you can run. It proves the outcome in the real world, not the activity that produced it.

Three properties make it work:

- **Observable.** It produces a result anyone can see: an exit code, a count, a page that loads, a payment that clears.
- **Runnable by someone else.** A teammate, a reviewer, or another agent can run it without asking you what you meant.
- **About the outcome.** It checks the thing the slice name promises. "Package installed" and "migration marked complete" describe steps. "After a reboot, `uname -r` shows the new kernel" describes the machine.

| Weak | Good |
|---|---|
| Tests pass | `pytest tests/test_checkout.py` passes |
| Deployed | `curl -fsS https://app.example.com/health` returns 200 after the deploy |
| Docs updated | A reader who has never seen the project follows the setup page on a clean machine and the app starts |
| Migration done | `SELECT count(*) FROM payment_methods WHERE token IS NULL` returns 0 |
| Kernel updated | After a reboot on each boot path, `uname -r` shows the new kernel |
| Sales process improved | A prospect who asks for pricing gets a quote the same day |

Go back to `references/cutting-slices.md` and narrow the outcome until a check exists.

## Done tests by type of work

| Type of work | Done test shape | Example |
|---|---|---|
| Code change | The project's own test command, aimed at the changed behavior | `pytest tests/test_auth.py` passes |
| Build | The build command exits 0 and produces the artifact | `npm run build` exits 0 |
| Deploy | The live service answers after the deploy, checked from outside | `curl -fsS https://app.example.com/health` returns 200 |
| Data or migration | A query that returns the expected count or value | The count of rows missing the new field is 0 |
| Infrastructure | The machine reports the intended state after a restart | `uname -r` shows the new kernel on every boot path |
| Content or docs | A reader can complete the task the page describes, or a machine check passes | A new reader follows the guide and finishes the task without asking for help |
| Sales | The customer-facing result happens on time | A prospect who asks for pricing gets a quote the same day |
| Finance | The number reaches the person who needs it without a request | The business owner sees cash runway every Monday without asking |
| Hiring | The candidate's path meets the target | A strong candidate goes from first call to offer in ten days |
| Support | The customer solves it alone | A customer with an expired card fixes it without writing to support |

Work outside software still gets a check someone else can run. For sales, finance, hiring, and support, the check is usually a date, a record, or an absence (no support ticket was filed). Name where the evidence lives so the next person can look.

## State the done test before starting the work

Write the done test down before starting the work. In a plan, it sits on the slice's `Done test:` line and again in its `#### Execute (Slice N)` brief. In a single turn without a plan, say it in the first lines of the reply: "Done test: `pytest tests/test_checkout.py` passes."

Writing it first does two jobs. It tells the person approving the work what "finished" will mean, and it keeps the work aimed at the outcome while you build. A plan with no done tests is not a plan. If you cannot name how a slice will be proven, research more before presenting it.

## Delegating with done tests

A delegated sub-task is incomplete without a done test.

A subagent works in a bounded context. The orchestrator does not see everything it read, tried, or changed, and reading all of that back would cost nearly as much as doing the work. The done test is the only cheap verification interface between orchestrator and worker. Instead of reviewing every file, the orchestrator can re-run one command and know.

Every delegation prompt ends with a `Verify:` line naming the exact command or check that proves the deliverable:

```text
Verify: pytest tests/test_auth.py passes
```

Two runs close the loop:

1. **The subagent runs the check itself before reporting done.** If it fails, the subagent keeps working or reports the failure. It does not report success.
2. **The orchestrator re-runs the check before accepting the work.** A report that says "passed" is a claim. The re-run is the proof.

In a plan, the delegation shows up as `Owner: delegate(task=..., verify=...)`, and the `verify` part is the slice's done test. The full delegation prompt shape is in `templates/delegation-brief.md`.

## Verify before done

An implementation turn is not complete until its done test has run and passed. Run the project's test command, a build, or, after a deploy, the live `/health` check.

If no done test exists, or it cannot run (no network, missing credentials, a service that is down, a check that needs a human), say so in plain words instead of claiming completion. Use the form "verification wasn't possible because ...", for example:

> Verification wasn't possible because the staging database is unreachable from this session. The change is written; `pytest tests/test_checkout.py` has not run.

That sentence lets the person reading know exactly what is proven and what is still a claim.

**Scope.** This rule covers implementation turns only. Conversation, research, and read-only turns are exempt. Nobody needs a test run to answer a question.

## Recording the proof

After the done test passes, write the command and its outcome into the slice's `Proved by:` line in the plan:

```markdown
- Status: done 2026-10-19
- Proved by: `pytest tests/test_checkout.py` -> 14 passed
```

Record what actually ran and what it actually returned. If the slice shipped something different from the plan, say so on its `Notes:` line. `scripts/check_plan.py` reports an error for any slice marked done without a `Proved by:` line. The plan format is in `references/plan-format.md`.

The next session, or the next owner, reads this line instead of re-deriving what happened. One line per slice is enough.

## Who accepts the work

The worker that did the work should never be the one that declares it accepted. Its own report is the cheapest thing to produce and the easiest to get wrong.

Choose done tests the worker cannot fake:

- **A test suite** that exercises the changed behavior.
- **A build** that exits 0.
- **A live check** against the running system, such as `/health` after a deploy, or `uname -r` after a reboot.
- **A real-world event** with a record: the payment cleared, the quote went out, the candidate signed.

Then let something outside the worker accept the result. That can be a second context (an orchestrator, a reviewer, another agent with fresh eyes) that re-runs the check, or a machine check that runs on its own, such as continuous integration. Turning the done test into something a machine runs is also the fastest way to stop verification from becoming the new queue.
