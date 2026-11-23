---
name: autonomous-delivery
description: Orchestrate an implementation or PR repair through delegated framing, design, implementation, review, validation, and delivery to an auto-merging PR. Use when the user, repository instructions, or an authorized automation opts into autonomous delivery.
---

Own the delivery as lead. Dispatch each stage to a child agent and decide whether its output is ready for the next stage. Keep PR operations and merge decisions with the lead. Repository instructions and the initiating request determine the scope of work. Opting into autonomous delivery authorizes the lead to push a branch, open a PR, and enable auto-merge on it, unless the repository instructions or the request limit that (for example "draft only", "no merge", or "local only").

## Dispatch

Give each child its role, relevant skill, repository and checkout, base and candidate commit where applicable, input artifacts, scope, and expected output. Resolve skill paths from the installed skills or from this skill's siblings in the shared checkout. Ask for artifact locations, decisions or findings, and validation evidence in the return. Children return to the lead at each question or approval checkpoint and at stage completion. The lead owns onward dispatch. Use the host's supported subagent and wait mechanisms. If the host cannot resume a child, dispatch a fresh one with the latest draft, decisions, and the lead's answer or approval. If delegation is unavailable, report the blocked stage.

Keep accepted artifacts under `.work/<task-slug>/` outside commits. For a child in an isolated checkout, pass the accepted artifacts or their contents explicitly and collect its outputs before continuing. Keep one writer per checkout. Integrate an implementation child's commits into the delivery branch before starting reviews. Run concurrent stages against the same committed revision, using separate checkouts for jobs that change sources, build state, or fixtures when they would interfere.

## Frame, model, and implement

1. **Frame.** Dispatch `frame` with the original request and relevant issue context. In this run, the lead is the framing counterpart. The child returns each round of questions with its recommendations, then returns a proposed agreement for confirmation. The lead answers routine decisions from the request, repository conventions, and available evidence, recording material assumptions and reasons. Confirm the agreement only once the goal, scope, and observable acceptance criteria are clear. Have the child produce `agreement.md` after confirmation.
2. **Model.** Dispatch `model` with the accepted agreement. The child returns the design, tradeoffs, and questions to the lead. Review it against the agreement and compatibility with existing callers. Return objections or confirm it, then collect the approved `sketch.md`. Keep both stages' issue publishing steps local unless external posting has been authorized for the lead.
3. **Implement.** Dispatch `implement` with the approved artifacts. The child owns local edits, tests, commits where the skill calls for them, and `report.md`. The lead checks that the report covers acceptance criteria and reconciles material design deviations. If a change invalidates the agreement or sketch, send the affected decision back to the corresponding stage before building further.

These role assignments apply within this workflow. An independent invocation of a stage follows that stage's normal interaction rules. Escalate to the user when a material product decision cannot be made from the delegated scope or when an external permission or required validation is unavailable.

## Review and validate

**Gate.** Before dispatching any reviewer, the lead runs the repository's deterministic checks itself on the candidate commit: what CI runs for formatting, lint, typecheck, build, and tests. A failure goes straight back to the implementation child with the output. No reviewer sees a revision that CI would reject.

**Size the review.** Choose the tier from the diff:

- **Light**, when the change adds no new logic: styles, copy, docs, assets, or config values. Dispatch `review` and manual validation, and run `code-quality` as one pass covering all six dimensions in a single context. Skip `adversarial-review` and `mutate`.
- **Full**, otherwise. Dispatch independent children for `review`, `adversarial-review`, `mutate`, and manual validation. Code quality is a separate track. The lead dispatches the six `code-quality` specialist dimensions directly in fresh contexts, in batches within the host's concurrency limit. Give each specialist the diff, its dimension, and the skill's reporting rubric. Apply the skill's aggregation rules to their returns. The `mutate` child owns mutation testing for the run. Record it as unavailable when the project has no mutation command.

Give test strength one owner per run: `mutate` when the project has a mutation command, otherwise the `code-quality` test-quality specialist. Tell the other reviewers to report a weak or missing test only when it hides a bug they proved.

The manual-validation child exercises the changed behavior through its normal entry point using the agreement's scenarios and the repository's tooling. Collect the command or environment, expected and observed behavior, and any scenario the child could not exercise. Use those results alongside the repository's prescribed tests and CI.

**Triage.** Triage findings against the acceptance criteria and evidence. Only blockers and should-fix findings start a repair cycle. The lead fixes nits inline when cheap, or drops them. Resolve small fixes as required by the host's orchestration rules. Send substantial confirmed fixes or missing tests to an implementation child. Pass the lead's curated findings as that run's repair input, superseding older review and mutation reports in the checkout. A finding that reopens an agreement or sketch decision goes to `frame` or `model`, not to `implement`.

**Re-review.** After a repair, run the gate again. Then re-dispatch only the checks whose findings were repaired, against the repair delta, with the earlier findings to confirm. A re-review raises new findings only for blockers in the delta. After two repair rounds, the lead decides each open finding itself: fix it, accept it with a reason, or escalate it to the user. If the same blocker recurs without a new diagnosis or viable fix, record the evidence and stop the retry loop.

## Learn from repair cycles

Every finding that starts a repair cycle, and every gate failure, goes in the delivery ledger. Log each one with `python3 <this skill>/scripts/ledger.py add`. Give it the repository, task slug, round, source (the reviewer, `gate`, or `ci`), severity, a kebab-case cause tag naming the root cause (for example `untested-guard`, `spec-gap-empty-state`, `lint-not-run`), a one-line summary, and the prevention that would have stopped it earlier. Use one of `none`, `lint`, `ci`, `repo-instructions`, or `skill:<name>`. Reuse an existing tag when the cause matches; `ledger.py tags` lists them.

Before returning, run `ledger.py report` and bring `LESSONS.md` at the root of the skills checkout (next to this skill's folder) up to date. It is the shared, cross-project record of recurring causes. For each recurring cause the report flags, add this run's findings as evidence under its entry, or create the entry if it has none. Then set or sharpen its proposal: the lint rule or check to add to the repository, or the line to add to the named skill. Leave the status of new and existing proposals as they are. In the return, name the entries you added or changed. `LESSONS.md` is the only file outside the task you may edit: propose the skill or tooling changes there, and make none of them.

## Deliver and resume

For an existing PR, start from its current head and recover the acceptance criteria from its issue, description, and repository context. Use framing or modelling for decisions still open. Keep CI-only repairs scoped to the failure and use the relevant review and validation stages. Automated intake checks only work items within its configured scope.

Delivery ends at a merged PR, not at a reviewed branch. Once review and validation cover the candidate commit:

1. Push the delivery branch and open the PR, or update the existing one. Use `describe` for its title and description, and record the reviewed commit and validation evidence in it. In T3, link each PR you create, take over, or push to on the next call.
2. Enable auto-merge pinned to the reviewed head: `gh pr merge <pr> --auto --squash --match-head-commit <sha>`. Squash by default. Use `--rebase` instead when every commit on the branch is clean and meaningful on its own, and the repository allows it. Use the repository's prescribed method when it has one. If the repository does not allow auto-merge, merge directly with the same expected head once the required checks pass. If the request or repository limits delivery to a draft or an unmerged PR, stop after step 1 and say so.
3. Watch the PR until it merges, following the host's watch instructions.

On wake, read the current head, checks, and review state. If the head moved, inspect the new commits, confirm the scope still applies, and base any repair on the new head. Delegate diagnosis of failures or review feedback as needed, fix and revalidate the affected behavior, push the repair, and re-enable auto-merge pinned to the new head. Log the CI failure or review comment in the ledger like any other repair cycle. If the push is rejected because the head moved again, inspect the new head before retrying.

Merge only with the workflow's review and validation covering the current head and repository-required checks and reviews satisfied. Verify the merge and any post-merge checks required by the repository or request. Return the PR, its merge state, evidence, material assumptions, ledger proposals, and any blocked validation or follow-up.
