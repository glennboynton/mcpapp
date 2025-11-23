#!/usr/bin/env python3
# config.py - Root of project (./config.py)
# Central configuration classes and settings for the Flask application.

import os
from pathlib import Path

from dotenv import load_dotenv

BASE_DIR = Path(__file__).resolve().parent
ENV_PATH = BASE_DIR / ".env"
load_dotenv(ENV_PATH)


# ------------------------------------------------------------------------------
class Config:
    """
    Base configuration for all environments.

    This configuration is intentionally minimal and uses environment variables
    for secrets and connection strings. For production, ensure that SECRET_KEY
    and database credentials are injected securely (e.g. via Docker secrets).
    
    Author:  Glenn Boynton vibe coded using Perplexity AI Workspace
    Modified:  2025-11-23
    """

    SECRET_KEY = os.getenv("SECRET_KEY", "dev-secret-change-me")
    SQLALCHEMY_DATABASE_URI = os.getenv(
        "DATABASE_URL", f"sqlite:///{BASE_DIR / 'app.db'}"
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # Session and security-related configuration
    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SECURE = False  # Set True when serving via HTTPS in prod
    REMEMBER_COOKIE_HTTPONLY = True

    # Flask-Scss configuration: compile SCSS at runtime in development
    ASSETS_DEBUG = True
    FLASK_SCSS = {
        "static_dir": "app/static",
        "asset_dir": "app/static/scss",
        "load_path": ["app/static/scss"],
    }

    # Simple configuration section for site settings editable by admin.
    SITE_NAME = os.getenv("SITE_NAME", "MCP API Integration Hub")
    DOCUSAURUS_BASE_URL = os.getenv(
        "DOCUSAURUS_BASE_URL", "http://localhost:3000/docs"
    )


# ------------------------------------------------------------------------------
class DevConfig(Config):
    """Development configuration."""

    DEBUG = True


# ------------------------------------------------------------------------------
class ProdConfig(Config):
    """Production configuration, tuned for SSL / hardened cookies."""

    DEBUG = False
    SESSION_COOKIE_SECURE = True


# ------------------------------------------------------------------------------
def get_config() -> type[Config]:
    """
    Helper function to select the correct configuration class.

    Uses the FLASK_ENV environment variable to decide between development
    and production configuration.

    Author:  Glenn Boynton vibe coded using Perplexity AI Workspace
    Modified:  2025-11-23
    """
    env = os.getenv("FLASK_ENV", "development").lower()
    if env == "production":
        return ProdConfig
    return DevConfig
