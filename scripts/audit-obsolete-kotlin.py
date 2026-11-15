#!/usr/bin/env python3
"""Conservative audit of legacy-named Kotlin files; reports only, never deletes."""
from pathlib import Path
import re

SOURCE_ROOT = Path("app/composeApp/src")
KOTLIN = sorted(SOURCE_ROOT.rglob("*.kt"))
LEGACY_NAME = re.compile(r"(legacy|deprecated|obsolete|old)", re.IGNORECASE)
DECLARATION = re.compile(
    r"(?m)^\s*(?:(?:public|internal|private|protected|expect|actual|inline|suspend|data|sealed|open|abstract|enum|annotation|value|infix|operator|tailrec|external)\s+)*"
    r"(?:class|object|interface|typealias|fun|val|var)\s+([A-Za-z_][A-Za-z0-9_]*)"
)

def occurrences(symbol: str, files: list[Path]) -> list[Path]:
    pattern = re.compile(rf"\b{re.escape(symbol)}\b")
    return [path for path in files if pattern.search(path.read_text(encoding="utf-8", errors="ignore"))]

candidates = [path for path in KOTLIN if LEGACY_NAME.search(path.name)]
if not candidates:
    print("No legacy-named Kotlin files found.")
    raise SystemExit(0)

reported = 0
for source in candidates:
    declarations = sorted(set(DECLARATION.findall(source.read_text(encoding="utf-8", errors="ignore"))))
    other_files = [path for path in KOTLIN if path != source]
    unreferenced = []
    for symbol in declarations:
        refs = occurrences(symbol, other_files)
        if not refs:
            unreferenced.append(symbol)
    if unreferenced:
        reported += 1
        print(f"REVIEW {source}: declarations with no references outside this file: {', '.join(unreferenced)}")

if not reported:
    print("No unreferenced declarations found in legacy-named Kotlin files.")

print("This is a conservative review report, not an automatic deletion list.")
