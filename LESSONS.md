# Delivery lessons

Causes that keep sending autonomous deliveries back for repair, collected across projects, with the change to a skill (or repo tooling) that should stop each one earlier. The raw per-finding record is the ledger at `~/.agents/delivery-ledger.jsonl` (`autonomous-delivery/scripts/ledger.py report`); this file is the readable layer on top of it, where patterns get named and turned into skill edits.

How to use it:
- After a delivery, add evidence to the matching cause (or a new cause once `ledger.py report` flags it as recurring) and refine its proposal.
- When a proposal is clearly general (seen in more than one project or stack), make the skill edit, then mark the entry **Adopted** with the skill and date. Leave adopted entries here so a recurrence after adoption is visible.

## check-then-act-race
Something that was true when an async operation started is acted on after it stopped being true.
- furbo-papa live-stream-lock: an eviction landing between slot grant and segmenter start restarted the evicted channel; a revoke during HLS startup made a poll answer 502 once.
- furbo-papa android-account-logout: a token refresh in flight during logout saved its tokens afterwards and signed the user back in; the HTTP client's bearer cache was refilled with the old user's token.

**Proposal (`model`):** for every state that several components react to (session, slot, lease), the sketch names the one owner of its transitions and says what happens to operations already in flight when it changes (dropped, superseded by a generation check, awaited). **Status:** proposed.

## domain-outcome-rederived
A consumer recomputes an outcome the owning module already knows, and drifts from it.
- grandpa-shop swap-filled-pockets: the UI re-derived the displaced copy instead of the move returning it (×2).
- open-parks site-polish: freshness recomputed in two places.
- furbo-papa android-account-logout: the cast view model worked out "the session ended" from raw states instead of the session module exposing it.

**Proposal (`model`):** the sketch's public API returns or emits every outcome a caller needs (the displaced item, the transition that happened), so no caller reconstructs it from state. **Status:** proposed.

## untested-guard
A condition in new code that no test fails without.
- Seen in grandpa-shop (×3), furbo-papa cast-movie-seek, live-stream-lock and android-account-logout, running-calculator, open-parks.
- android-account-logout: the "don't end the cast on a startup logout" guard was only tested via Loading→LoggedOut, never a first emission of LoggedOut.

**Proposal (`tests`):** for every new guard, write the case where it must *not* fire, reached through the real starting conditions (first emission, empty input, boundary value), not just the convenient path. **Status:** proposed.

## duplicated-test-fixture
The same fixture or helper copied across test files, then drifting.
- grandpa-shop (×3), running-calculator, furbo-papa live-stream-lock, furbo-papa android-account-logout (unsigned-JWT helper copied three times).

**Proposal (`tests`):** before writing a helper, look for the module's shared test-support file and add it there; a second copy is the signal to extract. **Status:** proposed.

## hollow-test
A test that cannot fail, or asserts a proxy for the behaviour.
- grandpa-shop (×2), running-calculator, furbo-papa live-stream-lock.

**Proposal (`tests`):** before committing a test, break the behaviour it names and watch it fail; assert the observable outcome, not a class name or absence. **Status:** proposed.

## ime-composition-unhandled
Text inputs that intercept keystrokes break under IME composition.
- running-calculator tap-and-paste-over-box (×2), two-linked-boxes.

**Proposal (`model`):** any design that intercepts `beforeinput`/key events on a text field states how it behaves during composition (`isComposing`) and includes a composition scenario in the agreement's checks. Web-specific; generalize only if it shows up outside this project. **Status:** proposed.
