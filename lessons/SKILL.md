---
name: lessons
description: Fold new delivery run files into the lessons summary, clustering causes into problem areas with their trend and proposals. Use when the user asks to update, rebuild, review or summarise delivery lessons. Also holds the run-file format deliveries write.
---

Delivery lessons live in this folder, next to this file:

- `runs/<date>-<repo>-<task>.md`: one file per delivery, written once by its lead and never edited. Files directly in `runs/` are not yet in the summary.
- `runs/folded/<year>/`: run files already folded into the summary.
- `SUMMARY.md`: the readable layer, grouped by problem area. Only this skill rewrites it.

Every finding is also in the ledger as data (`autonomous-delivery/scripts/ledger.py`). Counts come from `ledger.py report`, not from counting run files.

## Run files

A delivery writes `runs/<YYYY-MM-DD>-<repo>-<task>.md`, with the repository's short name:

```markdown
# <repo> <task>, <YYYY-MM-DD>

PR: <url, or "not opened">. Repair rounds: <n>.

## <cause tag>
<What went wrong, as the reviewer or CI saw it.> <Why: the root cause, not the symptom.> <What would have caught it earlier, and where: frame, model, implement, tests, lint, CI or repo instructions.> Found by <source>.
```

One section per cause the run logged in the ledger, with the same tag. Findings that share a cause share a section. Plain prose a reader outside the project follows; names of code only where they make the point. A run with no repair findings writes the header and one line saying so, because quiet runs show which areas are improving.

## Fold runs into the summary

1. Read `SUMMARY.md`, every file directly in `runs/`, and `ledger.py report`.
2. Put each new section under its cause in `SUMMARY.md`. A cause belongs to one area. Areas are named for the kind of mistake, never for a project or stack. A new tag joins the area whose pattern it shares and is added to that area's tag list. Rare tags that share a root count together: three one-off `spec-gap-*` tags are a recurring area even though no single tag recurs.
3. Give a cause its own entry once it recurs (`ledger.py report` flags it) or once one example is instructive enough to name. Each entry has a one-line definition, at most three examples, a proposal and a status. Keep the most instructive and the most recent examples and drop the rest; the run files and the ledger keep them.
4. For each area, refresh its numbers from the ledger (findings, tasks, projects, main sources) and write two or three lines on the pattern and its trend since the last fold: growing, steady or quiet. Name the proposals that would cover most of it.
5. Refresh the table at the top and the date of this fold.
6. Move the folded run files to `runs/folded/<year>/`.

A proposal is the lint rule, check or skill line that would have stopped the cause earlier, with the skill named. Statuses are `proposed`, `adopted (<skill>, <date>)` and `dropped (<reason>)`. Change one only when the user decides. Mark a proposal **ready** when its cause appears in two or more projects. When an adopted cause recurs after its adoption date, flag it at the top of its area.

Merge, split or rename areas when the clusters have shifted, and say so in the return. Keep each area readable in one screen; tighten examples before adding more.

Never edit other skills from here. Return what changed: new causes and areas, trends, proposals now ready, and recurrences after adoption.
