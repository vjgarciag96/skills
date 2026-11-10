---
name: code-quality
description: Review a PR or diff for code quality, not bugs: readability, test quality, encapsulation, SOLID, cohesion, and API depth, each judged by its own specialist in a fresh context. Use for "code quality review", "is this clean", or alongside adversarial-review. Never edits code.
---

Judge how good the change is to live with, not whether it works. Bugs, lies, and edge cases belong to `adversarial-review`; do not report them here.

Input is a PR, the diff the user names, or uncommitted changes plus commits not on the base branch.

## Specialists

Run one specialist per dimension below, each in its own fresh context (a subagent), seeing only the diff, the code around it, and its own dimension. A specialist does not see the others' findings.

1. **Readability.** How hard is this for a human to read in one pass? Names that hide intent, deep nesting, long functions, clever one-liners, control flow that needs a debugger to follow.
2. **Test quality.** What do the tests buy, and can they be read? Three passes:
   - **Assertion strength.** Would the test fail if the behaviour broke? Asserts that check only "not null" or "was called" are weak.
   - **No copied formulas.** Expected values computed with the same logic as the code under test stay green when both are wrong. Expected values should be literal.
   - **Readable tests.** Arrange, act, assert; one concept per test; a name that states the scenario. Judge by the `tests` skill.
   Mutation testing is an optional hook: if the project has a mutation command, run it on the changed modules (see `mutate`) and treat surviving mutants as findings.
3. **Encapsulation.** Internal state or representation leaking through public API, callers reaching into internals, getters and setters that expose what should be decided inside.
4. **SOLID.** A class or module with more than one reason to change, extension by editing a switch, subtypes that break their parent's contract, fat interfaces, high-level code depending on concrete details.
5. **Cohesion.** Things that change together living apart, unrelated things sharing a module, a grab-bag `utils`.
6. **API depth.** Deep modules hide a lot behind a small interface. Flag shallow ones: pass-through methods, wrappers that add a name and nothing else, interfaces as complex as their implementation.

Every specialist also hunts the AI smells in its dimension:
- duplication and copy-paste instead of reuse,
- error-masking: swallowed exceptions, broad catches, silent defaults,
- over-abstraction: layers, interfaces, or config for one caller,
- comment noise: comments that restate the code,
- dead code: unused functions, params, branches, imports,
- hollow tests: tests that cannot fail,
- over-mocking, including tests that mock the code under test,
- assertion roulette: many asserts with no message saying which failed.

## Rubric

Each finding gets a level:
- **blocker:** will cost real time soon: an unreadable core path, tests that cannot fail, a leak that callers already depend on.
- **should-fix:** a clear cost, but local and cheap to fix now.
- **nit:** taste. Drop any nit you cannot prove.

Prove findings where cheap. A hollow test: invert the logic and show the test still passes. A shallow API: name the pass-through and what it forwards to. Duplication: cite both locations. Dead code: show it has no callers.

Each specialist returns only findings, each with: file and line, level, confidence 0 to 100, the finding in one sentence, the proof if any, and a one-line cause tag (for example `cause: copy-paste instead of extracting a helper`). No praise, no summary.

## Merge

Keep only findings with confidence 80 or above. Group findings whose cause tags match across dimensions into one entry listing every location and dimension. Order blockers first. Do not re-judge the findings.

If there is a `.work/<task-slug>/` folder, write the result to `code-quality.md` there. If nothing passes the threshold, say so in one line.

Do not edit production code, commit, or fix anything. Never mention steps or handoffs to the user.
