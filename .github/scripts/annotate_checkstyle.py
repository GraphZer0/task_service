#!/usr/bin/env python3
"""Turn a Checkstyle XML report into native GitHub Actions annotations.

Native workflow-command annotations (`::warning file=...`) are written
directly to the job log for the *current* check run, so they don't need
to create or update a separate check run via the REST API - unlike
third-party actions such as jwgmeligmeyling/checkstyle-github-action,
which GitHub now blocks from updating check runs it didn't create
(https://github.blog/changelog/2025-02-12-notice-of-upcoming-deprecations-and-breaking-changes-for-github-actions/).
"""
import os
import sys
import xml.etree.ElementTree as ET


def main(path: str) -> None:
    if not os.path.exists(path):
        print(f"No Checkstyle report found at {path}")
        return

    tree = ET.parse(path)
    root = tree.getroot()
    cwd = os.getcwd()
    count = 0

    for file_elem in root.findall("file"):
        filename = file_elem.get("name")
        if not filename:
            continue
        try:
            rel = os.path.relpath(filename, cwd)
        except ValueError:
            rel = filename

        for error in file_elem.findall("error"):
            line = error.get("line", "1")
            column = error.get("column")
            severity = error.get("severity", "warning")
            message = (error.get("message") or "").replace("\n", " ").replace("::", ": ")
            level = "error" if severity == "error" else "warning"
            col_part = f",col={column}" if column else ""
            print(f"::{level} file={rel},line={line}{col_part}::[checkstyle] {message}")
            count += 1

    print(f"Checkstyle: {count} annotation(s) emitted")


if __name__ == "__main__":
    main(sys.argv[1] if len(sys.argv) > 1 else "target/checkstyle-result.xml")
