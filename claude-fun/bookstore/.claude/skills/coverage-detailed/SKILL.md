---
name: coverage-detailed
description: Run test coverage with JaCoCo, collect all problems, format in a JSON format and show it. Use when asked about code coverage detailed coverage.
allowed-tools: Bash
---

Run JaCoCo test coverage for this Gradle project and report detailed per-method problems.

## Steps

1. Run: `./gradlew clean test jacocoTestReport`
2. Run: `python3 .claude/skills/coverage-detailed/scripts/coverage_report.py` and capture the output
3. Present the JSON output to the user as-is
4. If JaCoCo is not configured, tell the user how to add it to build.gradle
