#!/usr/bin/env bash
set -e

# ─── CONFIG ────────────────────────────────────────────────
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[0;33m'
BLUE='\033[0;34m'
CYAN='\033[0;36m'
BOLD='\033[1m'
DIM='\033[2m'
NC='\033[0m'
WARN="WARN"

# ─── USAGE ─────────────────────────────────────────────────
print_help() {
    echo -e "${BOLD}Usage:${NC}"
    echo "  ./setup_new_year.sh <YEAR> <DAY> <LANGS>"
    echo
    echo -e "${BOLD}Examples:${NC}"
    echo "  ./setup_new_year.sh 2025 12 rust"
}

# ─── ARGUMENTS ─────────────────────────────────────────────
if [[ -z "$1" || -z "$2" || -z "$3" ]]; then
  print_help
  exit 1
fi

YEAR="$1"
DAYS="$2"
LANGS="$3"
EDITION="2024"

# ─── VALIDATION ────────────────────────────────────────────
if [[ ! "$YEAR" =~ ^[0-9]{4}$ ]]; then
  echo "YEAR must be a 4-digit number (e.g., 2025)"
  exit 1
fi

if [[ ! "$DAYS" =~ ^[0-9]+$ || "$DAYS" -lt 1 || "$DAYS" -gt 25 ]]; then
  echo "NUMBER_OF_DAYS must be between 1 and 25"
  exit 1
fi

IFS=',' read -ra LANG_LIST <<< "$LANGS"
for lang in "${LANG_LIST[@]}"; do
  if [[ "$lang" != "rust" && "$lang" != "python" ]]; then
    echo "Invalid language: $lang (allowed: rust, python)"
    exit 1
  fi
done

echo "Setting up Advent of Code $YEAR with $DAYS days"
mkdir -p "$YEAR"
cd "$YEAR"

# ─── DAYS SETUP ────────────────────────────────────────────
for d in $(seq 1 "$DAYS"); do
  echo "Day $d"
  mkdir -p "$d"

  # ---------- RUST ----------
  if [[ " ${LANG_LIST[*]} " == *" rust "* ]]; then
    if [[ ! -f "$d/Cargo.toml" ]]; then
      echo "  Creating Cargo.toml"
      cat > "$d/Cargo.toml" <<EOF
[package]
name = "day$d"
version = "0.1.0"
edition = "$EDITION"

[[bin]]
name = "rust_${YEAR}_day${d}_part1"
path = "part1.rs"

[[bin]]
name = "rust_${YEAR}_day${d}_part2"
path = "part2.rs"
EOF
    else
      echo "  Cargo.toml already exists, nothing to do"
    fi

    if [[ ! -f "$d/part1.rs" ]]; then
      echo "  Creating part1.rs"
      cat > "$d/part1.rs" <<'EOF'
use std::io;

fn main() {
    let input = io::read_to_string(io::stdin()).unwrap();
    println!("{}", input.lines().count());
}
EOF
    else
      echo "  part1.rs already exists, nothing to do"
    fi

    if [[ ! -f "$d/part2.rs" ]]; then
      echo "  Creating part2.rs"
      cat > "$d/part2.rs" <<'EOF'
use std::io;

fn main() {
    let input = io::read_to_string(io::stdin()).unwrap();
    println!("{}", input.len());
}
EOF
    else
      echo "  part2.rs already exists, nothing to do"
    fi
  else
    echo "  Rust not selected, skipping Rust setup"
  fi

  # ---------- PYTHON ----------
  if [[ " ${LANG_LIST[*]} " == *" python "* ]]; then
    if [[ ! -f "$d/part1.py" ]]; then
      echo "  Creating part1.py"
      cat > "$d/part1.py" <<'EOF'
import sys
data = sys.stdin.read()
print(len(data.splitlines()))
EOF
    else
      echo "  part1.py already exists, nothing to do"
    fi

    if [[ ! -f "$d/part2.py" ]]; then
      echo "  Creating part2.py"
      cat > "$d/part2.py" <<'EOF'
import sys
data = sys.stdin.read()
print(len(data))
EOF
    else
      echo "  part2.py already exists, nothing to do"
    fi
  else
    echo "  Python not selected, skipping Python setup"
  fi
done

cd ..

# ─── WORKSPACE UPDATE (RUST ONLY) ──────────────────────────
if [[ " ${LANG_LIST[*]} " == *" rust "* ]]; then
  WORKSPACE_TOML="Cargo.toml"
  echo "Updating workspace Cargo.toml..."

  NEW_MEMBERS=$(for d in $(seq 1 "$DAYS"); do
    echo "\"$YEAR/$d\""
  done)

  if [[ ! -f "$WORKSPACE_TOML" ]]; then
    echo "  Workspace does not exist, creating it"
    {
      echo "[workspace]"
      echo "resolver = \"2\""
      echo "members = ["
      for m in $NEW_MEMBERS; do
        echo "    $m,"
      done
      echo "]"
    } > "$WORKSPACE_TOML"

  else
    echo "  Workspace exists, adding missing members only"

    TMP_FILE="$(mktemp)"

    awk '
      BEGIN {in_members=0}
      /^\[workspace\]/ {print; next}
      /^members\s*=\s*\[/ {in_members=1; print; next}
      in_members && /^\]/ {print; in_members=0; next}
      {print}
    ' "$WORKSPACE_TOML" > "$TMP_FILE"

    while read -r member; do
      if ! grep -q "$member" "$WORKSPACE_TOML"; then
        sed -i "/^members\s*=\s*\[/a\    $member," "$TMP_FILE"
        echo "  Added $member"
      else
        echo "  Already present: $member"
      fi
    done <<< "$NEW_MEMBERS"

    mv "$TMP_FILE" "$WORKSPACE_TOML"
  fi
else
  echo "Rust not selected, workspace not modified"
fi

echo "Advent of Code $YEAR setup complete"
