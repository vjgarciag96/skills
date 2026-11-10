---
name: review
description: Review a change against its agreement and sketch and report only findings proven by a run. Last link of the chain. Never edits code.
---

Input is `.work/<task-slug>/report.md` with the agreement and sketch beside it. Without them, review the diff the user names, or uncommitted changes plus commits not on the base branch.

Read the whole change, plus enough surrounding code to judge it in context.

Check, in this order:

1. **Correctness.** Does it meet "Done when"? Edge cases, error paths, concurrency, data loss.
2. **Modelling.** Does the code match the sketch's structure? A new branch on an existing if-chain, or a second flag that must stay in sync with another, means the modelling was skipped.
3. **Architecture.** Right layer, right boundaries, fits the existing design.
4. **Security.** Untrusted input reaching queries, shells, or files; secrets in code or logs; missing auth checks.
5. **Maintainability.** Dead code left behind, duplication, abstraction that removes no branches or invalid states.
6. **Readability.** Can a human follow it in one pass? Comments that restate the code or explain no real why.
7. **Tests.** Do they check observable behaviour, and would they fail if the change broke?

Prove each correctness or test finding with a run: a failing test, a repro script, or command output that shows the wrong behaviour. Drop any such finding you could not prove. Security findings get a repro where one is safe to run. Findings in 2 to 6 cite file and line and the concrete cost.

Write `.work/<task-slug>/review.md` with each finding: file and line, severity (blocker, should-fix, nit), what is wrong, the proof, the fix in one sentence. Blockers first. No praise. If nothing is worth raising, say so in one line.

Mutation testing is a separate, optional skill, `mutate`. This review does not depend on it.

Do not edit code, commit, or fix anything. If there are findings, the next step is `implement` with this file; route it silently and do not mention steps or handoffs to the user. Otherwise the change is ready.
