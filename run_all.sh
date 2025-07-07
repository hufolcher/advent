#!/usr/bin/env bash

set -euo pipefail

ROOT_DIR=$(pwd)

# ─── Color definitions ──────────────────────────────────────────────────────────
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[0;33m'
BLUE='\033[0;34m'
CYAN='\033[0;36m'
BOLD='\033[1m'
DIM='\033[2m'
NC='\033[0m'  # No Color

# ─── Symbols ─────────────────────────────────────────────────────────────────────
CHECK="✅"
CROSS="❌"
ROCKET="🚀"
GEAR="⚙️"
WARN="⚠️"

# ─── CLI Args ─────────────────────────────────────────────────────────────────────
YEAR_FILTER=""
DAY_FILTER=""

# ─── Time util ────────────────────────────────────────────────────────────────────
format_time() {
    local milliseconds=$1
    local seconds=$((milliseconds / 1000))
    local ms=$((milliseconds % 1000))
    if [ $seconds -eq 0 ]; then
        printf "%dms" "$ms"
    else
        printf "%d.%03ds" "$seconds" "$ms"
    fi
}

# ─── Help ─────────────────────────────────────────────────────────────────────────
print_help() {
    echo -e "${BOLD}Usage:${NC} ./run_all.sh [options]\n"
    echo -e "${BOLD}Options:${NC}"
    echo -e "  -y, --year <YEAR>     Run only a specific year (e.g., 2023)"
    echo -e "  -d, --day <DAY>       Run only a specific day (e.g., 1)"
    echo -e "  -h, --help            Show this help message\n"
    echo -e "${BOLD}Example:${NC}"
    echo -e "  ./run_all.sh             Run all years/days"
    echo -e "  ./run_all.sh -y 2024     Run all days for year 2024"
    echo -e "  ./run_all.sh -y 2024 -d 1 Run day 1 only"
}

while [[ $# -gt 0 ]]; do
    case $1 in
        -y|--year)
            YEAR_FILTER="$2"; shift 2;;
        -d|--day)
            DAY_FILTER="$2"; shift 2;;
        -h|--help)
            print_help; exit 0;;
        *)
            echo -e "${RED}Unknown option: $1${NC}\nUse ${BOLD}-h${NC} for help."; exit 1;;
    esac
done

# ─── aocd / env checks ───────────────────────────────────────────────────────────
if ! command -v aocd &>/dev/null; then
    echo -e "${RED}Error: 'aocd' not found.${NC}"
    echo -e "${YELLOW}Install it with:${BOLD} uv pip install advent-of-code-data${NC}"
    exit 1
fi

if [[ -z "${AOC_SESSION:-}" ]]; then
    echo -e "${RED}Error: AOC_SESSION is not set.${NC}"
    echo -e "${YELLOW}Run:${BOLD} export AOC_SESSION='...'${NC}"
    exit 1
fi

# ─── Header ───────────────────────────────────────────────────────────────────────
echo -e "${BOLD}${CYAN}${ROCKET} Running Advent of Code${NC}"
echo -e "${DIM}──────────────────────────────────────────────${NC}"

# ─── Loop over days ──────────────────────────────────────────────────────────────
for year_dir in $(find . -maxdepth 1 -type d -regex './[0-9]+' | sort); do
    year=$(basename "$year_dir")
    [[ "$year" =~ ^[0-9]{4}$ ]] || continue
    [[ -n "$YEAR_FILTER" && "$year" != "$YEAR_FILTER" ]] && continue

    for day_dir in $(find "$year_dir" -maxdepth 1 -mindepth 1 -type d | sort -V); do
        day=$(basename "$day_dir")
        [[ "$day" =~ ^[0-9]+$ ]] || continue
        [[ -n "$DAY_FILTER" && "$day" != "$DAY_FILTER" ]] && continue

        echo -e "\n${BOLD}📅 Year $year / Day $day${NC}"

        has_solution=false
        input_data=$(AOC_YEAR="$year" AOC_DAY="$day" aocd "$year" "$day")

        # ─── Python ───────────────────────────────────────────────────────────────
        py_dir="$day_dir/python"
        if [[ -d "$py_dir" ]]; then
            for part in 1 2; do
                py_file="$py_dir/part$part.py"
                if [[ -f "$py_file" ]]; then
                    echo -e "${BLUE}🐍 Python Part $part${NC}"
                    (
                        cd "$py_dir"
                        run_start=$(date +%s%3N)
                        echo "$input_data" | python3 "part$part.py"
                        run_end=$(date +%s%3N)
                        run_duration=$((run_end - run_start))
                        echo -e "${DIM}Run Time: $(format_time "$run_duration")${NC}"
                    )
                    has_solution=true
                fi
            done
        fi

        # ─── Rust ────────────────────────────────────────────────────────────────
        rust_dir="$day_dir/rust"
        if [[ -d "$rust_dir" && -f "$rust_dir/Cargo.toml" ]]; then
            for part in 1 2; do
                bin_name="part$part"
                rs_file="$rust_dir/$bin_name.rs"
                if [[ -f "$rs_file" ]]; then
                    echo -e "${GREEN}🦀 Rust Part $part${NC}"

                    build_start=$(date +%s%3N)
                    cargo build --release --bin "$bin_name" --manifest-path "$rust_dir/Cargo.toml" &>/dev/null
                    build_end=$(date +%s%3N)

                    run_start=$(date +%s%3N)
                    echo "$input_data" | ./target/release/$bin_name
                    run_end=$(date +%s%3N)

                    echo -e "${DIM}Build Time: $(format_time $((build_end - build_start)))${NC}"
                    echo -e "${DIM}Run Time:   $(format_time $((run_end - run_start)))${NC}"

                    has_solution=true
                fi
            done
        fi

        if [[ "$has_solution" = false ]]; then
            echo -e "${YELLOW}${WARN} No solutions for ${year}/Day ${day}${NC}"
        fi
    done
done
