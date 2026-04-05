#!/usr/bin/env python3
import xml.etree.ElementTree as ET
import json
import sys

REPORT_PATH = "build/reports/jacoco/test/jacocoTestReport.xml"


def parse_coverage(path):
    tree = ET.parse(path)
    root = tree.getroot()  # <report>

    problems = []

    for pkg in root.findall("package"):
        pkg_name = pkg.get("name", "").replace("/", ".")
        for cls in pkg.findall("class"):
            cls_name = cls.get("name", "").replace("/", ".")
            for method in cls.findall("method"):
                method_name = method.get("name", "")
                line = method.get("line", "?")

                if method_name in ("<init>", "<clinit>") or method_name.startswith("lambda$"):
                    continue

                branch_counter = method.find("counter[@type='BRANCH']")
                instr_counter = method.find("counter[@type='INSTRUCTION']")

                missing_branches = int(branch_counter.get("missed", 0)) if branch_counter is not None else 0
                missing_instrs = int(instr_counter.get("missed", 0)) if instr_counter is not None else 0

                if missing_instrs > 0 or missing_branches > 0:
                    problems.append({
                        "class": cls_name,
                        "method": method_name,
                        "missingBranches": missing_branches,
                        "missingInstructions": missing_instrs,
                        "lineRange": line,
                    })

    problems.sort(key=lambda x: x["missingInstructions"], reverse=True)
    return problems


def main():
    path = sys.argv[1] if len(sys.argv) > 1 else REPORT_PATH
    try:
        problems = parse_coverage(path)
    except FileNotFoundError:
        print(f"Error: report not found at '{path}'")
        sys.exit(1)

    print(json.dumps(problems, indent=2))


if __name__ == "__main__":
    main()
