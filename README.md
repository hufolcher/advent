# 🎄 Advent of Code

Fully automated **Advent of Code** repository with:

- Rust & Python support
- Automatic input fetching
- Batch execution with formatted output
- Reference result checking
- Automatic submission to AoC
- Workspace-managed Rust builds

No manual compilation, no copy/paste, no browser juggling.

---

## Features

- Year / Day structured layout
- Python solutions (`part1.py`, `part2.py`)
- Rust solutions (workspace + per-day binaries)
- Automatic input fetching via `aocd` + `uv`
- Unified runner with timing, formatting & filters
- Reference result comparison via `results.ref`
- Automatic submission script (`submit.sh`)
- Cross-language result verification
- Rust workspace auto-managed

---

## Repository Structure

```bash
advent/
├── 2024/
│   ├── 1/
│   │   ├── part1.py
│   │   ├── part2.py
│   │   ├── part1.rs
│   │   ├── part2.rs
│   │   ├── Cargo.toml
│   │   └── input.txt
│   ├── 2/
│   └── ...
├── 2025/
│   └── ...
├── Cargo.toml          # Rust workspace
├── run.sh              # Run all / year / day / language
├── submit.sh           # Submit answers to AoC
├── sync_results.sh     # Sync historical results
└── results.ref         # Reference answers
```

Each day folder contains:

- `input.txt` – puzzle input
- `part1.py`, `part2.py` – Python solutions
- `part1.rs`, `part2.rs` – Rust solutions
- `Cargo.toml` – Rust per-day binary config

---

## Setup

### Install dependencies

#### Python + uv

```bash
curl -Ls https://astral.sh/uv/install.sh | bash
uv venv
source .venv/bin/activate
uv pip install advent-of-code-data
```

#### Rust

```bash
curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh
```

---

### Set your AoC session token

```bash
export AOC_SESSION=\"your_session_cookie_here\"
```

This is required for input fetching, result syncing, and submissions.

---

## Input Fetching

Inputs are fetched automatically by `run.sh` when missing:

```bash
./run.sh 2025 1
```

This creates:

```text
2025/1/input.txt
```

No separate fetch command is required.

---

## Running Solutions (`run.sh`)

### Run everything

```bash
./run.sh --all
```

### Run a full year

```bash
./run.sh 2025
```

### Run a single day

```bash
./run.sh 2025 3
```

### Run Rust only

```bash
./run.sh 2025 --rust
./run.sh 2025 3 --rust
```

### Run Python only

```bash
./run.sh 2025 --python
./run.sh 2025 3 --python
```

---

### Output Format

```text
Day 1
  Part 1 |  Python: 4035     14ms     Rust: 4035     Build:43ms  Run:3ms   Expected:4035
  Part 2 |  Python: 5872     15ms     Rust: 5872     Build:40ms  Run:4ms   Expected:5872
```

If no solution exists:

```text
WARN: No solutions for 2025/Day 12
```

---

## Reference Results (`results.ref`)

Reference file format:

```text
2025 1 P1 4035
2025 1 P2 5872
2025 2 P1 30608905813
2025 2 P2 31898925685
```

Used by `run.sh` to:

- Check correctness
- Display expected values inline
- Detect regressions

---

## Sync Historical Results (`sync_results.sh`)

Fetches your already solved AoC answers from the official website:

```bash
./sync_results.sh 2025
```

The script:

- Queries AoC using `aocd`
- Writes clean reference output to `results.ref`
- Skips unsolved days
- Applies rate-limiting

---

## Submit Answers (`submit.sh`)

Submit an answer safely to AoC:

### Direct value

```bash
./submit.sh 2025 1 1 4035
```

### From stdin

```bash
echo 4035 | ./submit.sh 2025 1 1
```

The script detects:

- Wrong answers
- Already solved parts
- Server feedback in real time

---

## Language Cross-Check

If Python and Rust are both enabled:

- Outputs are compared automatically
- If they differ, a warning is printed
- Only matching results should be submitted

If only one language is enabled, that one is used.

---

## Rust Workspace

- All days are registered in the root `Cargo.toml` workspace
- Each day exposes:
  - `dayX_part1`
  - `dayX_part2`
- Builds are fully incremental and isolated

---

## Notes

- All scripts are Bash-first, no Python orchestration required
- Output formatting is fixed-width and stable
- Clean CI-style logs
- Suitable for:
  - Local execution
  - CI pipelines
  - Benchmarking
  - Submission automation

