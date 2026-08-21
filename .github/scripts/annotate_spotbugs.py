#!/usr/bin/env python3
"""Turn a SpotBugs XML report into native GitHub Actions annotations.

See annotate_checkstyle.py for why this avoids third-party check-run
based actions.
"""
import os
import sys
import xml.etree.ElementTree as ET


def main(path: str) -> None:
    if not os.path.exists(path):
        print(f"No SpotBugs report found at {path}")
        return

    tree = ET.parse(path)
    root = tree.getroot()
    count = 0

    for bug in root.findall("BugInstance"):
        priority = bug.get("priority", "3")
        long_message_elem = bug.find("LongMessage")
        message = (
            long_message_elem.text
            if long_message_elem is not None and long_message_elem.text
            else bug.get("type", "SpotBugs issue")
        )
        message = message.replace("\n", " ").replace("::", ": ")

        source_line = bug.find("SourceLine")
        if source_line is None:
            continue
        sourcepath = source_line.get("sourcepath")
        start = source_line.get("start", "1")
        if not sourcepath:
            continue

        level = "warning" if priority in ("1", "2") else "notice"
        print(f"::{level} file=src/main/java/{sourcepath},line={start}::[spotbugs] {message}")
        count += 1

    print(f"SpotBugs: {count} annotation(s) emitted")


if __name__ == "__main__":
    main(sys.argv[1] if len(sys.argv) > 1 else "target/spotbugsXml.xml")
