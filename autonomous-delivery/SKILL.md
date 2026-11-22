---
name: autonomous-delivery
description: Orchestrate an implementation or PR repair through delegated framing, design, implementation, review, validation, and authorized delivery. Use when the user, repository instructions, or an authorized automation opts into autonomous delivery.
---

Own the delivery as lead. Dispatch each stage to a child agent and decide whether its output is ready for the next stage. Keep PR operations and merge decisions with the lead. Repository instructions and the initiating request determine the scope of work and the authorization to publish or merge.

## Dispatch

Give each child its role, relevant skill, repository and checkout, base and candidate commit where applicable, input artifacts, scope, and expected output. Resolve skill paths from the installed skills or from this skill's siblings in the shared checkout. Ask for artifact locations, decisions or findings, and validation evidence in the return. Children return to the lead at each question or approval checkpoint and at stage completion. The lead owns onward dispatch. Use the host's supported subagent and wait mechanisms. If the host cannot resume a child, dispatch a fresh one with the latest draft, decisions, and the lead's answer or approval. If delegation is unavailable, report the blocked stage.

Keep accepted artifacts under `.work/<task-slug>/` outside commits. For a child in an isolated checkout, pass the accepted artifacts or their contents explicitly and collect its outputs before continuing. Keep one writer per checkout. Integrate an implementation child's commits into the delivery branch before starting reviews. Run concurrent stages against the same committed revision, using separate checkouts for jobs that change sources, build state, or fixtures when they would interfere.

## Frame, model, and implement

1. **Frame.** Dispatch `frame` with the original request and relevant issue context. In this run, the lead is the framing counterpart. The child returns each round of questions with its recommendations, then returns a proposed agreement for confirmation. The lead answers routine decisions from the request, repository conventions, and available evidence, recording material assumptions and reasons. Confirm the agreement only once the goal, scope, and observable acceptance criteria are clear. Have the child produce `agreement.md` after confirmation.
2. **Model.** Dispatch `model` with the accepted agreement. The child returns the design, tradeoffs, and questions to the lead. Review it against the agreement and compatibility with existing callers. Return objections or confirm it, then collect the approved `sketch.md`. Keep both stages' issue publishing steps local unless external posting has been authorized for the lead.
3. **Implement.** Dispatch `implement` with the approved artifacts. The child owns local edits, tests, commits where the skill calls for them, and `report.md`. The lead checks that the report covers acceptance criteria and reconciles material design deviations. If a change invalidates the agreement or sketch, send the affected decision back to the corresponding stage before building further.

These role assignments apply within this workflow. An independent invocation of a stage follows that stage's normal interaction rules. Escalate to the user when a material product decision cannot be made from the delegated scope or when an external permission or required validation is unavailable.

## Review and validate

After implementation, dispatch independent children for `review`, `adversarial-review`, `mutate`, and manual validation. Code quality is a separate track. The lead dispatches the six `code-quality` specialist dimensions directly in fresh contexts, in batches within the host's concurrency limit. Give each specialist the diff, its dimension, and the skill's reporting rubric. Apply the skill's aggregation rules to their returns. The `mutate` child owns mutation testing for the run. Record it as unavailable when the project has no mutation command.

The manual-validation child exercises the changed behavior through its normal entry point using the agreement's scenarios and the repository's tooling. Collect the command or environment, expected and observed behavior, and any scenario the child could not exercise. Use those results alongside the repository's prescribed tests and CI.

Triage findings against the acceptance criteria and evidence. Resolve small fixes as required by the host's orchestration rules. Send substantial confirmed fixes or missing tests to an implementation child. Pass the lead's curated findings as that run's repair input, superseding older review and mutation reports in the checkout. Review and validate the updated revision with fresh children for the affected checks. If the same blocker recurs without a new diagnosis or viable fix, record the evidence and stop the retry loop.

## Deliver and resume

For an authorized existing PR, start from its current head and recover the acceptance criteria from its issue, description, and repository context. Use framing or modelling for decisions still open. Keep CI-only repairs scoped to the failure and use the relevant review and validation stages. Automated intake checks only work items within its configured scope.

The lead pushes, opens or updates the PR, and records the reviewed commit and validation evidence when authorized. Use `describe` for PR copy. In T3, link each PR you create, take over, or push to on the next call. Use the PR watch to resume when work is pending, following the host's watch instructions. On wake, read the current head, checks, and review state. If the head moved, inspect the new commits, confirm the scope still applies, and base any repair on the new head. Delegate diagnosis of failures or review feedback as needed, fix and revalidate the affected behavior, and push the repair. If the push is rejected because the head moved again, inspect the new head before retrying.

Merge only within the standing or task-specific merge authorization, with the workflow's review and validation covering the current head and repository-required checks and reviews satisfied. Use the host's expected-head merge option where available. Verify the merge and any post-merge checks required by the repository or request. Return the PR, evidence, material assumptions, and any blocked validation or follow-up.
