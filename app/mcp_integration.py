#!/usr/bin/env python3
# app/mcp_integration.py - (./app/mcp_integration.py)
# Stubs for integrating with external MCP-style tools and Docusaurus docs.

from urllib.parse import urljoin

from flask import current_app

from .models import ApiIntegration


# ------------------------------------------------------------------------------
def get_docusaurus_url(integration: ApiIntegration) -> str | None:
    """
    Build a Docusaurus documentation URL for the given integration.

    If the integration specifies a relative documentation path and a base
    URL is configured on the Flask side, this returns a complete URL.
    Otherwise, returns None and the UI will omit the link.

    Author:  Glenn Boynton vibe coded using Perplexity AI Workspace
    Modified:  2025-11-23
    """
    if not integration.docusaurus_doc_path:
        return None
    base = current_app.config.get("DOCUSAURUS_BASE_URL")
    if not base:
        return None
    return urljoin(base.rstrip("/") + "/", integration.docusaurus_doc_path.lstrip("/"))
