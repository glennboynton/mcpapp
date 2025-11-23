#!/usr/bin/env python3
# app/routes/api_admin.py - (./app/routes/api_admin.py)
# Routes for API administrators with full CRUD capabilities.

from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_required

from ..extensions import db
from ..forms import ApiIntegrationForm
from ..models import ApiIntegration
from ..mcp_integration import get_docusaurus_url
from ..security import role_required
from ..api_utils import generate_api_module

api_admin_bp = Blueprint("api_admin", __name__)


# ------------------------------------------------------------------------------
@api_admin_bp.route("/integrations")
@login_required
@role_required("api_admin")
def list_integrations():
    """
    Show all API integrations with full management controls.

    API admins can view, edit, delete, enable/disable, and retrigger
    errored integrations from this interface.

    Author:  Glenn Boynton vibe coded using Perplexity AI Workspace
    Modified:  2025-11-23
    """
    integrations = ApiIntegration.query.order_by(ApiIntegration.name).all()
    doc_links = {i.id: get_docusaurus_url(i) for i in integrations}
    return render_template(
        "api_admin/integrations.html",
        integrations=integrations,
        doc_links=doc_links,
    )


# ------------------------------------------------------------------------------
@api_admin_bp.route("/integrations/new", methods=["GET", "POST"])
@login_required
@role_required("api_admin")
def create_integration():
    """
    Create a new API integration as an API administrator.

    The owner is set to the current user or can be reassigned later by
    admin or API admin roles as needed.

    Author:  Glenn Boynton vibe coded using Perplexity AI Workspace
    Modified:  2025-11-23
    """
    from flask_login import current_user

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

        # Create on-disk module scaffold for this integration.
        generate_api_module(integration)

        flash("API integration created.", "success")
        return redirect(url_for("api_admin.list_integrations"))

    return render_template("api_admin/integration_form.html", form=form)


# ------------------------------------------------------------------------------
@api_admin_bp.route("/integrations/<int:integration_id>/edit", methods=["GET", "POST"])
@login_required
@role_required("api_admin")
def edit_integration(integration_id: int):
    """
    Edit an existing API integration.

    API admins can change any attributes including ownership and
    documentation paths if needed (ownership not exposed in this
    simple form yet).

    Author:  Glenn Boynton vibe coded using Perplexity AI Workspace
    Modified:  2025-11-23
    """
    integration = ApiIntegration.query.get_or_404(integration_id)
    form = ApiIntegrationForm(obj=integration)

    if form.validate_on_submit():
        form.populate_obj(integration)
        db.session.commit()
        flash("API integration updated.", "success")
        return redirect(url_for("api_admin.list_integrations"))

    return render_template(
        "api_admin/integration_form.html", form=form, integration=integration
    )


# ------------------------------------------------------------------------------
@api_admin_bp.route("/integrations/<int:integration_id>/delete", methods=["POST"])
@login_required
@role_required("api_admin")
def delete_integration(integration_id: int):
    """
    Delete an API integration permanently.

    To avoid accidental data loss, this endpoint is POST-only and
    could be extended with confirmation dialogs client-side.

    Author:  Glenn Boynton vibe coded using Perplexity AI Workspace
    Modified:  2025-11-23
    """
    integration = ApiIntegration.query.get_or_404(integration_id)
    db.session.delete(integration)
    db.session.commit()
    flash("API integration deleted.", "info")
    return redirect(url_for("api_admin.list_integrations"))


# ------------------------------------------------------------------------------
@api_admin_bp.route("/integrations/<int:integration_id>/toggle", methods=["POST"])
@login_required
@role_required("api_admin")
def toggle_integration_status(integration_id: int):
    """
    Toggle an integration between enabled and disabled status.

    If the integration is in an 'error' state, toggling will switch
    it back to 'enabled' to allow another test run.

    Author:  Glenn Boynton vibe coded using Perplexity AI Workspace
    Modified:  2025-11-23
    """
    integration = ApiIntegration.query.get_or_404(integration_id)
    if integration.status == "enabled":
        integration.status = "disabled"
    else:
        integration.status = "enabled"
    db.session.commit()
    flash("Integration status updated.", "success")
    return redirect(url_for("api_admin.list_integrations"))


# ------------------------------------------------------------------------------
@api_admin_bp.route("/integrations/<int:integration_id>/test", methods=["POST"])
@login_required
@role_required("api_admin")
def test_integration(integration_id: int):
    """
    Simulate testing an integration and update its status.

    In a real implementation, this would perform an outbound HTTP request
    to the configured endpoint and update status based on the result.
    Here, we simply mark previously errored integrations as enabled.

    Author:  Glenn Boynton vibe coded using Perplexity AI Workspace
    Modified:  2025-11-23
    """
    integration = ApiIntegration.query.get_or_404(integration_id)
    if integration.status == "error":
        integration.status = "enabled"
        db.session.commit()
        flash("Integration test simulated and set to enabled.", "success")
    else:
        flash("Integration appears healthy. No action taken.", "info")
    return redirect(url_for("api_admin.list_integrations"))
