---
name: slice
description: Split a task, initiative, project, or idea into thin vertical slices that each ship end to end and tell one easy story to a reviewer. Use whenever breaking work into implementable pieces, units, tickets, or PRs.
---

Split the work so each piece cuts through every layer it touches and leaves something working that a user or caller can see. Prefer vertical slices over horizontal ones whenever the work allows. Write no code.

Matt Pocock's skills call a piece like this a ticket. Here it is a slice.

**Vertical first.** A slice goes end to end: data source, logic, interface, and a test proving the whole path. The first slice is the thinnest one that works. Each later slice makes it fatter.

**Example.** A new phone screen shows data from an API.
- Wrong: one PR for the network call, one for the view model, one for the UI. Nothing works until the third PR lands, and no reviewer can check the first two against real behaviour.
- Right: slice 1 fetches one field from the API and shows it on a bare screen, with a test from response to rendered text. Slice 2 adds the rest of the fields. Slice 3 adds loading and error states. Slice 4 adds pull-to-refresh. Each slice runs on a device and fits in one sentence.

**Ordering.**
1. Start with the slice that proves the riskiest connection, usually the thin end-to-end path.
2. Then order by value: each slice should leave the product more useful than the last.
3. Edge cases, error handling, and polish come after the happy path works, as their own slices.
4. Each slice depends only on the slices before it, so the work can stop after any one and still be shippable.

**Each slice states:**
- a title that says what a user can now do or see,
- what it adds, in one or two sentences,
- how to check it works: the test or the manual step that proves it.

A reviewer should be able to read the title, run the check, and approve without having to look at another slice.

**When horizontal is right.** Some work has no user-visible path: a schema migration, a dependency upgrade, a pure refactor. Slice it into steps that each leave the build green, and say why it is not vertical.

**Anti-patterns:**
- **Layer by layer.** Backend PR, then API PR, then UI PR. Integration bugs surface last, and every review is about code that does nothing yet.
- **Big bang.** One slice that does everything. Too big to review, too risky to revert.
- **Scaffolding first.** Empty classes, interfaces, or files "to be filled in later". Ship them inside the first slice that uses them.
- **Dead flags and stubs.** A slice that only works behind a flag nobody turns on, or that returns fake data, unless the flag is the point of the rollout.
- **Polish before path.** Animations, theming, or edge cases before one real end-to-end path works.

Output the slices as an ordered `- [ ]` list. If there is a `.work/<task-slug>/` folder, put them under **Units** in `sketch.md`. Never mention steps or handoffs to the user.
