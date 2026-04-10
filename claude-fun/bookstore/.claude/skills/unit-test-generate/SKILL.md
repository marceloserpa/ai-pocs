---
name: unit-test-generate
description: Generate unit tests by analysing JaCoCo coverage gaps. Use when asked to generate, write, or improve unit tests.
allowed-tools: Bash, Read, Write, Edit, Glob
---

Generate unit tests for this Spring Boot project by first identifying coverage gaps, then writing tests to fill them.

## Steps


### 1. Capture the current coverage status

Invoke the `coverage` skill to run the overall coverage pipeline and get the overview report.

### 2. Collect coverage gaps

Invoke the `coverage-detailed` skill to run the full coverage pipeline and get the per-method gap report. Capture its JSON output.

Parse the JSON output. Focus on methods where `missingBranches > 0` first, then methods with the highest `missingInstructions`. Skip plain getters/setters (methods starting with `get`/`set` that have `missingBranches == 0` and `missingInstructions <= 4`).

### 3. Read the source files

For each class that appears in the gap report, read the corresponding source file under `src/main/java/`. Understand:
- What the method does
- What branches exist (if/else, Optional, throws)
- What dependencies are injected (for mocking)

Also read any existing test file for that class under `src/test/java/` to match style and avoid duplicates.

### 4. Conventions to follow

Match the project's existing test style exactly:
- `@ExtendWith(MockitoExtension.class)` for unit tests
- `@Mock` for dependencies, `@InjectMocks` for the class under test
- AssertJ assertions (`assertThat`, `assertThatThrownBy`)
- Test method naming: `methodName_expectedBehavior_whenCondition`
- One `@Test` per logical branch or scenario
- No Spring context (`@SpringBootTest`) — pure unit tests only
- Package mirrors `src/main/java/` structure

### 5. What to test

Create test to cover but not limited by the following scenarios:

- happy path
- null input
- invalid input
- dependency failure
- exception propagation
- boundary cases
- empty collections
- duplicate data scenarios

### 6. Follow best practices

- mak eeach test orthogonal
- dont make unnecessary assertions
- mock all external services
- keep tests short, simple and fast
- follow AAA pattern

### 7. Write the tests

For each gap:
- If a test file already exists for that class: add new `@Test` methods to it using the Edit tool
- If no test file exists: create it under `src/test/java/` using the Write tool

Cover every missing branch: happy path, not-found / empty Optional, validation failures, and exception paths.

### 8. Verify

Run `./gradlew test` and confirm all new tests pass. If any fail, read the error, fix the test, and re-run.

### 9. Report

Invoke the `coverage` skill to run the overall coverage pipeline and get the overview report. Compare this result 
with the previous. Show in a table, the before and after comparison.

After the table show a summary of what was generated:
- Files created or modified
- Number of tests added per class
- Any gaps that could not be covered with pure unit tests (e.g. require DB or HTTP layer) and why



