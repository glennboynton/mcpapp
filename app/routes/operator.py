#!/usr/bin/env python3
# app/routes/operator.py - (./app/routes/operator.py)
# Operator routes for read-only dashboards on integration status.

from flask import Blueprint, render_template
from flask_login import login_required

from ..models import ApiIntegration
from ..security import role_required
from ..mcp_integration import get_docusaurus_url

operator_bp = Blueprint("operator", __name__)


# ------------------------------------------------------------------------------
@operator_bp.route("/status")
@login_required
@role_required("operator", "admin", "api_admin")
def status_dashboard():
    """
    Display high-level status of all API integrations.

    Operators can view counts by status, drill into integration details,
    and navigate to documentation links without performing CRUD actions.

    Author:  Glenn Boynton vibe coded using Perplexity AI Workspace
    Modified:  2025-11-23
    """
    integrations = ApiIntegration.query.all()
    counts = {"enabled": 0, "disabled": 0, "error": 0}
    for i in integrations:
        counts[i.status] = counts.get(i.status, 0) + 1
    doc_links = {i.id: get_docusaurus_url(i) for i in integrations}
    return render_template(
        "operator/status_dashboard.html",
        integrations=integrations,
        counts=counts,
        doc_links=doc_links,
    )
