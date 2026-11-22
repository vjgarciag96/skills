#!/usr/bin/env python3
"""Record what sends autonomous deliveries back for repair, and report recurring causes.

The ledger is JSON Lines at $DELIVERY_LEDGER, default ~/.agents/delivery-ledger.jsonl.
"""

import argparse
import json
import os
import re
import sys
from collections import Counter, defaultdict
from datetime import datetime, timezone
from pathlib import Path

LEDGER = Path(os.environ.get("DELIVERY_LEDGER", Path.home() / ".agents" / "delivery-ledger.jsonl"))
SEVERITIES = ("blocker", "should-fix")
PREVENTION = re.compile(r"^(none|lint|ci|repo-instructions|skill:[a-z0-9-]+)$")
TAG = re.compile(r"^[a-z0-9]+(-[a-z0-9]+)*$")
RECURRING_COUNT = 3
RECURRING_TASKS = 2


def read():
    if not LEDGER.exists():
        return []
    with LEDGER.open() as f:
        return [json.loads(line) for line in f if line.strip()]


def add(args):
    if not TAG.match(args.cause):
        sys.exit(f"cause must be a kebab-case tag, got {args.cause!r}")
    if not PREVENTION.match(args.prevention):
        sys.exit(f"prevention must be none, lint, ci, repo-instructions or skill:<name>, got {args.prevention!r}")
    entry = {
        "at": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "repo": args.repo,
        "task": args.task,
        "round": args.round,
        "source": args.source,
        "severity": args.severity,
        "cause": args.cause,
        "summary": args.summary,
        "prevention": args.prevention,
    }
    LEDGER.parent.mkdir(parents=True, exist_ok=True)
    with LEDGER.open("a") as f:
        f.write(json.dumps(entry) + "\n")
    print(f"logged {args.cause} to {LEDGER}")


def tags(_):
    for cause, n in Counter(e["cause"] for e in read()).most_common():
        print(f"{n:4}  {cause}")


def report(args):
    entries = read()
    if args.repo:
        entries = [e for e in entries if e["repo"] == args.repo]
    if not entries:
        print("ledger is empty")
        return

    by_cause = defaultdict(list)
    for e in entries:
        by_cause[e["cause"]].append(e)
    rounds = defaultdict(int)
    for e in entries:
        key = (e["repo"], e["task"])
        rounds[key] = max(rounds[key], e["round"])

    print(f"{len(entries)} repair findings across {len(rounds)} tasks\n")
    print("By source:")
    for source, n in Counter(e["source"] for e in entries).most_common():
        print(f"{n:4}  {source}")
    print("\nBy cause:")
    for cause, es in sorted(by_cause.items(), key=lambda kv: -len(kv[1])):
        tasks = {(e["repo"], e["task"]) for e in es}
        preventions = sorted({e["prevention"] for e in es})
        print(f"{len(es):4}  {cause}  ({len(tasks)} tasks; prevention: {', '.join(preventions)})")
    print("\nMost repair rounds:")
    for (repo, task), n in sorted(rounds.items(), key=lambda kv: -kv[1])[:5]:
        print(f"{n:4}  {repo} {task}")

    recurring = [
        (cause, es) for cause, es in by_cause.items()
        if len(es) >= RECURRING_COUNT and len({(e["repo"], e["task"]) for e in es}) >= RECURRING_TASKS
    ]
    print("\nRecurring causes, each needs a prevention proposal:")
    if not recurring:
        print("   none")
    for cause, es in recurring:
        print(f"  - {cause}: {len(es)} findings, e.g. {es[-1]['summary']}")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(required=True)

    p = sub.add_parser("add", help="log one finding that started a repair cycle")
    p.add_argument("--repo", required=True)
    p.add_argument("--task", required=True)
    p.add_argument("--round", required=True, type=int)
    p.add_argument("--source", required=True, help="reviewer, gate, or ci")
    p.add_argument("--severity", required=True, choices=SEVERITIES)
    p.add_argument("--cause", required=True, help="kebab-case root cause tag")
    p.add_argument("--summary", required=True)
    p.add_argument("--prevention", required=True)
    p.set_defaults(run=add)

    p = sub.add_parser("tags", help="list cause tags already in use")
    p.set_defaults(run=tags)

    p = sub.add_parser("report", help="summarize causes and flag recurring ones")
    p.add_argument("--repo")
    p.set_defaults(run=report)

    args = parser.parse_args()
    args.run(args)


if __name__ == "__main__":
    main()
