#!/usr/bin/env python3
# app/models.py - (./app/models.py)
# SQLAlchemy ORM models for users, roles, and API integrations.

from datetime import datetime

from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

from .extensions import db


# ------------------------------------------------------------------------------
class Role(db.Model):
    """
    Role model for defining user capabilities.

    Roles supported:
      - admin: manages users and site settings, read-only for API records.
      - api_admin: full CRUD on all API integrations and maintenance.
      - developer: full CRUD on own integrations, read-only on others.
      - operator: reporting-only view of API integrations.

    Author:  Glenn Boynton vibe coded using Perplexity AI Workspace
    Modified:  2025-11-23
    """

    __tablename__ = "roles"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True, nullable=False)
    description = db.Column(db.String(255))

    users = db.relationship("User", back_populates="role")


# ------------------------------------------------------------------------------
class User(UserMixin, db.Model):
    """
    User model for authentication and authorization.

    Stores salted+hashed passwords using Werkzeug helpers. For serious
    deployments, prefer a stronger password policy and separate audit
    logging of authentication events.

    Author:  Glenn Boynton vibe coded using Perplexity AI Workspace
    Modified:  2025-11-23
    """

    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    full_name = db.Column(db.String(120), nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    active = db.Column(db.Boolean, default=True)

    role_id = db.Column(db.Integer, db.ForeignKey("roles.id"))
    role = db.relationship("Role", back_populates="users")

    integrations = db.relationship(
        "ApiIntegration", back_populates="owner", lazy="dynamic"
    )

    def set_password(self, password: str) -> None:
        self.password_hash = generate_password_hash(password)

    def check_password(self, password: str) -> bool:
        return check_password_hash(self.password_hash, password)

    @property
    def is_admin(self) -> bool:
        return self.role and self.role.name == "admin"

    @property
    def is_api_admin(self) -> bool:
        return self.role and self.role.name == "api_admin"

    @property
    def is_developer(self) -> bool:
        return self.role and self.role.name == "developer"

    @property
    def is_operator(self) -> bool:
        return self.role and self.role.name == "operator"


# ------------------------------------------------------------------------------
class ApiIntegration(db.Model):
    """
    Primary record for tracking API integrations and MCP-style endpoints.

    Includes status tracking and a reference to optional Docusaurus
    documentation paths for each integration.

    Author:  Glenn Boynton vibe coded using Perplexity AI Workspace
    Modified:  2025-11-23
    """

    __tablename__ = "api_integrations"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    system_name = db.Column(db.String(120), nullable=False)
    base_url = db.Column(db.String(255), nullable=False)
    endpoint_path = db.Column(db.String(255), nullable=False)
    http_method = db.Column(db.String(10), default="GET")
    status = db.Column(
        db.String(20),
        default="enabled",
        doc="enabled, disabled, error",
    )
    auth_type = db.Column(db.String(50), default="api_key")
    api_key = db.Column(db.String(255))
    notes = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(
        db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow
    )

    owner_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    owner = db.relationship("User", back_populates="integrations")

    # Simple Docusaurus doc path, e.g. /integrations/my-api
    docusaurus_doc_path = db.Column(db.String(255))


# ------------------------------------------------------------------------------
class SiteSetting(db.Model):
    """
    Simple key/value table for admin-managed site configuration.

    This can be extended later with structured configuration or versions.

    Author:  Glenn Boynton vibe coded using Perplexity AI Workspace
    Modified:  2025-11-23
    """

    __tablename__ = "site_settings"

    id = db.Column(db.Integer, primary_key=True)
    key = db.Column(db.String(100), unique=True, nullable=False)
    value = db.Column(db.String(255), nullable=False)


# ------------------------------------------------------------------------------
def seed_initial_data() -> None:
    """
    Seed initial roles and an admin user on a new database.

    The default admin user is admin@example.com / admin123. In any
    environment beyond local development, change this password immediately
    after first login.

    Author:  Glenn Boynton vibe coded using Perplexity AI Workspace
    Modified:  2025-11-23
    """
    if Role.query.count() == 0:
        roles = [
            Role(name="admin", description="Site administrator"),
            Role(
                name="api_admin",
                description="Full control over API integrations",
            ),
            Role(
                name="developer",
                description="CRUD on own integrations",
            ),
            Role(
                name="operator",
                description="Read-only operator dashboard",
            ),
        ]
        db.session.add_all(roles)
        db.session.commit()

    if User.query.filter_by(email="admin@example.com").first() is None:
        admin_role = Role.query.filter_by(name="admin").first()
        admin = User(
            email="admin@example.com",
            full_name="Default Admin",
            role=admin_role,
        )
        admin.set_password("admin123")
        db.session.add(admin)
        db.session.commit()
