#!/usr/bin/env bash
set -euo pipefail

# --- CONFIG
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[0;33m'
BLUE='\033[0;34m'
CYAN='\033[0;36m'
BOLD='\033[1m'
DIM='\033[2m'
NC='\033[0m'
WARN="WARN"

# --- USAGE
if [[ $# -lt 3 ]]; then
  echo -e "${BOLD}Usage:${NC} $0 <YEAR> <DAY> <PART> [<ANSWER>]"
  echo
  echo "PART: 1 or 2"
  echo "If ANSWER is omitted, it is read from stdin"
  echo
echo -e "${BOLD}Examples:${NC}"
  echo "  ./submit.sh 2025 12 1 4035"
  echo "  echo 4035 | ./submit.sh 2025 12 1"
  exit 1
fi

YEAR="$1"
DAY="$2"
PART="$3"

# Read answer from arg or stdin
if [[ $# -eq 4 ]]; then
  ANSWER="$4"
else
  read -r ANSWER
fi

# Validation
[[ ! "$YEAR" =~ ^[0-9]{4}$ ]] && { echo "Invalid YEAR"; exit 1; }
[[ ! "$DAY" =~ ^[0-9]{1,2}$ ]] && { echo "Invalid DAY"; exit 1; }
[[ "$PART" != "1" && "$PART" != "2" ]] && { echo "PART must be 1 or 2"; exit 1; }

if [[ -z "${AOC_SESSION:-}" ]]; then
  echo "Error: AOC_SESSION is not set"
  exit 1
fi

# Map part to aocd format
if [[ "$PART" == "1" ]]; then
  PART_LETTER="a"
else
  PART_LETTER="b"
fi

echo "Submitting:"
echo "  Year:   $YEAR"
echo "  Day:    $DAY"
echo "  Part:   $PART ($PART_LETTER)"
echo "  Answer: $ANSWER"
echo

AOC_YEAR="$YEAR" AOC_DAY="$DAY" \
uv run python - <<EOF
from aocd import submit

part = "a" if "$PART" == "1" else "b"
submit("$ANSWER", year=$YEAR, day=$DAY, part=part)
EOF

