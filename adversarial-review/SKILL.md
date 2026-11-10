---
name: adversarial-review
description: Adversarially review a PR or diff: hunt for bugs, gaps, and blind spots the author missed, not just whether it matches the plan. Use for "adversarial review", "tear this apart", "what did I miss", or as a second opinion from a different model than the one that wrote the code. Never edits code.
---

Find what is wrong with the change, not whether it looks right. Assume the implementer was overconfident. Find the most likely lies and blind spots in the implementation, the spec, and the modelling.

Input is a PR, the diff the user names, or uncommitted changes plus commits not on the base branch. If `.work/<task-slug>/` holds an agreement, sketch, or report, read them as claims to attack, not as truth.

Review from a different perspective than the author's. If you are the model that wrote the code, say so in one line and review as a stranger anyway: do not trust your memory of why it is correct. Read the whole change, plus the callers, callees, and tests around it.

Hunt for:

1. **Lies in the implementation.** Claims in names, comments, commit messages, or the report that the code does not keep. A function called `validate` that does not reject; "handles retries" with no backoff; "tested" with no test that would fail.
2. **Logic errors.** Off-by-one, inverted conditions, wrong operator, early return that skips cleanup, wrong default, swallowed errors, unit or timezone mix-ups.
3. **Spin bugs.** Loops, retries, polling, or recursion that never terminate or never back off: busy-waits, retry-forever on a permanent error, a re-render or event loop that triggers itself, a lock or await that can deadlock.
4. **Missing edge cases.** Empty, null, zero, negative, huge, duplicate, unicode, concurrent, partial failure, restart midway, clock skew, the first and last element.
5. **Gaps in the spec.** Cases the agreement never decided that the code silently decided anyway. Requirements that contradict each other. "Done when" checks that would pass with the bug still there.
6. **Blind spots in the modelling.** States the types allow that the domain forbids, two flags that must stay in sync, a new branch bolted onto an if-chain, data that can drift between two sources of truth.
7. **Mismatches.** Between spec and code, code and tests, the change and its callers, the new code and the conventions around it. Places the author changed one side and not the other.
8. **Tests that prove nothing.** Tests that pass if the change is reverted, mock the thing under test, or assert on implementation instead of behaviour.

For each suspicion, try to break it: write a failing test, a repro script, or run the code with the hostile input. A proven finding beats a plausible one. Keep unproven findings only when they are high-risk and cannot be run safely; mark them **unproven** and say what would confirm them.

Report each finding with file and line, severity (blocker, should-fix, nit), what is wrong, the proof, and the fix in one sentence. Blockers first. No praise, no restating what the code does. If you tried hard and found nothing, say what you attacked and that it held, in two lines.

Code quality (readability, test quality, design) is a separate skill, `code-quality`, run alongside this one. This review does not cover it.

If there is a `.work/<task-slug>/` folder, write the findings to `adversarial-review.md` there. Do not edit code, commit, or fix anything. Never mention steps or handoffs to the user.
