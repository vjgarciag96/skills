# open-parks site-polish, 2026-11-23

PR: https://github.com/vjgarciag96/open-parks/pull/128, later split into #129 to #137. Repair rounds: 1.

## spec-gap-window-day
The page showed an alert's closure window, due the next day, as today's hours, under the verdict and above the forecast. The agreement said to show the window but not which day it applies to, and the feed gives it as a date range plus hours. Framing would have caught it with a done-when line for a window on another date. Found by review.

## spec-gap-window-past-schedule
During an alert closure that outlasted the park's scheduled closing, the page said "Hasta medianoche", promising a reopening the schedule rules out. Two sources decide when the park reopens, the alert window and the seasonal schedule, and the agreement didn't say which wins where they overlap. Framing would have caught it by naming the winner at each overlap. Found by adversarial review.

## spec-gap-time-without-date
The last-checked time had no date when the last successful fetch was on an earlier day, so a stale check read as today's. The agreement specified the time but not what it shows when it isn't today. Framing would have caught it with a done-when line for a time from another day. Found by adversarial review.

## untested-guard
New boundaries had no test: a closure ending before midnight, hours like 24:30, minute 60, the instant a window ends, a one-day date range, and a closure with both a window and a reopening forecast. Tests covered the typical case of each rule and never its edges. Writing a test at each boundary value and just past it, while implementing, would have caught them. Found by code-quality.

## model-outside-model-layer
The alert-closure type was defined in the headline module but built in the status module, creating a cycle, and the page re-derived closure decisions from its bare variants. The sketch placed the type by where it was shown, not by who produces it. Modelling would have caught it by putting a domain type beside its only producer, with the queries its consumers need. Found by code-quality.

## domain-outcome-rederived
The page recomputed the data's freshness after it had already been built once, and the status read the incident window twice. Implementation passed raw inputs down instead of the outcome already computed. The existing `model` proposal covers it. Found by code-quality.

## duplicated-markup
The Telegram button markup and the midnight clock formatting were each written twice, and the spoken sentence for each forecast hour was assembled partly in the view and partly in the translations. The second Telegram placement and the second language were added by copying. The existing `implement` duplication proposal covers it. Found by code-quality.
