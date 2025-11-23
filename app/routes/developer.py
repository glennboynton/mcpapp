#!/usr/bin/env python3
# app/routes/developer.py - (./app/routes/developer.py)
# Routes for developer role: CRUD on own integrations and dashboard.

from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user

from ..extensions import db
from ..forms import ApiIntegrationForm
from ..models import ApiIntegration
from ..mcp_integration import get_docusaurus_url
from ..security import role_required
from ..api_utils import generate_api_module

developer_bp = Blueprint("developer", __name__)


# ------------------------------------------------------------------------------
@developer_bp.route("/")
@login_required
def dashboard():
    """
    Simple landing page after login showing role-specific entry points.

    Developers see their own integrations; other roles may see different
    dashboards depending on their permissions.

    Author:  Glenn Boynton vibe coded using Perplexity AI Workspace
    Modified:  2025-11-23
    """
    return render_template("dashboard.html")


# ------------------------------------------------------------------------------
@developer_bp.route("/integrations")
@login_required
@role_required("developer", "api_admin", "admin")
def my_integrations():
    """
    List integrations created by the current user.

    Developers can create, update, and delete only records they own,
    while admins or API admins may have alternate interfaces for
    broader management.

    Author:  Glenn Boynton vibe coded using Perplexity AI Workspace
    Modified:  2025-11-23
    """
    integrations = (
        ApiIntegration.query.filter_by(owner_id=current_user.id)
        .order_by(ApiIntegration.name)
        .all()
    )
    doc_links = {i.id: get_docusaurus_url(i) for i in integrations}
    return render_template(
        "developer/my_integrations.html",
        integrations=integrations,
        doc_links=doc_links,
    )


# ------------------------------------------------------------------------------
@developer_bp.route("/integrations/new", methods=["GET", "POST"])
@login_required
@role_required("developer", "api_admin", "admin")
def create_integration():
    """
    Create a new integration owned by the current user.

    Newly created integrations also get an on-disk module scaffold
    in the api/ directory to help jumpstart endpoint coding work.

    Author:  Glenn Boynton vibe coded using Perplexity AI Workspace
    Modified:  2025-11-23
    """
    form = ApiIntegrationForm()
    if form.validate_on_submit():
        integration = ApiIntegration(
            name=form.name.data,
            system_name=form.system_name.data,
            base_url=form.base_url.data,
            endpoint_path=form.endpoint_path.data,
            http_method=form.http_method.data,
            status=form.status.data,
            auth_type=form.auth_type.data,
            api_key=form.api_key.data,
            notes=form.notes.data,
            docusaurus_doc_path=form.docusaurus_doc_path.data,
            owner_id=current_user.id,
        )
        db.session.add(integration)
        db.session.commit()

        generate_api_module(integration)

        flash("Integration created.", "success")
        return redirect(url_for("developer.my_integrations"))

    return render_template("api_admin/integration_form.html", form=form)


# ------------------------------------------------------------------------------
@developer_bp.route("/integrations/<int:integration_id>/edit", methods=["GET", "POST"])
@login_required
@role_required("developer", "api_admin", "admin")
def edit_integration(integration_id: int):
    """
    Edit an integration if and only if the current user is the owner.

    This enforces the rule that developers cannot modify integrations
    created by other users, though they may be able to view them in
    other contexts depending on role.

    Author:  Glenn Boynton vibe coded using Perplexity AI Workspace
    Modified:  2025-11-23
    """
    integration = ApiIntegration.query.get_or_404(integration_id)
    if integration.owner_id != current_user.id and not current_user.is_api_admin:
        flash("You do not have permission to edit this integration.", "danger")
        return redirect(url_for("developer.my_integrations"))

    form = ApiIntegrationForm(obj=integration)
    if form.validate_on_submit():
        form.populate_obj(integration)
        db.session.commit()
        flash("Integration updated.", "success")
        return redirect(url_for("developer.my_integrations"))

    return render_template(
        "api_admin/integration_form.html", form=form, integration=integration
    )


# ------------------------------------------------------------------------------
@developer_bp.route(
    "/integrations/<int:integration_id>/delete", methods=["POST"]
)
@login_required
@role_required("developer", "api_admin", "admin")
def delete_integration(integration_id: int):
    """
    Delete an integration only if the current user is the owner.

    This guardrail prevents accidental or malicious deletion of
    integrations belonging to other developers in the system.

    Author:  Glenn Boynton vibe coded using Perplexity AI Workspace
    Modified:  2025-11-23
    """
    integration = ApiIntegration.query.get_or_404(integration_id)
    if integration.owner_id != current_user.id and not current_user.is_api_admin:
        flash("You do not have permission to delete this integration.", "danger")
        return redirect(url_for("developer.my_integrations"))

    db.session.delete(integration)
    db.session.commit()
    flash("Integration deleted.", "info")
    return redirect(url_for("developer.my_integrations"))
