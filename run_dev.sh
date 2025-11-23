#!/usr/bin/env bash
# run_dev.sh - Root of project (./run_dev.sh)
# Convenience script to run the development server.

export FLASK_ENV=development
export FLASK_APP=app.py
python3 app.py
