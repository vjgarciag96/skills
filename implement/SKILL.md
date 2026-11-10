---
name: implement
description: Build a design sketch unit by unit and prove each one works. Third link of the chain.
---

Input is `.work/<task-slug>/sketch.md` and the agreement beside it. If there is a `review.md` or `mutation.md` too, fix its findings instead and nothing else.

Build what you are given, at the size it comes in: a whole feature, one slice, or a smaller task. Slicing is not your job; do not split, merge, or reorder the work yourself. If the sketch lists `- [ ]` units, build them in order, and if some are already ticked, resume from the first unticked one. Otherwise treat the whole input as one unit.

Make the deletions first.

Then build each unit in order:

1. Where there is a clear seam, write a failing test that checks behaviour a user of the code can observe. Write it by **Tests** below.
2. Fill in the sketch until the check passes.
3. Run the typechecker and the unit's tests. Do not start the next unit with anything failing.
4. Commit the unit with a message written per the `describe` skill (title alone is fine for a small unit), then tick it in the sketch. Unit commits don't wait for approval.

**Tests.** Write every unit test, and any other test, by the `tests` skill (`~/.agents/skills/tests/SKILL.md`).

The sketch is the contract. If the code needs something the sketch did not plan for, decide whether the sketch was wrong, the agreement missed it, or the code is overreaching, and record the answer. If the same workaround keeps appearing, stop and send it back to `model`.

Follow the code's existing patterns and names. No speculative abstractions, no unrelated cleanups. Keep a comment only for a why the code cannot show.

When the units are done, run what CI runs, the full test suite, and every check under "Done when". Where the change has a running surface (an app, a CLI, an endpoint), exercise it there. Observe the real result, not a proxy.

Write `.work/<task-slug>/report.md` with: commits, checks run with their output, sketch deviations and why, anything left open.

Keep the work local: commit on a branch, but do not push or open a pull request. The user iterates locally first and opens the PR when they ask for it. When they do, write its title and description with `describe` against the final diff.

Do not review your own work. Hand off the report path to `review` silently; do not mention steps or handoffs to the user.
