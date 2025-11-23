#!/usr/bin/env python3
# app/routes/auth.py - (./app/routes/auth.py)
# Authentication routes for login, logout, and registration.

from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user, login_required, current_user

from ..extensions import db
from ..forms import LoginForm, RegisterForm
from ..models import User, Role

auth_bp = Blueprint("auth", __name__)

@auth_bp.route("/")
def index():
    """
    Default entry route for the root URL.

    Redirects authenticated users to their dashboard, and unauthenticated
    visitors to the login page.

    Author:  Glenn Boynton vibe coded using Perplexity AI Workspace
    Modified:  2025-11-23
    """
    if current_user.is_authenticated:
        return redirect(url_for("developer.dashboard"))
    return redirect(url_for("auth.login"))


# ------------------------------------------------------------------------------
@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    """
    Log a user into the application using email and password.

    On success, redirects to a role-appropriate dashboard. On failure,
    re-renders the login page with an error message.

    Author:  Glenn Boynton vibe coded using Perplexity AI Workspace
    Modified:  2025-11-23
    """
    if current_user.is_authenticated:
        return redirect(url_for("developer.dashboard"))

    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data.lower()).first()
        if user and user.check_password(form.password.data) and user.active:
            login_user(user)
            next_page = request.args.get("next") or url_for("developer.dashboard")
            return redirect(next_page)
        flash("Invalid credentials or inactive account.", "danger")

    return render_template("auth/login.html", form=form)


# ------------------------------------------------------------------------------
@auth_bp.route("/logout")
@login_required
def logout():
    """
    Terminate the current user session and redirect to login.

    Author:  Glenn Boynton vibe coded using Perplexity AI Workspace
    Modified:  2025-11-23
    """
    logout_user()
    flash("You have been logged out.", "info")
    return redirect(url_for("auth.login"))


# ------------------------------------------------------------------------------
@auth_bp.route("/register", methods=["GET", "POST"])
def register():
    """
    Register a new developer user.

    For now, all self-registered accounts are assigned the developer role.
    Admins can later update the role via the admin section.

    Author:  Glenn Boynton vibe coded using Perplexity AI Workspace
    Modified:  2025-11-23
    """
    if current_user.is_authenticated:
        return redirect(url_for("developer.dashboard"))

    form = RegisterForm()
    if form.validate_on_submit():
        existing = User.query.filter_by(email=form.email.data.lower()).first()
        if existing:
            flash("Email already registered.", "warning")
        else:
            dev_role = Role.query.filter_by(name="developer").first()
            user = User(
                email=form.email.data.lower(),
                full_name=form.full_name.data,
                role=dev_role,
            )
            user.set_password(form.password.data)
            db.session.add(user)
            db.session.commit()
            flash("Registration successful. Please log in.", "success")
            return redirect(url_for("auth.login"))

    return render_template("auth/register.html", form=form)
