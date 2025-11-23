#!/usr/bin/env bash
# run_all_dev.sh - Root of project (./run_all_dev.sh)
# Convenience script to start Flask dev server AND Docusaurus dev server.

set -euo pipefail

###############################################################################
# Helper: print usage
###############################################################################
usage() {
  cat <<'EOF'
Usage: ./run_all_dev.sh

Starts:
  - Flask dev server on http://localhost:5000
  - Docusaurus dev server on http://localhost:3000

Requirements:
  - Python environment with Flask app dependencies installed (see requirements.txt)
  - Node.js + npm installed
  - Docusaurus site scaffolded under ./docs (run:
      npx create-docusaurus@latest docs classic
      cd docs && npm install && cd ..
    )

Author:  Glenn Boynton vibe coded using Perplexity AI Workspace
Modified:  2025-11-23
EOF
}

if [[ "${1-}" == "-h" || "${1-}" == "--help" ]]; then
  usage
  exit 0
fi

###############################################################################
# Start Flask dev server
###############################################################################
echo "[run_all_dev] Starting Flask dev server on http://localhost:5000 ..."
export FLASK_ENV=development
export FLASK_APP=app.py

# Start Flask in background
python3 app.py &
FLASK_PID=$!
echo "[run_all_dev] Flask PID: ${FLASK_PID}"

###############################################################################
# Start Docusaurus dev server
###############################################################################
if [[ ! -d "docs" ]]; then
  echo "[run_all_dev] ERROR: ./docs directory not found."
  echo "  Please scaffold Docusaurus with:"
  echo "    npx create-docusaurus@latest docs classic"
  exit 1
fi

echo "[run_all_dev] Starting Docusaurus dev server on http://localhost:3000 ..."
cd docs
npm start &
DOCS_PID=$!
cd ..

echo "[run_all_dev] Docusaurus PID: ${DOCS_PID}"
echo "[run_all_dev] Both dev servers started."
echo "  Flask:      http://localhost:5000"
echo "  Docusaurus: http://localhost:3000"

###############################################################################
# Trap and cleanup on exit
###############################################################################
cleanup() {
  echo
  echo "[run_all_dev] Stopping dev servers..."
  if kill -0 "${FLASK_PID}" 2>/dev/null; then
    kill "${FLASK_PID}" || true
  fi
  if kill -0 "${DOCS_PID}" 2>/dev/null; then
    kill "${DOCS_PID}" || true
  fi
  echo "[run_all_dev] Done."
}

trap cleanup INT TERM

# Wait on both processes
wait "${FLASK_PID}" "${DOCS_PID}" || true
