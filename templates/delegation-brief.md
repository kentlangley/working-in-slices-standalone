# Delegation brief

Copy the prompt below into your agent's delegation tool (a subagent, a task, a worker). Fill every angle bracket. Take the slice name, the files, and the steps from the slice and its Execute brief in the plan. The Verify line goes last, and the sentence above it stays.

A delegated slice without a Verify line is unfinished work. The line gives you one command to re-run when the subagent reports back, so you confirm the result without reading the whole transcript.

## The prompt

```text
You are implementing one slice of a larger plan. Work on this slice only.

Slice: <name in domain language, "who can do what">

What it ships: <what the user can do after this that they could not do before>

Files you may touch:
- <path, folder, or layer>
- <path, folder, or layer>

Steps:
1. <imperative step, pointing at a design section instead of restating it>
2. <imperative step>
3. <imperative step>

Out of scope:
- <what this slice leaves out>
- <anything nearby you might be tempted to fix>

Constraints:
- Do not redesign. The design decisions for this slice are frozen.
- Touch only the files listed above.
- If the brief is wrong or incomplete, stop and report the discrepancy. Do not improvise a new design.

Return:
- What you changed, one line per file.
- Anything you left out, deferred, or discovered along the way.
- The exact output of the Verify command below.

Run the Verify command yourself before reporting done. If it fails, fix the work or report the failure. Never report done on a failing check.

Verify: <the exact command or check that proves the deliverable>
```

## Example: a code slice

```text
You are implementing one slice of a larger plan. Work on this slice only.

Slice: Users can sign in with a one-time code sent by email

What it ships: A user who forgot their password can request a six-digit code, enter it, and land signed in.

Files you may touch:
- src/auth/otp.py
- src/auth/routes.py
- tests/test_auth.py

Steps:
1. Add code generation and expiry (10 minutes) in src/auth/otp.py, as the Design section describes.
2. Add the request-code and verify-code routes in src/auth/routes.py.
3. Add tests for a valid code, an expired code, and a reused code.

Out of scope:
- Rate limiting
- Changing the password flow

Constraints:
- Do not redesign. The design decisions for this slice are frozen.
- Touch only the files listed above.
- If the brief is wrong or incomplete, stop and report the discrepancy. Do not improvise a new design.

Return:
- What you changed, one line per file.
- Anything you left out, deferred, or discovered along the way.
- The exact output of the Verify command below.

Run the Verify command yourself before reporting done. If it fails, fix the work or report the failure. Never report done on a failing check.

Verify: pytest tests/test_auth.py passes
```

## Example: a deploy slice

```text
You are implementing one slice of a larger plan. Work on this slice only.

Slice: Customers can check an order's status from the live site

What it ships: The order status page is deployed to production and the service reports itself healthy.

Files you may touch:
- deploy/production.yml
- src/health.py

Steps:
1. Add the order status route to the production deploy file, following the staging entry.
2. Make src/health.py report the status route as a dependency.
3. Deploy with the project's deploy command and wait for it to finish.

Out of scope:
- Staging changes
- Any change to the order data model

Constraints:
- Do not redesign. The design decisions for this slice are frozen.
- Touch only the files listed above.
- If the brief is wrong or incomplete, stop and report the discrepancy. Do not improvise a new design.

Return:
- What you changed, one line per file.
- Anything you left out, deferred, or discovered along the way.
- The exact output of the Verify command below.

Run the Verify command yourself before reporting done. If it fails, fix the work or report the failure. Never report done on a failing check.

Verify: curl -fsS https://app.example.com/health returns HTTP 200 with "status":"ok" after the deploy finishes
```
