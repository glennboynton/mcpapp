#!/usr/bin/env python3
# app/routes/admin.py - (./app/routes/admin.py)
# Admin routes for managing users and simple site settings.

from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_required

from ..extensions import db
from ..forms import SiteSettingForm
from ..models import User, Role, SiteSetting
from ..security import role_required

admin_bp = Blueprint("admin", __name__)


# ------------------------------------------------------------------------------
@admin_bp.route("/users")
@login_required
@role_required("admin")
def users():
    """
    Display a list of all registered users for administration.

    Admins can see roles and activation state but are not provided
    with direct CRUD over API integration records via this view.

    Author:  Glenn Boynton vibe coded using Perplexity AI Workspace
    Modified:  2025-11-23
    """
    users = User.query.order_by(User.full_name).all()
    roles = {r.id: r.name for r in Role.query.all()}
    return render_template("admin/users.html", users=users, roles=roles)


# ------------------------------------------------------------------------------
@admin_bp.route("/users/set-role/<int:user_id>", methods=["POST"])
@login_required
@role_required("admin")
def set_user_role(user_id: int):
    """
    Update a user's role based on form selection.

    This endpoint expects a 'role_name' field in the POST body. It
    does not allow deletion of accounts to simplify demo behavior.

    Author:  Glenn Boynton vibe coded using Perplexity AI Workspace
    Modified:  2025-11-23
    """
    role_name = request.form.get("role_name")
    user = User.query.get_or_404(user_id)
    role = Role.query.filter_by(name=role_name).first()
    if role:
        user.role = role
        db.session.commit()
        flash("User role updated.", "success")
    else:
        flash("Invalid role selection.", "danger")
    return redirect(url_for("admin.users"))


# ------------------------------------------------------------------------------
@admin_bp.route("/settings", methods=["GET", "POST"])
@login_required
@role_required("admin")
def settings():
    """
    Basic interface for reading and editing site-level settings.

    This implementation focuses on a single key/value at a time to keep
    the example clear, but it can be extended to a more complex control
    panel as needed.

    Author:  Glenn Boynton vibe coded using Perplexity AI Workspace
    Modified:  2025-11-23
    """
    key = request.args.get("key", "SITE_NAME")
    setting = SiteSetting.query.filter_by(key=key).first()
    form = SiteSettingForm(obj=setting)
    form.key.data = key

    if form.validate_on_submit():
        setting = SiteSetting.query.filter_by(key=form.key.data).first()
        if not setting:
            setting = SiteSetting(key=form.key.data, value=form.value.data)
            db.session.add(setting)
        else:
            setting.value = form.value.data
        db.session.commit()
        flash("Setting saved.", "success")
        return redirect(url_for("admin.settings", key=form.key.data))

    return render_template("admin/settings.html", form=form, setting=setting)
