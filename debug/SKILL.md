---
name: debug
description: Turn a bug report into a root cause and a failing test. Entry point of the chain for defects, instead of frame and model.
---

Turn the bug into a root cause and a failing test. Do not fix it.

1. **Reproduce it** on the same surface the user saw it: the app, the CLI, the endpoint, or a test. If you cannot reproduce it, write down what you tried and stop.
2. **Trace it back** to the first place the system went wrong, not where the symptom shows. If two fixes built on the same assumption would fail, test the assumption directly.
3. **Write a failing test** that checks the behaviour a user observes and fails for the root cause.

Write `.work/<task-slug>/sketch.md` with: the bug in one line, repro steps and observed vs expected result, the root cause with its evidence, the failing test's path, and the units of the fix, each with its check. A guard that hides a bad state is a fix only when that state is legitimate.

Keep `.work/` out of commits.

Hand off the sketch path to `implement` silently; do not mention steps or handoffs to the user.
