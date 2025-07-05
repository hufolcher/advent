# 🎄 Advent of Code – Multi-Year, Multi-Language

Welcome to a fully automated **Advent of Code** repository!  
Solve puzzles from multiple years in both **Python** and **Rust**, with scripts to manage folder structure, fetch inputs, and run all solutions.

---

## 📦 Features

- 📁 Organized folder structure per year/day/language  
- 🤖 `fetch.py` to auto-generate directory layout and download inputs  
- 🚀 `run_all.py` to execute all solutions across all years and languages  
- 🧪 Supports both **Python** and **Rust**  
- 🔒 Input fetching using your AoC session token (via cookie)

---

## 🗂️ Repository Structure
```
AoC/
├── rust_workspace/
│   ├── Cargo.toml
│   └── .cargo/config.toml
├── 2021/
│ ├── day01/
│ │ ├── python/
│ │ │ ├── solution.py
│ │ │ └── input.txt
│ │ └── rust/
│ │ ├── solution.rs
│ │ └── input.txt
│ └── ...
├── 2022/
│ └── ...
├── fetch.py # Creates folders & fetches input for a given year/day
└── run_all.py # Executes all solutions for all years and languages
````

Each day's folder includes:
- `input.txt`: your puzzle input  
- `solution.py` or `solution.rs`: your solution script

---

## 🛠️ Setup

### 1. Install dependencies
Python and Rust toolchain (For Rust use ```curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh```)

Install this Python package to fetch input from the AoC website:

```bash
pip install advent-of-code-data
```

### 2. AOC session token has to be available in environmment:
```
export AOC_SESSION="your_session_cookie_here"
```
You can also store it in a .env file or inject it manually.

📥 Usage
Generate Folder + Fetch Input
```
python fetch.py 2023 1
```
This creates:

```
2023/
└── day01/
    ├── python/
    │   ├── input.txt
    │   └── solution.py
    └── rust/
        ├── input.txt
        └── solution.rs
```

🚀 Running Solutions
```
cd 2023/day01/python
python solution.py
```

```
cd 2023/day01/rust
rustc solution.rs -o solution
./solution
```

Your solution scripts should read from input.txt in the same folder.

🔁 Run All Solutions
Automatically run all Python and Rust solutions for all days and years:

```
python run_all.py
```

This script will:

- Recursively find all solution.py and solution.rs files
- Run them in their respective directories
- Print the output with clear headings

✅ Example Output
```
📅 2023 / Day 01 / python
Part 1: 1234
Part 2: 5678

📅 2023 / Day 01 / rust
Part 1: 1234
Part 2: 5678
```

📌 Notes
Make sure solution.py and solution.rs read from input.txt in the same directory.

The project assumes a consistent file naming convention.

Rust solutions are compiled with rustc before execution.

🎯 Todo (Optional Enhancements)
 - Speedrun mode
