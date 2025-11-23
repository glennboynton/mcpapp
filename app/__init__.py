#!/usr/bin/env python3
# app/__init__.py - Package root (./app/__init__.py)
# Application factory and high-level wiring for the Flask MCP API site.

from flask import Flask, redirect, url_for
from flask_scss import Scss

from config import get_config
from .extensions import db, login_manager
from .models import User, Role, seed_initial_data
from .routes.auth import auth_bp
from .routes.admin import admin_bp
from .routes.api_admin import api_admin_bp
from .routes.developer import developer_bp
from .routes.operator import operator_bp


# ------------------------------------------------------------------------------
def create_app() -> Flask:
    """
    Application factory for creating a configured Flask instance.

    Wires core extensions, registers blueprints, and runs initial database
    migrations and seeding where necessary. This design keeps the top-level
    app.py thin and makes the codebase easier to test or embed in WSGI
    servers.

    Author:  Glenn Boynton vibe coded using Perplexity AI Workspace
    Modified:  2025-11-23
    """
    app = Flask(__name__)
    app.config.from_object(get_config())

    # Initialize Flask-Scss for runtime SCSS compilation for development.
    # In production, prefer precompiled CSS assets.
    Scss(app, asset_dir="app/static/scss", static_dir="app/static/css")

    # Initialize extensions
    db.init_app(app)
    login_manager.init_app(app)

    # Configure user loader for Flask-Login
    @login_manager.user_loader
    def load_user(user_id: str) -> User | None:
        return User.query.get(int(user_id))

    # Simple unauthorized handler redirecting to login page.
    login_manager.login_view = "auth.login"

    # Register blueprints for separated concerns.
    app.register_blueprint(auth_bp)
    app.register_blueprint(admin_bp, url_prefix="/admin")
    app.register_blueprint(api_admin_bp, url_prefix="/api-admin")
    app.register_blueprint(developer_bp, url_prefix="/developer")
    app.register_blueprint(operator_bp, url_prefix="/operator")

    # Moved to /app/auth.py where current_user is defined.
    # Default route: redirect to login or dashboard
    # @app.route("/")
    # def index():
    #     if current_user.is_authenticated:
    #         return redirect(url_for("developer.dashboard"))
    #     return redirect(url_for("auth.login"))

    # Ensure database and seed roles/users.
    with app.app_context():
        db.create_all()
        seed_initial_data()

    return app
