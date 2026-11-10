---
name: mutate
description: Run the project's mutation testing on a change and report surviving mutants as missing tests. Optional link after implement or review. Never edits code.
---

Input is `.work/<task-slug>/report.md`, or the diff the user names, or uncommitted changes plus commits not on the base branch.

Find the project's own mutation command in its scripts, build config, or docs. If there is none, say so in one line and stop. Do not install or configure a tool.

Limit the run to the changed files or the diff. Never run it on the whole codebase.

The tool makes the mutants and decides which were killed. Do not invent mutants, edit code to make them, or guess a result the tool did not report. Your job is to run the command and read its report.

For each surviving mutant:

- **On new or changed logic,** treat it as a lead for a missing test. Name the behaviour no test checks.
- **Unkillable,** meaning the mutation cannot change observable behaviour: drop it and give the reason in one line.
- **In logging, error messages, or defensive code,** ignore it as noise.

Do not chase a 100% score. A survivor matters only when it points to behaviour a user of the code would notice breaking.

Write `.work/<task-slug>/mutation.md` with: the command run and its summary line, each kept survivor (file and line, the mutation, the missing test in one sentence), and dropped survivors counted by reason.

Do not write tests or edit code. If survivors are kept, the next step is `implement` with this file; route it silently and do not mention steps or handoffs to the user. Otherwise the change is done.
