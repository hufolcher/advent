#!/usr/bin/env bash
set -euo pipefail

# ─── CONFIG ────────────────────────────────────────────────
ROOT_DIR=$(pwd)

RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[0;33m'
BLUE='\033[0;34m'
CYAN='\033[0;36m'
BOLD='\033[1m'
DIM='\033[2m'
NC='\033[0m'

WARN="WARN"
RESULTS_REF="results.ref"

# ─── TIME UTIL ─────────────────────────────────────────────
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

# ─── USAGE ─────────────────────────────────────────────────
print_help() {
    echo -e "${BOLD}Usage:${NC}"
    echo "  ./run.sh --all"
    echo "  ./run.sh <YEAR>"
    echo "  ./run.sh <YEAR> <DAY>"
    echo "  ./run.sh <YEAR> <DAY> [--rust|--python]"
    echo "  ./run.sh <YEAR> <DAY> [--submit-p1|--submit-p2]"
    echo
    echo -e "${BOLD}Options:${NC}"
    echo "  --all         Run all years and all days"
    echo "  --rust        Run only Rust solutions"
    echo "  --python      Run only Python solutions"
    echo "  --submit-p1   Submit Part 1 only (requires YEAR + DAY)"
    echo "  --submit-p2   Submit Part 2 only (requires YEAR + DAY)"
    echo
    echo -e "${BOLD}Examples:${NC}"
    echo "  ./run.sh 2025 2 --submit-p1"
    echo "  ./run.sh 2025 2 --rust --submit-p2"
    echo "  ./run.sh 2025 2"
}


# ─── ARG PARSING ───────────────────────────────────────────
RUN_ALL=false
YEAR_FILTER=""
DAY_FILTER=""

RUN_PYTHON=true
RUN_RUST=true
SUBMIT_PART=""

if [[ $# -eq 0 ]]; then
    print_help
    exit 1
fi

while [[ $# -gt 0 ]]; do
    case "$1" in
        --all)
            RUN_ALL=true
            shift
            ;;
        --rust)
            RUN_RUST=true
            RUN_PYTHON=false
            shift
            ;;
        --python)
            RUN_PYTHON=true
            RUN_RUST=false
            shift
            ;;
        --submit-p1)
            SUBMIT_PART="1"
            shift
            ;;
        --submit-p2)
            SUBMIT_PART="2"
            shift
            ;;
        *)
            if [[ -z "$YEAR_FILTER" ]]; then
                YEAR_FILTER="$1"
                [[ ! "$YEAR_FILTER" =~ ^[0-9]{4}$ ]] && {
                    echo -e "${RED}Invalid year${NC}"
                    exit 1
                }
            elif [[ -z "$DAY_FILTER" ]]; then
                DAY_FILTER="$1"
                [[ ! "$DAY_FILTER" =~ ^[0-9]{1,2}$ ]] && {
                    echo -e "${RED}Invalid day${NC}"
                    exit 1
                }
            else
                echo -e "${RED}Unknown option: $1${NC}"
                exit 1
            fi
            shift
            ;;
    esac
done

# ─── SUBMIT SAFETY CHECK ───────────────────────────────────
if [[ -n "$SUBMIT_PART" ]]; then
    if [[ -z "$DAY_FILTER" ]]; then
        echo -e "${RED}Error:${NC} --submit-p$SUBMIT_PART requires an explicit day."
        exit 1
    fi
fi


# ─── ENV CHECK ─────────────────────────────────────────────
if ! command -v uv &>/dev/null; then
    echo -e "${RED}Error: uv not found${NC}"
    exit 1
fi

if [[ -z "${AOC_SESSION:-}" ]]; then
    echo -e "${RED}Error: AOC_SESSION is not set${NC}"
    exit 1
fi

# ─── HEADER ────────────────────────────────────────────────
echo -e "${BOLD}${CYAN}Running Advent of Code${NC}"
echo -e "${DIM}---------------------------------------------${NC}"

# ─── MAIN LOOP ─────────────────────────────────────────────
get_expected() {
    local year="$1"
    local day="$2"
    local part="$3"   # 1 or 2

    if [[ ! -f "$RESULTS_REF" ]]; then
        echo "--"
        return
    fi

    # Take expected value from results.ref (one line per part)
    local expected
    expected=$(awk -v y="$year" -v d="$day" -v p="P$part" \
        '$1==y && $2==d && $3==p {print $4; exit}' "$RESULTS_REF")

    [[ -z "$expected" ]] && expected="--"
    echo "$expected"
}

for year_dir in $(find . -maxdepth 1 -type d -regex './[0-9]+' | sort); do
    year=$(basename "$year_dir")

    if [[ "$RUN_ALL" == false && "$year" != "$YEAR_FILTER" ]]; then
        continue
    fi

    for day_dir in $(find "$year_dir" -maxdepth 1 -mindepth 1 -type d | sort -V); do
        day=$(basename "$day_dir")
        [[ "$day" =~ ^[0-9]+$ ]] || continue

        if [[ -n "$DAY_FILTER" && "$day" != "$DAY_FILTER" ]]; then
            continue
        fi

        input_file="$day_dir/input.txt"

        if [[ ! -s "$input_file" ]]; then
            echo -e "${YELLOW}Fetching input.txt for $year/$day${NC}"

            if ! AOC_YEAR="$year" AOC_DAY="$day" uv run aocd "$year" "$day" > "$input_file"; then
                echo -e "${RED}Failed to fetch input for $year/$day${NC}"
                rm -f "$input_file"
                continue
            fi

            if [[ ! -s "$input_file" ]]; then
                echo -e "${RED}Fetched input is empty for $year/$day${NC}"
                rm -f "$input_file"
                continue
            fi
        fi

        has_solution=false

        py_p1="--"; py_p2="--"
        rs_p1="--"; rs_p2="--"

        py_t1="--"; py_t2="--"
        rs_bt1="--"; rs_rt1="--"
        rs_bt2="--"; rs_rt2="--"

        for part in 1 2; do
            # ─── PYTHON ──────────────────────
            py_file="$day_dir/part$part.py"
            if [[ "$RUN_PYTHON" == true && -f "$py_file" ]]; then
                run_start=$(date +%s%3N)
                py_out=$(python3 "$py_file" < "$day_dir/input.txt" | tail -n 1 | sed 's/[^0-9.-]//g')
                run_end=$(date +%s%3N)

                [[ -z "$py_out" ]] && py_out="--"
                py_time=$(format_time $((run_end - run_start)))

                if [[ "$part" == "1" ]]; then
                    py_p1="$py_out"
                    py_t1="$py_time"
                else
                    py_p2="$py_out"
                    py_t2="$py_time"
                fi

                has_solution=true
            fi

            # ─── RUST ────────────────────────
            if [[ "$RUN_RUST" == true && -f "$day_dir/Cargo.toml" ]]; then
                bin_name="rust_${year}_day${day}_part${part}"
                if grep -q "name = \"$bin_name\"" "$day_dir/Cargo.toml"; then
                    build_start=$(date +%s%3N)
                    cargo build --release \
                        --manifest-path "$day_dir/Cargo.toml" \
                        --bin "$bin_name" \
                        --quiet
                    build_end=$(date +%s%3N)

                    run_start=$(date +%s%3N)
                    rs_out=$("target/release/$bin_name" < "$day_dir/input.txt")
                    run_end=$(date +%s%3N)

                    rs_bt=$(format_time $((build_end - build_start)))
                    rs_rt=$(format_time $((run_end - run_start)))

                    if [[ "$part" == "1" ]]; then
                        rs_p1="$rs_out"
                        rs_bt1="$rs_bt"
                        rs_rt1="$rs_rt"
                    else
                        rs_p2="$rs_out"
                        rs_bt2="$rs_bt"
                        rs_rt2="$rs_rt"
                    fi

                    has_solution=true
                fi
            fi
        done

        exp_p1=$(get_expected "$year" "$day" 1)
        exp_p2=$(get_expected "$year" "$day" 2)

        if [[ "$has_solution" = true ]]; then
            echo -e "${BOLD}${CYAN}Day $day${NC}"
            echo -e "${DIM}---------------------------------------------${NC}"

            # ─── PART 1 ─────────────────────────────
            printf "  ${BOLD}Part 1${NC} |  ${BLUE}Python:${NC} %-20s %-6s   ${GREEN}Rust:${NC} %-20s Build:%-6s Run:%-6s   ${CYAN}Expected:${NC} %-20s\n" \
                "$py_p1" "$py_t1" \
                "$rs_p1" "$rs_bt1" "$rs_rt1" \
                "$exp_p1"

            # ─── PART 2 ─────────────────────────────
            printf "  ${BOLD}Part 2${NC} |  ${BLUE}Python:${NC} %-20s %-6s   ${GREEN}Rust:${NC} %-20s Build:%-6s Run:%-6s   ${CYAN}Expected:${NC} %-20s\n" \
                "$py_p2" "$py_t2" \
                "$rs_p2" "$rs_bt2" "$rs_rt2" \
                "$exp_p2"

            if [[ -n "$SUBMIT_PART" ]]; then
                echo -e "${DIM}Submitting Part $SUBMIT_PART for $year/Day $day...${NC}"

                if [[ "$SUBMIT_PART" == "1" ]]; then
                    py_val="$py_p1"
                    rs_val="$rs_p1"
                else
                    py_val="$py_p2"
                    rs_val="$rs_p2"
                fi

                submit_val=""

                if [[ "$RUN_PYTHON" == true && "$py_val" != "--" ]]; then
                    submit_val="$py_val"
                fi

                if [[ "$RUN_RUST" == true && "$rs_val" != "--" ]]; then
                    if [[ -n "$submit_val" && "$submit_val" != "$rs_val" ]]; then
                        echo -e "${RED}ERROR: Python and Rust results differ — submission blocked${NC}"
                        echo -e "${RED}  Python: $py_val${NC}"
                        echo -e "${RED}  Rust:   $rs_val${NC}"
                        exit 1
                    else
                        submit_val="$rs_val"
                    fi
                fi

                if [[ -z "$submit_val" || "$submit_val" == "--" ]]; then
                    echo -e "${YELLOW}No valid result to submit for Part $SUBMIT_PART${NC}"
                    exit 1
                fi

                echo "$submit_val" | ./submit.sh "$year" "$day" "$SUBMIT_PART"
            fi
        else
            echo -e "${YELLOW}${WARN}: No solutions for $year/Day $day${NC}"
        fi
    done
done
