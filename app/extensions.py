#!/usr/bin/env python3
# app/extensions.py - (./app/extensions.py)
# Centralized Flask extension instances.

from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

# ------------------------------------------------------------------------------
# SQLAlchemy database instance shared across the app.
db = SQLAlchemy()

# ------------------------------------------------------------------------------
# Flask-Login manager to handle user sessions and authentication.
login_manager = LoginManager()

"""
Author:  Glenn Boynton vibe coded using Perplexity AI Workspace
Modified:  2025-11-23
"""
