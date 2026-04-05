#!/usr/bin/env python3
import xml.etree.ElementTree as ET
import sys

REPORT_PATH = "build/reports/jacoco/test/jacocoTestReport.xml"


def parse_coverage(path):
    tree = ET.parse(path)
    root = tree.getroot()  # <report>

    counters = {}
    for counter in root.findall("counter"):
        ctype = counter.get("type")
        missed = int(counter.get("missed"))
        covered = int(counter.get("covered"))
        total = missed + covered
        pct = (covered / total * 100) if total > 0 else 0
        counters[ctype] = {"missed": missed, "covered": covered, "total": total, "pct": pct}

    return counters


def main():
    path = sys.argv[1] if len(sys.argv) > 1 else REPORT_PATH
    try:
        counters = parse_coverage(path)
    except FileNotFoundError:
        print(f"Error: report not found at '{path}'")
        sys.exit(1)

    print(f"{'Type':<14} {'Covered':>8} {'Missed':>8} {'Total':>8} {'Coverage':>10}")
    print("-" * 52)
    for ctype in ("INSTRUCTION", "BRANCH", "LINE", "COMPLEXITY", "METHOD", "CLASS"):
        if ctype not in counters:
            continue
        c = counters[ctype]
        print(f"{ctype:<14} {c['covered']:>8} {c['missed']:>8} {c['total']:>8} {c['pct']:>9.1f}%")


if __name__ == "__main__":
    main()
