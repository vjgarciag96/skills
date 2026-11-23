---
name: guided-delivery
description: Frame and model a task together with the user in this conversation, then deliver it autonomously from implementation to an auto-merging PR. Use when the user wants to shape the agreement and design themselves and hand off the rest.
---

Run the first two stages with the user, then run the rest as the lead of `autonomous-delivery`. Opting into this skill authorizes the same delivery as `autonomous-delivery` (push a branch, open a PR, enable auto-merge) once the user approves the design, unless the repository instructions or the request limit it.

## With the user

Run these stages yourself in this conversation. Do not delegate them, and do not answer questions on the user's behalf.

1. **Frame.** Follow the `frame` skill with the user as the counterpart: prepare quietly, interrogate in rounds with your recommendations, push back, then summarise and confirm. Write `.work/<task-slug>/agreement.md` once the user confirms, and offer to post it as an issue as that skill says.
2. **Model.** Follow the `model` skill with the confirmed agreement as input and the user as reviewer. Write `.work/<task-slug>/sketch.md` once the user agrees, posting it to the issue if there is one. Ignore that skill's instruction to stop after the sketch.
3. **Hand off.** Tell the user in one or two lines that you are now building, reviewing, and delivering this autonomously, and that you will come back only for a product decision, a missing permission, or the merged PR. Their approval of the sketch is the go-ahead; do not ask again.

## Autonomously

Follow `autonomous-delivery` from its **Implement** step onward, with the accepted `agreement.md` and `sketch.md` as the approved artifacts: its dispatch rules, implement, gate, review and validation, triage, re-review, ledger (its `scripts/ledger.py`) and the shared `LESSONS.md` it keeps up to date, and delivery to a merged PR. When you hand back the merged PR, tell the user in a line or two which lessons entries this run added or changed.

The user stays the owner of the agreement and the sketch. When a change or a finding would reopen a decision in either, do not resolve it as lead: stop that work, bring the decision back to the user with your recommendation, update the artifact once they answer, and resume. Every other decision is the lead's, as in `autonomous-delivery`.
