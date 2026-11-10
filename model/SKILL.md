---
name: model
description: Turn an agreed plan into a high-level design the user can review: diagrams, domain model, public API shapes, and key decisions. Second link of the chain.
---

Input is `.work/<task-slug>/agreement.md` (or the GitHub issue it links to). Turn it into a design the user can review and agree on before any code is written. Write no logic.

Never mention steps, handoffs, skills, or what happens "next". To the user this is the same continuous conversation.

**Prepare quietly.** Read the code the agreement touches: its current shape, module boundaries, and the library versions the project pins. Facts are your job; do not ask the user for what you can look up.

**Draft the design.** Keep it at the level a reviewer agrees on, not the level an implementer types:
- **Diagram.** One or two Mermaid diagrams (or a short textual equivalent): components and how data flows between them, plus a state diagram if anything moves between states.
- **Domain model.** Entities, their relationships, the states they move through, and what must never be allowed.
- **Public API shapes.** Types and signatures at module boundaries only, with the caller's usage shown first. No private helpers, no bodies.
- **Key decisions.** Each architectural choice (structure, where it lives, what it replaces) with a one-line why. When the change crosses a module boundary, name the alternative you rejected and why. If the current shape is already clear and local, keep it boring and say so.
- **Removes.** Code or paths this design makes obsolete, at module level.
- **Order.** Only if it matters: a coarse ordering of 2 to 5 milestones. No per-commit plan.

**Review it together.** Present the design in the conversation. Ask the user to push back, and point out the one or two decisions you are least sure of. When they challenge something, answer with your reason or change the design; do not just give way. Repeat until they say they agree.

**Record it.** Once they agree, write `.work/<task-slug>/sketch.md` with: diagram, domain model, public API shapes, key decisions with why, removes, and order if any. If `agreement.md` links a GitHub issue, post the sketch to it as a comment with `gh issue comment <issue-url> --body-file .work/<task-slug>/sketch.md` and add the comment URL to the top of the sketch. Never edit the issue description. If there is no issue, keep the local files only. Keep `.work/` out of commits.

Stop there. Building happens in a separate session from the issue, so write no code, change no files outside `.work/`, and do not start building. End by giving the user the sketch path and the comment URL.
