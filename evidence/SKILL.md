---
name: evidence
description: Show a change's effect as before-and-after evidence of each area it touches, embedded in the PR description. Use once review and code-quality have passed on a change people can see or get back: pages, copy, bot or API replies, HTTP behaviour, accessibility, telemetry events, logs.
---

Evidence lets a reviewer judge a change without running it. It shows only what the change touches, before and after, and says plainly what was not checked.

## When

Gather it once review, code-quality and every other check have passed, on the final reviewed head. If the head moves afterwards, redo the items the new commits touch.

It applies when the change alters something a person sees or gets back, or that someone reads to understand the system: a page's layout or copy, a bot's or API's replies, status codes and redirects, what a screen reader announces, a telemetry event's name or payload, a log line, a metric. A refactor, a test-only change or an internal change gets no evidence. Its description says "No visible change; covered by tests." instead.

## What

One item per changed area, taken from the agreement's scenarios and the diff. For each:

- **Before is the PR's base, after is its head.** Same scenario, instant, viewport, theme and language on both sides. If the head adds a fixture the base lacks, render both sides from the head's fixtures and say so.
- **A crop of the area, not the whole page.** The element's box plus a small margin, at 2× scale, with reduced motion so animations have settled. Add viewports or themes only where the change differs across them, such as a breakpoint or a dark-mode colour.
- **Text when it isn't visual.** Command output such as `curl -si`, bot replies, the accessibility tree of the area, measurements such as contrast ratios or tap-target sizes, the telemetry events emitted or the log lines written for the scenario, captured from the running code rather than copied from the source. Show it as a diff when short.
- **Expected and observed.** One line each. Where they differ, keep the item and add the difference to the gaps.

Then list what was not checked by hand and why (it needs a device, a production-only service, a real account), and any visible issue knowingly left in.

Capture with the project's own tooling: its preview or fixture renderer, its browser automation, its test fakes for external services. Keep capture scripts and throwaway fixtures out of the PR.

## Where

In the PR description, after the `describe` body, under one `## Evidence` heading.

- Host images in the repository, never on an outside service. Commit them to a separate branch, never the PR's own: the repository's existing screenshot branch if it has one, otherwise an orphan `evidence` branch. Put them under `pr-<number>/<head sha>/` and reference them as `https://github.com/<owner>/<repo>/blob/<branch>/<path>?raw=true`, which renders for anyone who can see the repository.
- One subsection per item: a heading naming the area and scenario, a two-column Before and After table of images or short text, then expected and observed.
- Put long text, such as accessibility trees or full replies, in `<details>` blocks. Keep the description under GitHub's 65,536-character limit; move overflow to files on the evidence branch and link them.
- End with the not-checked list and the head sha the evidence was gathered on.

After editing the description, request every image URL in it and confirm each returns 200.
