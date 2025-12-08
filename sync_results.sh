#!/usr/bin/env bash
set -euo pipefail

if [[ $# -ne 1 ]]; then
  echo "Usage: $0 <YEAR>"
  echo "Example: $0 2025"
  exit 1
fi

YEAR="$1"
RESULTS_REF="results.ref"

if [[ -z "${AOC_SESSION:-}" ]]; then
  echo "Error: AOC_SESSION is not set"
  exit 1
fi

# Ensure file exists (DO NOT truncate)
touch "$RESULTS_REF"

echo "Syncing historical AoC results for year $YEAR..."
echo "Appending missing entries to $RESULTS_REF"
echo

uv run python - <<EOF
import time
from pathlib import Path
from aocd.models import Puzzle
from aocd.exceptions import PuzzleUnsolvedError, AocdError

year = int("$YEAR")
ref_file = Path("$RESULTS_REF")

existing = set()
with ref_file.open() as f:
    for line in f:
        existing.add(line.strip())

new_lines = []

for day in range(1, 26):
    try:
        p = Puzzle(year=year, day=day)
    except AocdError:
        continue

    # --- Part 1
    try:
        a = p.answer_a
    except (PuzzleUnsolvedError, AttributeError):
        a = None

    if a:
        line = f"{year} {day} P1 {a}"
        if line not in existing:
            new_lines.append(line)

    time.sleep(0.1)  # ✅ RATE LIMIT

    # --- Part 2
    try:
        b = p.answer_b
    except (PuzzleUnsolvedError, AttributeError):
        b = None

    if b:
        line = f"{year} {day} P2 {b}"
        if line not in existing:
            new_lines.append(line)

    time.sleep(0.1)  # ✅ RATE LIMIT

if new_lines:
    with ref_file.open("a") as f:
        for line in new_lines:
            f.write(line + "\\n")

print(f"Added {len(new_lines)} new entries.")
EOF

echo
echo "Current results.ref:"
echo "--------------------------------"
cat "$RESULTS_REF"
