# ─── Color definitions ──────────────────────────────────────────────────────────
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[0;33m'
BLUE='\033[0;34m'
CYAN='\033[0;36m'
BOLD='\033[1m'
DIM='\033[2m'
NC='\033[0m'  # No Color

# ─── Check for AOC_SESSION env var ───────────────────────────────────────────────
if [[ -z "${AOC_SESSION:-}" ]]; then
    echo -e "${RED}Error: AOC_SESSION environment variable is not set.${NC}"
    echo -e "${YELLOW}You must set your Advent of Code session token first.${NC}"
    echo -e "${YELLOW}${BOLD}export AOC_SESSION='your_session_cookie_here'${NC}"
    echo ""
fi

curl -Ls https://astral.sh/uv/install.sh | bash
uv venv
source .venv/bin/activate
uv pip install advent-of-code-data
