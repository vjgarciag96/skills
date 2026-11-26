# Delivery lessons

What keeps sending autonomous deliveries back for repair, across projects, grouped by the kind of mistake, with the skill or tooling change that should stop each one earlier. Rebuilt by the `lessons` skill from the run files in `runs/` and the ledger (`autonomous-delivery/scripts/ledger.py report`); deliveries never edit it.

Last fold: 2026-11-26, covering the ledger from 2026-11-22 (203 findings across four projects). This first fold was carried over from the old `LESSONS.md`, so there is no trend yet.

| Area | Findings | Tasks | Projects | Mostly found by |
|---|---|---|---|---|
| [Tests that don't protect](#tests-that-dont-protect) | 71 | 31 | 4 | code-quality |
| [Knowledge in the wrong place, or twice](#knowledge-in-the-wrong-place-or-twice) | 31 | 22 | 3 | code-quality |
| [Untrusted and degraded input](#untrusted-and-degraded-input) | 24 | 12 | 2 | adversarial review |
| [Timing and stale state](#timing-and-stale-state) | 23 | 15 | 2 | adversarial review |
| [Gaps in the agreement](#gaps-in-the-agreement) | 17 | 9 | 4 | adversarial review, review |
| [Shapes that mislead](#shapes-that-mislead) | 16 | 12 | 3 | code-quality |
| [UI conditions not checked](#ui-conditions-not-checked) | 16 | 12 | 3 | adversarial review, review |
| [Environment drift](#environment-drift) | 5 | 3 | 2 | CI |

Proposals marked **ready** have a cause seen in two or more projects.

## Tests that don't protect
Tests that pass with the behaviour broken, miss the case where a guard must not fire, or are copied until they drift. The largest area by far, in every project, and almost all of it found by code-quality after the tests were written. The `tests` proposals for untested-guard and hollow-test would cover most of it.

Tags: untested-guard, hollow-test, duplicated-test-fixture, one-valued-fixture, test-gap, untested-tie-break, untested-wiring, untested-branch-order, untested-degenerate-join, fixture-order-luck, weak-fixture, weak-assertion, null-equality-assertion, absence-without-presence, missing-output-assertion, intermediate-state-assertion, arrange-only-scenario, stub-fakes-the-answer, host-measured-text-assertion, test-coupled-to-storage-shape, test-concepts-bundled, misleading-test-name, mystery-guest, copied-formula.

### untested-guard
A condition in new code that no test fails without.
- Seen in grandpa-shop (×3), furbo-papa cast-movie-seek, live-stream-lock and android-account-logout, running-calculator, open-parks.
- running-calculator desktop-columns: a CSS `min-height` media guard that stops a sticky column being cut off on short windows had no test; removing it passed the suite.
- android-account-logout: the "don't end the cast on a startup logout" guard was only tested via Loading→LoggedOut, never a first emission of LoggedOut.
- grandpa-shop cardmarket-price: the key validator refused comma, tab and quote but not a line break; the web abort and stale-answer guards survived four mutants; a zero trend, a padded set code and a non-IOException at start had no pinning test until a tidy pass.
- grandpa-shop binder-shelf: padded names were also duplicates, fractional page counts were also below the minimum, and invalid capacities also had the wrong number of slots. Those fixtures still passed with their intended guards removed.

**Proposal (`tests`):** for every new guard (media-query conditions included), write the case where it must *not* fire, reached through the real starting conditions (first emission, empty input, boundary value), not just the convenient path. For the rejection case, choose input that violates only the targeted guard, so another guard cannot make the test pass. **Status:** proposed, **ready**.

### hollow-test
A test that cannot fail, or asserts a proxy for the behaviour.
- grandpa-shop (×2), running-calculator, furbo-papa live-stream-lock.
- running-calculator redesign-world-records: "records stay with an empty/invalid goal" tests never changed the distance, so leftover text from the last valid render satisfied them; a paceFor test compared paceFor with calculate(), which returns paceFor. A first attempt at the 320 px overflow test also passed against the bug (page width stayed 320 while the picker overflowed into the margin) until it was run against the unfixed CSS.
- running-calculator desktop-columns: Playwright's `isVisible()` was used as an "in view" check; it ignores the viewport, so it passed with the element 815 px above the window.
- grandpa-shop binder-shelf: a legacy-compatible read passed even when migration made no write, and a catalogue class assertion passed when the catalogue rendered physically below the desktop spread.
- furbo-papa epg (#111), seven forms across nine slices:
  - `assertEquals(key(a), key(b))` passed with both keys null;
  - "sheet closes after refresh" never checked the sheet had opened;
  - "re-listed after clear" did set and clear before the first read;
  - a retry test asserted Loading but not a second fetch;
  - local-time expectations reused the screen's own `toLocaleString`;
  - a fixture used the same value for id and display name, so swapping them passed;
  - a dedup test picked the right channel only because the winner was read last.

**Proposal (`tests`):** before committing a test, break the behaviour it names and watch it fail; assert the observable outcome, not a class name or absence. A test that something "stays" or "still shows" must first change the input it depends on, so stale output cannot pass it; an expected value must not come from the function under test or a caller of it. Check visibility and spatial relationships with bounding boxes, and verify a migration at the target storage boundary if the current loader still accepts the source format. Asserting absence first asserts presence; a test of "follows changes" reads between each change; an equality between two computed values also pins one literal; fixtures give every field a distinct value and put the expected winner somewhere other than first or last. **Status:** proposed, **ready**.

### duplicated-test-fixture
The same fixture or helper copied across test files, then drifting.
- grandpa-shop (×3), running-calculator, furbo-papa live-stream-lock, furbo-papa android-account-logout (unsigned-JWT helper copied three times).
- grandpa-shop remove-copy-by-drag: the layout stub's new spread box repeated the pocket grid's literals instead of sharing them, and a local release helper sat outside the shared drag helpers.
- running-calculator redesign-world-records: each world record was written four times (data, unit test, EN e2e rows, ES e2e rows that differed only in three labels).
- furbo-papa ui-tests-screenshots: the phone and TV screenshot tests each built the same catalog fixture, even though both flavours could see a shared `src/test` source set.
- grandpa-shop cardmarket-price: three route tests hand-built the same product rows while a shared `row(...)` helper already existed in the module's test support.

**Proposal (`tests`):** before writing a helper, look for the module's shared test-support file and add it there; a second copy is the signal to extract. A fake that models geometry or state derives every value from one set of constants, so two fakes of the same layout cannot disagree. Expected values that differ per locale or variant are derived from one table by swapping only what differs (labels), not written out again per variant. When the same scenario is rendered per form factor or flavour (phone/TV, light/dark), its state fixture goes in the source set every variant shares. **Status:** proposed, **ready**.

### one-valued-fixture
A fixture with one element or one value can't tell the rule under test apart from a constant, so a mutant that hard-codes that value survives.
- furbo-papa epg-115b: `live` was only ever read back as true.
- grandpa-shop shelf-view: open and replace were tested on a one-binder shelf at index 0, so `index === 0` mutants passed until the fixture gained a second binder acted on at index 1.

**Proposal (`tests`):** when a rule selects or updates one element by index, key or flag, the fixture has at least two candidates. The test acts on one that isn't first or default and asserts that the others are unchanged. **Status:** proposed, **ready**.

## Knowledge in the wrong place, or twice
A rule, outcome or piece of markup written in a second place, or owned by a module other than the one that knows it, so the copies drift. Found mostly by code-quality. The `model` proposal for domain-outcome-rederived and the `implement` proposal for duplication would cover most of it.

Tags: domain-outcome-rederived, duplication, duplicated-markup, duplicated-rule, duplicated-work, copy-paste-across-flavors, copy-paste-helper, model-outside-model-layer, two-sources-of-truth, parallel-name-tables, layout-knowledge-across-modules, storage-policy-leaks-into-view, state-transition-in-jsx, accessor-bypassed, duplicate-layout-subscription, focus-ownership-split, per-activity-session-graph, docs-vocabulary-drift.

### domain-outcome-rederived
A consumer recomputes an outcome the owning module already knows, and drifts from it.
- grandpa-shop swap-filled-pockets: the UI re-derived the displaced copy instead of the move returning it (×2).
- open-parks site-polish: freshness recomputed in two places.
- furbo-papa android-account-logout: the cast view model worked out "the session ended" from raw states instead of the session module exposing it.
- grandpa-shop rarity-filter: the filter component read `selected.size > 0` to decide "a filter is on", re-stating the empty-means-no-filter rule the pure module applied in `keepRarities`.

**Proposal (`model`):** the sketch's public API returns or emits every outcome a caller needs (the displaced item, the transition that happened, a predicate such as "is a filter on"), and exposes a selection or state type only alongside the predicates callers branch on, so no caller reconstructs it from state or reads its representation. **Status:** proposed, **ready**.

### duplication
New code copies an existing helper, rule or layout instead of sharing it, and the copies drift (seven findings in furbo-papa #111).
- The live check lived in SQL and a filter.
- An EPG ranking comparator was copied and lost its id tiebreak.
- The "unavailable sources" notice was written twice with different wording.
- A keep-at-top scroll guard and its tests were copied between two screens.
- A catch-all-null block appeared in a fourth API client.
- A row layout was copied.
- Programme repository fakes were copied.
- open-parks site-polish (as duplicated-markup): the Telegram button and the midnight clock formatting were each written twice.
- Related: `copy-paste-across-flavors` and `duplicated-test-fixture`.

**Proposal (`implement`):** before writing a rule, helper or composable, grep for an existing one with the same job. A second copy is the signal to extract the shared version in the same commit, never later. **Status:** proposed.

### copy-paste-across-flavors
A second form factor or flavour (TV next to phone) gets its own copy of a piece of UI or logic the first already has, and the copies drift.
- furbo-papa tv-parity (PR #223): the TV drawer's section enum, `isIn` check and top-level navigate block were copied from the phone's bottom bar instead of shared from the `main` source set both flavours see.
- furbo-papa tv-parity (PR #225): the TV movie card redrew the phone's poster plate line for line; only the colour helper had been made public.
- Related: `duplicated-test-fixture` (the same pattern in test fixtures, furbo-papa ui-tests-screenshots).

**Proposal (`implement`):** when building a variant of an existing screen for another form factor, first list what the existing screen draws or decides that isn't form-factor specific (card faces, palettes, navigation rules, state mapping) and extract that into the shared module or source set as a composable or function both call. Only the focus, input and layout wrapper is written per variant. Widening a helper's visibility for one value is the signal that the drawing around it should move too. **Status:** proposed.

## Untrusted and degraded input
Input from outside is bounded in total but not in the dimension that costs, a partial or empty snapshot replaces good data, or a boundary lets failures other than the promised one escape. Concentrated in furbo-papa's EPG feeds and grandpa-shop's storage and price data, and found mostly by adversarial review. The `model` proposal for unbounded-untrusted-input and the `frame` proposal for destructive-on-degraded-input would cover most of it.

Tags: unbounded-untrusted-input, unbounded-hostile-input, regex-backtracking, destructive-on-degraded-input, destructive-drop-without-cancel-guard, any-overlap-arms-destructive-drop, io-contract-not-enforced, unvalidated-wire-body, error-masking, error-handling-scope, partial-input-tolerance, over-strict-guard, data-assumption-gap, migration-duplicates-persisted-data, migration-depends-on-mutable-default, h2-postgres-divergence.

### unbounded-untrusted-input
Input from outside (a public feed, a server field, a user name) is bounded in total but not in one of the dimensions that actually costs memory or CPU.
- furbo-papa epg-115a (five findings across two rounds):
  - a 250 KB gzip with one huge attribute, millions of channel ids, a UTF-16 attribute, or millions of nested tags each exhausted the JVM heap under a 256 MB byte cap;
  - kept programme text had no total budget.
- furbo-papa epg-117b: title regexes with an unanchored `\s+` went quadratic on titles padded with long runs of spaces, at about 8 s per request.
- furbo-papa epg-119b: a far-future `end` from the server overflowed `Duration.toMillis()` and would crash the app.

**Proposal (`model`):** for every untrusted input, the sketch lists each dimension it can grow in, and a cap for each:
- total bytes;
- size of one token, attribute or string;
- count of each kind of element;
- nesting depth;
- total kept;
- numeric range of times and durations;
- the encoding the caps assume.

Each regex over untrusted text runs in linear time: anchor whitespace runs, or use possessive quantifiers. **Status:** proposed.

### destructive-on-degraded-input
A run with an incomplete snapshot (an empty feed, a channels-only file, or stale state from another tab) replaces good stored state.
- furbo-papa epg-115a: a feed listing channels but no programmes replaced a source's stored week with zero rows; the first fix then failed legit sources whose mapped channel was simply off air.
- furbo-papa epg-117d: the same empty feed wiped the event counts whenever nothing on that source was mapped.
- grandpa-shop binder-shelf: a tab that only changed which binder was open saved its stale shelf and erased a binder added in another tab.

**Proposal (`frame`):** for every replace-all write, the agreement says which degraded inputs count as failures that keep the old state. It covers an empty input, a header-only input, and a large drop from the stored size. Each gets a done-when line, plus one for the legitimate small input that must still go through. For a shared store, specify which actions can rewrite collection contents and prove that navigation from an older snapshot preserves newer content. **Status:** proposed, **ready**.

### io-contract-not-enforced
A boundary promises one failure type (for example IOException) but the parsing behind it throws others, and the caller that relies on the promise crashes.
- grandpa-shop cardmarket-price: `PriceGuides.keep` documented IOException but let JSON, date and overflow errors escape; the first repair wrapped some of them, and the adversarial review of the next slice found `main` still crashing at start on the rest (×2 in one task, the second after a repair).

**Proposal (`tests`):** when a boundary names the exceptions it throws, write one test per kind of bad input it reads (malformed syntax, bad value, out of range) and assert the documented type, and one test on the caller that the promised type is the only one it needs to catch. A repair of such a finding lists every parse step behind the boundary before fixing one. **Status:** proposed.

## Timing and stale state
Something true when an async operation started is acted on after it stopped being true: a refresh racing a first load, a stale answer winning, a wait with no bound. Found almost only by adversarial review, so the tests written during implementation don't reach it. The `model` proposal for check-then-act-race and the `tests` proposal for query-invalidation-race would cover most of it.

Tags: check-then-act-race, query-invalidation-race, async-state-race, stale-drop-target-after-turn, stale-ui-state, stale-swallowed-key-state, retry-same-key-noop, poll-not-keyed-to-input, remote-state-not-tied-to-load, late-content-insert, cancelled-before-respond, shared-mutation-state-across-rows, unbounded-network-wait, body-not-cancelled-on-parse-failure, unstable-identity, server-data-as-ui-key, identity-key-mismatch.

### check-then-act-race
Something that was true when an async operation started is acted on after it stopped being true.
- furbo-papa live-stream-lock: an eviction landing between slot grant and segmenter start restarted the evicted channel; a revoke during HLS startup made a poll answer 502 once.
- furbo-papa android-account-logout: a token refresh in flight during logout saved its tokens afterwards and signed the user back in; the HTTP client's bearer cache was refilled with the old user's token.

**Proposal (`model`):** for every state that several components react to (session, slot, lease), the sketch names the one owner of its transitions and says what happens to operations already in flight when it changes (dropped, superseded by a generation check, awaited). **Status:** proposed.

### query-invalidation-race
Async state in a UI is refreshed in a way that lets a stale in-flight answer win.
- furbo-papa epg-116b: TanStack Query does not restart a first load that is still running when it is invalidated, so a mapping cleared during the first 30 s suggestions load never got its suggestion back. The same bug sat unnoticed in #117d's list.
- furbo-papa epg-114c: a retry with the same key was a no-op.
- furbo-papa epg-119a: a late Live row was inserted above the visible area.
- furbo-papa epg-119b: a refresh had to cancel an earlier collection and its timers.

**Proposal (`tests`):** every refresh or invalidation path gets a test where the earlier request is held open across the change and released after it. The test asserts that the newer state wins and that a fresh read happened. **Status:** proposed.

## Gaps in the agreement
A rule in the agreement covers the typical case and says nothing about the edge: one candidate, a tie, a time on another day, two sources that disagree. No single tag recurs, but together they appear in every project. open-parks site-polish alone logged three (an alert window on another day shown as today's, a closure outlasting the schedule, a time without its date). Framing would cover most of it by asking, for every rule, what happens at its edges and when its sources conflict.

Tags: spec-gap-degenerate-rule, spec-gap-absent-value, spec-gap-equivalent-input, spec-gap-eviction-persistence, spec-gap-headerless-identity, spec-gap-regional-variants, spec-gap-time-without-date, spec-gap-variant-conflation, spec-gap-visual-boundary, spec-gap-window-day, spec-gap-window-past-schedule, agreement-scope-mismatch, guideline-scope-widened, cross-source-precedence, tie-break-on-equal-key.

### spec-gap-degenerate-input
A rule in the agreement is written for the typical case and says nothing about the degenerate one (one element, equal keys, size one), so the implementation picks arbitrarily and the reviewer finds it.
- grandpa-shop cardmarket-price: one-name sets joined to whichever one-product expansion was oldest; equal trends paired by product id; the minimum-names rule was then written for ties only, leaving untied one-name sets joined (×3 across two rounds).

**Proposal (`frame`):** for every matching, ranking or pairing rule, the agreement states what happens with one candidate, with equal keys, and below a minimum size, as explicit done-when lines, before the sketch is written. **Status:** proposed.

## Shapes that mislead
An interface whose shape says something untrue: a type that allows an impossible case, an API nobody needs, a name from an older role, a query that mutates. All found by code-quality. The `model` proposal for hidden-type-switch and the `implement` proposals for speculative-api and stale-module-name would cover most of it.

Tags: hidden-type-switch, speculative-api, stale-module-name, coupled-params-split, dense-code, comment-describes-future-state, name-collision, fat-interface-dependency, mutator-used-as-query, hidden-side-effect-in-query, leaky-callback.

### hidden-type-switch
An invariant that should be in a type lives in a comment or a runtime check, so callers carry dead branches for impossible cases.
- Seen in 3 tasks so far (ledger).
- grandpa-shop remove-copy-by-drag: the drop target type allowed "a printing dropped off the binder"; only a comment said it could not happen, and the app kept a nested branch that silently ignored it.

**Proposal (`model`):** when the sketch adds a variant that only some inputs can produce, the public shape pairs input and outcome in one union (for example origin with target), so the impossible pair cannot be written. **Status:** proposed, **ready**.

### speculative-api
An interface shape with no second use: added before it's needed, or left behind after its other variants were deleted.
- furbo-papa epg-114a: `EpgChannelLists.channels` was added before anything needed it, and the only caller went around it.
- grandpa-shop shelf-view: deleting the shelf dialog left `DeskDialog` as a one-member union carried through state, a callback and a prop.

**Proposal (`implement`):** after deleting a variant, a caller or a feature, re-read every union, parameter and callback it touched. Collapse any that now take only one value into a boolean or a plain call. **Status:** proposed, **ready**.

### stale-module-name
A name kept after the thing it names changed role, so it now describes an older or narrower use.
- grandpa-shop precise-drag-drop: `pocketHitTest` no longer did hit-testing.
- grandpa-shop shelf-view: once the shelf became its own view, `reopenWorkspace`, `text.binder.title` and the `desk__*` header classes were serving it too, and a `last` flag inside a map read as "last item".

**Proposal (`implement`):** when a change widens where a function, string key or CSS block is used, rename it to fit its new scope in the same change. For an app-wide piece, that means an app-level namespace rather than the namespace of the screen it was born in. **Status:** proposed.

## UI conditions not checked
The UI works at the size, theme and input it was built at, and breaks at another: a narrow or landscape screen, a dark theme, keyboard focus, a screen reader, key repeat, IME composition. No cause recurs on its own yet, and no proposal covers the area as a whole. A candidate for `frame`: the agreement lists the viewports, themes and input methods each change must hold at.

Tags: narrow-viewport-unchecked, fixed-height-layout-not-checked-in-landscape, fixed-width-text, inherited-responsive-rule, partial-theme-mapping, occlusion-not-modelled, focus-target-off-screen, focus-restorer-no-fallback, live-region-hidden-when-empty, a11y-label-moved-outside-focusable, a11y-value-regression, key-repeat-unhandled, back-modelled-as-key-but-routed-via-dispatcher, ime-composition-unhandled.

### ime-composition-unhandled
Text inputs that intercept keystrokes break under IME composition.
- running-calculator tap-and-paste-over-box (×2), two-linked-boxes.

**Proposal (`model`):** any design that intercepts `beforeinput`/key events on a text field states how it behaves during composition (`isComposing`) and includes a composition scenario in the agreement's checks. Web-specific; generalize only if it shows up outside this project. **Status:** proposed.

## Environment drift
CI's device or resources differ from the local run, or the base branch moved under a delivery. Small, and found by CI. No proposal yet.

Tags: ci-device-differs-from-local, ci-runner-resources-unchecked, base-moved-under-branch, base-moved-reopened-agreement.

## Adopted
None yet.
