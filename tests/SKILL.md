---
name: tests
description: Write unit tests and any other automated tests by the xUnit patterns. Use whenever writing or changing a test.
---

Every test, unit or otherwise, follows the xUnit patterns (Meszaros, *xUnit Test Patterns*). A test is read when it fails, by someone who did not write it. Write it for that person.

- **Name.** State the scenario and the expected outcome: `returns_empty_list_when_no_orders`, not `test1` or `testOrders`.
- **Shape.** Arrange, act, assert, in that order, separated by a blank line. One act per test.
- **Scope.** One logical concept per test, and one assert where practical. Several asserts only when they check that one outcome.
- **Behaviour, not implementation.** Test through the public API what a user of the code can observe. Never reach into private state or assert on how the code does it.
- **No logic.** No loops, conditionals, or computed expected values. Write expected values literally.
- **Independence.** Each test stands alone: a fresh fixture per test, no shared mutable state, no dependence on order, and no real clock, network, filesystem, or randomness unless that is what is under test. Use test doubles instead.
- **Failure messages.** A failure says what went wrong without a debugger: use the framework's most specific assertion and a message naming the expectation.

Follow the project's existing test framework, layout, and naming where it has them. Where they conflict with the rules above, match the project and say so.
