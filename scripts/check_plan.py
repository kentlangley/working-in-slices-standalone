#!/usr/bin/env python3
# SPDX-License-Identifier: MIT
# Copyright (c) 2026 unixguru2k; Copyright (c) 2026 Kent Langley
"""Check a slice plan document against the plan format.

Usage:
    python3 scripts/check_plan.py PLAN.md [PLAN.md ...] [--json] [--strict]

Read only: it never moves or edits a file. It prints one line per finding
(ERROR or WARN, the slice number when there is one, and the fix) and one
summary line per file. When every slice is done and the plan is not in
plans/archive/, it prints the command that archives it.

Exit codes: 0 no errors, 1 errors (or warnings with --strict), 2 usage
error or unreadable file. The format is described in references/plan-format.md.
"""
from __future__ import annotations

import argparse
import json
import os
import re
import shlex
import sys

SLICE_FIELDS = ("Ships", "Touches", "Done test", "Owner", "Out for now",
                "Status", "Proved by", "Notes")
BRIEF_FIELDS = ("Done test", "Decisions frozen")
HINTS = {
    "Ships": "what the user can do after this slice that they could not before",
    "Touches": "the layers or files the slice changes",
    "Done test": "the command or check that proves the slice",
}
STATUSES = ("planned", "in progress", "done", "deferred")

FENCE = re.compile(r"^ {0,3}(`{3,}|~{3,})")
HEADING = re.compile(r"^(#{1,6})\s+(.*\S)\s*$")
SLICE_HEAD = re.compile(r"Slice\s+(\d+)\s*:\s*(.*)")
BRIEF_HEAD = re.compile(r"Execute\s*\(\s*Slice\s+(\d+)\s*\)")
FIELD = re.compile(r"^ {0,3}[-*]\s+([A-Z][A-Za-z ]*?):[ \t]*(.*)$")
LIST_ITEM = re.compile(r"^\s*([-*]|\d+\.)\s")
PLAN_STATUS = re.compile(r"^ {0,3}(?:[-*]\s+)?Status:[ \t]*(.*)$")
DELEGATE = re.compile(r"delegate\(\s*task\s*=(.*?),\s*verify\s*=(.*)\)", re.S)
IMPL_WORD = re.compile(r"\b(table|column|endpoint|ticket|refactor|schema|migration)\b", re.I)
SNAKE_CASE = re.compile(r"\b[a-z][a-z0-9]*(?:_[a-z0-9]+)+\b")
CAMEL_CASE = re.compile(r"\b[a-z]+[A-Z][A-Za-z0-9]*\b")


def is_placeholder(value):
    """Empty, wholly inside <...>, or one of TBD, TODO, ?, ..., and the ellipsis."""
    v = value.strip()
    return (not v or re.fullmatch(r"<[^<>]*>", v) is not None
            or v.upper() in ("TBD", "TODO", "?", "...", "\u2026"))


def parse(text):
    """Split a plan into its plan-level status, slices, and Execute briefs."""
    plan = {"status": None, "slices": [], "briefs": {}, "bad_heads": []}
    current, allowed, last, fence = None, (), None, None
    for no, raw in enumerate(text.splitlines(), 1):
        if fence:  # inside a fenced code block: ignore everything
            close = r"^ {0,3}%s{%d,}\s*$" % (re.escape(fence[0]), len(fence))
            if re.match(close, raw):
                fence = None
            continue
        opened = FENCE.match(raw)
        if opened:
            fence, last = opened.group(1), None
            continue
        head = HEADING.match(raw)
        if head:
            current, allowed, last = None, (), None
            level, title = len(head.group(1)), head.group(2)
            if level == 3 and re.match(r"Slice\b", title):
                sm = SLICE_HEAD.fullmatch(title)
                if sm:
                    current = {"num": int(sm.group(1)), "name": sm.group(2).strip(),
                               "line": no, "fields": {}}
                    plan["slices"].append(current)
                    allowed = SLICE_FIELDS
                else:
                    plan["bad_heads"].append(title)
            elif level == 4 and BRIEF_HEAD.fullmatch(title):
                current = {"line": no, "fields": {}}
                plan["briefs"].setdefault(int(BRIEF_HEAD.fullmatch(title).group(1)), current)
                allowed = BRIEF_FIELDS
            continue
        if not plan["slices"] and plan["status"] is None:
            ps = PLAN_STATUS.match(raw)
            if ps and ps.group(1).strip():
                plan["status"] = ps.group(1).strip()
        fm = FIELD.match(raw)
        if fm and current is not None and fm.group(1) in allowed:
            current["fields"].setdefault(fm.group(1), fm.group(2).strip())
            last = (current["fields"], fm.group(1))
        elif last and raw.startswith("  ") and raw.strip() and not LIST_ITEM.match(raw):
            fields, key = last  # a wrapped continuation of the previous value
            fields[key] = (fields[key] + " " + raw.strip()).strip()
        else:
            last = None
    return plan


def status_kind(value):
    """Return planned, in progress, done, or deferred; None when invalid."""
    low = value.strip().lower()
    for kind in STATUSES:
        if low == kind or (kind in ("done", "deferred") and re.match(re.escape(kind) + r"[\s:,(]", low)):
            return kind
    return None


def owner_problem(value):
    """Return what is wrong with an Owner value, or None when it is valid."""
    v = value.strip()
    if is_placeholder(v):
        return "Owner is a placeholder. Write self, or delegate(task=..., verify=...)."
    if v == "self":
        return None
    if v.startswith("delegate"):
        m = DELEGATE.fullmatch(v)
        if m is None or is_placeholder(m.group(2)):
            return "Owner delegate has no verify. Write delegate(task=..., verify=...) with the command that proves the task."
        if is_placeholder(m.group(1)):
            return "Owner delegate has no task. Write delegate(task=..., verify=...) with what the subagent builds."
        return None
    return "Owner must be exactly self or delegate(task=..., verify=...)."


def name_problem(name):
    if is_placeholder(name):
        return "The slice name is a placeholder. Name it in domain language, as \"<who> can <do what>\"."
    if "`" in name or IMPL_WORD.search(name) or SNAKE_CASE.search(name) or CAMEL_CASE.search(name):
        return "The slice name reads like implementation language. Rewrite it as \"<who> can <do what>\"."
    return None


def archive_command(path, in_plans):
    folder = os.path.join(os.path.dirname(path), "archive") if in_plans else os.path.join("plans", "archive")
    dest = os.path.join(folder, os.path.basename(path))
    return "mkdir -p %s && mv %s %s" % (shlex.quote(folder), shlex.quote(path), shlex.quote(dest))


def check_slice(s, brief, add):
    """Add findings for one slice and its brief. Returns the slice's status kind."""
    n, f = s["num"], s["fields"]
    problem = name_problem(s["name"])
    if problem:
        add("WARN", n, problem)
    for key in ("Ships", "Touches", "Done test"):
        if key not in f:
            add("ERROR", n, "%s is missing. Add a \"- %s:\" line with %s." % (key, key, HINTS[key]))
        elif is_placeholder(f[key]):
            add("ERROR", n, "%s is a placeholder. Write %s." % (key, HINTS[key]))
    if "Owner" not in f:
        add("ERROR", n, "Owner is missing. Add \"- Owner: self\" or \"- Owner: delegate(task=..., verify=...)\".")
    elif owner_problem(f["Owner"]):
        add("ERROR", n, owner_problem(f["Owner"]))
    if "Out for now" not in f or is_placeholder(f["Out for now"]):
        add("WARN", n, "Out for now is missing. Say what this slice leaves out, or write \"nothing\".")
    kind = None
    if "Status" not in f:
        add("WARN", n, "Status is missing. Add \"- Status: planned\" (or in progress, done, deferred).")
    else:
        kind = status_kind(f["Status"])
        if kind is None:
            add("WARN", n, "Status \"%s\" is not one of: %s." % (f["Status"], ", ".join(STATUSES)))
    if kind == "done" and ("Proved by" not in f or is_placeholder(f["Proved by"])):
        add("ERROR", n, "Proved by is missing. The slice is done, so record the command and its outcome.")
    if brief is None:
        add("ERROR", n, "has no Execute brief. Add \"#### Execute (Slice %d)\" with steps, Done test, and Decisions frozen." % n)
        return kind
    bf = brief["fields"]
    if "Done test" not in bf or is_placeholder(bf["Done test"]):
        add("ERROR", n, "Execute brief is missing Done test. Add \"- Done test:\" with the exact command.")
    elif "Done test" in f and not is_placeholder(f["Done test"]):
        same = lambda v: " ".join(v.replace("`", "").split())
        if same(bf["Done test"]) != same(f["Done test"]):
            add("WARN", n, "Execute brief Done test differs from the slice Done test. Make them match.")
    if is_placeholder(bf.get("Decisions frozen", "")):
        add("ERROR", n, "Execute brief is missing Decisions frozen. Add \"- Decisions frozen:\" naming what applies as written.")
    return kind


def check(path, text):
    plan = parse(text)
    findings = []

    def add(level, num, msg):
        findings.append((level, num, msg))

    slices = plan["slices"]
    abs_parts = os.path.abspath(path).split(os.sep)
    in_archive = len(abs_parts) >= 3 and abs_parts[-2] == "archive" and abs_parts[-3] == "plans"
    in_plans = len(abs_parts) >= 2 and abs_parts[-2] == "plans"

    for title in plan["bad_heads"]:
        add("ERROR", None, "Heading \"%s\" is not a slice heading. Write it as \"### Slice N: name\"." % title)
    if not slices:
        add("ERROR", None, "No slices found. Add headings like \"### Slice 1: Customers can do something\".")
    seen = set()
    for s in slices:
        if s["num"] in seen:
            add("WARN", s["num"], "appears more than once. Give each slice its own number.")
        seen.add(s["num"])
    for num in sorted(set(plan["briefs"]) - seen):
        add("WARN", num, "Execute brief has no matching slice heading. Fix the number or remove the brief.")

    kinds = {}
    for s in slices:
        kinds[id(s)] = check_slice(s, plan["briefs"].get(s["num"]), add)
    done = sum(1 for k in kinds.values() if k == "done")
    deferred = [s["num"] for s in slices if kinds[id(s)] == "deferred"]

    if plan["status"] is None:
        why = " Slice %s is deferred, so the line must name what remains." % deferred[0] if deferred else ""
        add("WARN", None, "Plan Status line is missing. Add \"Status: ...\" before the first slice: how many slices are done and what is next." + why)
    if not (in_plans or in_archive):
        add("WARN", None, "File is not inside a plans/ folder. Save it as plans/<slug>.md.")
    if in_archive:
        for s in slices:
            if kinds[id(s)] not in ("done", "deferred"):
                add("ERROR", s["num"], "is not done or deferred, yet the plan is in plans/archive/. Move the plan back to plans/ or finish the slice.")
    ready = bool(slices) and done == len(slices) and not in_archive
    if ready:
        add("WARN", None, "Every slice is done. Archive the plan: " + archive_command(path, in_plans))

    errors = [(n, m) for lv, n, m in findings if lv == "ERROR"]
    warnings = [(n, m) for lv, n, m in findings if lv == "WARN"]
    return {"path": path, "slices": len(slices), "done": done, "findings": findings,
            "errors": errors, "warnings": warnings, "ready_to_archive": ready}


def text_of(num, msg):
    return ("Slice %d: %s" % (num, msg)) if num is not None else msg


def plural(n, word):
    return "%d %s%s" % (n, word, "" if n == 1 else "s")


def report(result):
    for level, num, msg in result["findings"]:
        print("%s: %s %s" % (result["path"], level, text_of(num, msg)))
    print("%s: %s, %d done, %s, %s" % (
        result["path"], plural(result["slices"], "slice"), result["done"],
        plural(len(result["errors"]), "error"), plural(len(result["warnings"]), "warning")))


def main(argv=None):
    ap = argparse.ArgumentParser(
        prog="check_plan.py",
        description="Check slice plan documents against the plan format. Read only.",
        epilog="Exit codes: 0 no errors, 1 errors (or warnings with --strict), 2 usage error or unreadable file.")
    ap.add_argument("plans", nargs="+", metavar="PLAN.md", help="plan files to check")
    ap.add_argument("--json", action="store_true", help="print a JSON list with one object per file")
    ap.add_argument("--strict", action="store_true", help="treat warnings as failures")
    args = ap.parse_args(argv)

    results, unreadable = [], False
    for path in args.plans:
        try:
            with open(path, encoding="utf-8-sig") as fh:
                text = fh.read()
        except (OSError, UnicodeDecodeError) as exc:
            print("check_plan.py: cannot read %s: %s" % (path, exc), file=sys.stderr)
            unreadable = True
            continue
        results.append(check(path, text))

    if args.json:
        keys = ("path", "slices", "done", "errors", "warnings", "ready_to_archive")
        out = [dict(r, errors=[text_of(*e) for e in r["errors"]],
                    warnings=[text_of(*w) for w in r["warnings"]]) for r in results]
        print(json.dumps([{k: o[k] for k in keys} for o in out], indent=2))
    else:
        for r in results:
            report(r)
    if unreadable:
        return 2
    failed = any(r["errors"] or (args.strict and r["warnings"]) for r in results)
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
