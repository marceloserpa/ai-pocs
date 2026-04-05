---
name: coverage
description: Run test coverage with JaCoCo and show results. Use when asked about code coverage, test coverage, or coverage reports.
allowed-tools: Bash
---

Run JaCoCo test coverage for this Gradle project and report the results.

## Steps

1. Run: `./gradlew clean test jacocoTestReport`
2. Run `python3 .claude/skills/coverage/scripts/coverage_report.py` and capture the output
3. Present the coverage table from the script output using this exact box-drawing format:

  ┌─────────────┬─────────┬────────┬───────┬──────────┐
  │    Type     │ Covered │ Missed │ Total │ Coverage │
  ├─────────────┼─────────┼────────┼───────┼──────────┤
  │ INSTRUCTION │ 60      │ 824    │ 884   │ 6.8%     │
  ├─────────────┼─────────┼────────┼───────┼──────────┤
  │ BRANCH      │ 0       │ 16     │ 16    │ 0.0%     │
  ├─────────────┼─────────┼────────┼───────┼──────────┤
  │ LINE        │ 17      │ 191    │ 208   │ 8.2%     │
  ├─────────────┼─────────┼────────┼───────┼──────────┤
  │ COMPLEXITY  │ 11      │ 107    │ 118   │ 9.3%     │
  ├─────────────┼─────────┼────────┼───────┼──────────┤
  │ METHOD      │ 11      │ 99     │ 110   │ 10.0%    │
  ├─────────────┼─────────┼────────┼───────┼──────────┤
  │ CLASS       │ 2       │ 16     │ 18    │ 11.1%    │
  └─────────────┴─────────┴────────┴───────┴──────────┘
4. If JaCoCo is not configured, tell the user how to add it to build.gradle
