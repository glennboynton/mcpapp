#!/usr/bin/env python3
# app.py - Root of project (./app.py)
# Entry point for the Flask MCP API site application.

from flask import redirect, url_for
from flask_login import current_user

from app import create_app

# ------------------------------------------------------------------------------
def main() -> None:
    """
    Main entry point for running the Flask development server.

    This launches the application in development mode with debug enabled.
    For production deployment, use a WSGI/ASGI server (e.g., gunicorn) and
    configure SSL termination at the front-end proxy or load balancer.

    Author:  Glenn Boynton vibe coded using Perplexity AI Workspace
    Modified:  2025-11-23
    """
    app = create_app()
    app.run(host="0.0.0.0", port=5000, debug=True)


# ------------------------------------------------------------------------------
if __name__ == "__main__":
    main()
