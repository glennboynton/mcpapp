#!/usr/bin/env python3
# app/api_utils.py - (./app/api_utils.py)
# Utilities for generating and managing API endpoint scaffolding on disk.

from pathlib import Path
from textwrap import dedent

from flask import current_app

from .models import ApiIntegration


# ------------------------------------------------------------------------------
def get_api_root() -> Path:
    """
    Return the root path for generated API modules.

    This function centralizes path handling to make it easier to
    adjust or secure in future iterations.

    Author:  Glenn Boynton vibe coded using Perplexity AI Workspace
    Modified:  2025-11-23
    """
    root = Path(current_app.root_path).parent / "api"
    root.mkdir(exist_ok=True)
    return root


# ------------------------------------------------------------------------------
def generate_api_module(integration: ApiIntegration) -> Path:
    """
    Create a new Python module under the api/ folder for the given integration.

    The generated code is intentionally simple and should be reviewed or
    adapted by developers before exposure to external traffic. The endpoint
    is not auto-registered; developers can wire it into blueprints as needed.

    Author:  Glenn Boynton vibe coded using Perplexity AI Workspace
    Modified:  2025-11-23
    """
    api_root = get_api_root()
    safe_name = f"integration_{integration.id}"
    module_path = api_root / f"{safe_name}.py"

    if module_path.exists():
        return module_path

    content = dedent(
        f'''\
        # api/{safe_name}.py - Auto-generated integration module
        # Generated for integration: {integration.name} (ID: {integration.id})

        from flask import Blueprint, jsonify, request

        blueprint = Blueprint("{safe_name}", __name__)

        @blueprint.route("{integration.endpoint_path}", methods=["{integration.http_method}"])
        def handle_{safe_name}():
            \"\"\"Example handler stub for the generated integration endpoint.

            Replace this logic with real integration behavior. This stub is
            intentionally simple and echoes the request payload for testing.

            Author:  Glenn Boynton vibe coded using Perplexity AI Workspace
            Modified:  2025-11-23
            \"\"\"
            return jsonify({{"message": "Stub handler for {integration.name}", "payload": request.json}}), 200
        '''
    )

    module_path.write_text(content, encoding="utf-8")
    return module_path
