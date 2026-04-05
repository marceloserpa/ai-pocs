---
name: coverage
description: Run test coverage with JaCoCo and show results. Use when asked about code coverage, test coverage, or coverage reports.
allowed-tools: Bash
---

Run JaCoCo test coverage for this Gradle project and report the results.

## Steps

1. Run: `./gradlew test jacocoTestReport`
2. Read the summary from `build/reports/jacoco/test/html/index.html`
3. Report line coverage %, branch coverage %, and the path to the full HTML report
4. If JaCoCo is not configured, tell the user how to add it to build.gradle
