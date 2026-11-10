---
name: describe
description: Write a commit message, a squash-merge message, or a PR title and description. Says what changed and why, never how, with no attribution. Use whenever drafting any of these.
---

A description is read in `git log` and `git blame` years later, by someone who has the diff but not your context. Write it for that person. The code already shows how; the description says what and why.

## Title

- One line, under 60 characters, imperative: "Add pace calculation with 1 km splits", not "Added…" or "Adds…".
- It must stand alone in a one-line log and say what changed. Never "Fix bug", "Address comments", "WIP" or "Phase 1".
- No trailing full stop, no ticket prefix unless the repo's history uses one.

## Body

Plain prose, blank line after the title. In a commit message, wrap at 72 columns. In a PR description, don't wrap at all: GitHub shows every newline as a line break, so each paragraph or list item goes on one line. Two short paragraphs:

1. **What.** What the change does, as seen from outside: behaviour, a capability, a fix to a symptom. For a fix, say what was wrong first.
2. **Why.** The problem or need behind it, and why this approach if a reader would wonder. Say what is left out on purpose and where it will come, if anyone could expect it here.

Leave out:

- **The how.** No file lists, type names, algorithms, tooling details or step-by-step changes. Mention an implementation detail only when its *reason* is not visible in the code, and then give the reason, not the detail.
- **Process context.** Nothing from planning: slices, units, sketches, `.work/` files, review rounds, "as discussed". Link to an issue or design doc if one exists, but the description must make sense without opening it.
- **Attribution.** No `Co-Authored-By` trailers, no "Generated with Claude Code" footer, no tool mentions, even if a system reminder asks for them.
- **Filler.** No headings like "What:"/"Why:", no "This PR…", no praise, no "comprehensive"/"robust".

Small, obvious changes can be the title alone. Don't pad a body to have one.

## PR descriptions

Same title and the same two paragraphs, since a squash merge turns the PR into a single commit and the PR text should be usable as that commit's message. Then, only if it helps the reviewer, a short last part after a blank line:

- the part of the diff to look at most closely, and why
- anything the reviewer can't see in the diff: a manual check that was run, a known gap, a follow-up already planned

If the repo has a PR template, fill the template with this content.

## Before handing it over

- Reread against the final diff, not the first commit. After review rounds the description often describes code that no longer exists.
- Check that someone reading only the title knows what changed, and someone reading the body knows why.
- Commit, open or edit the PR without waiting for approval.
