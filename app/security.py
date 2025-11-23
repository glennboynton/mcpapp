#!/usr/bin/env python3
# app/security.py - (./app/security.py)
# Helper utilities for role-based access control and session hygiene.

from functools import wraps
from typing import Callable, Any

from flask import abort
from flask_login import current_user


# ------------------------------------------------------------------------------
def role_required(*roles: str) -> Callable:
    """
    Decorator enforcing that the current user has one of the given roles.

    Example:
        @blueprint.route("/admin-only")
        @login_required
        @role_required("admin")
        def admin_view():
            ...

    Author:  Glenn Boynton vibe coded using Perplexity AI Workspace
    Modified:  2025-11-23
    """

    def decorator(view: Callable) -> Callable:
        @wraps(view)
        def wrapped_view(*args: Any, **kwargs: Any):
            if not current_user.is_authenticated:
                abort(401)
            if not current_user.role or current_user.role.name not in roles:
                abort(403)
            return view(*args, **kwargs)

        return wrapped_view

    return decorator
