#!/usr/bin/env python3
# app/forms.py - (./app/forms.py)
# WTForms-based form definitions for authentication and CRUD operations.

from flask_wtf import FlaskForm
from wtforms import (
    StringField,
    PasswordField,
    SubmitField,
    TextAreaField,
    SelectField,
)
from wtforms.validators import DataRequired, Email, Length, Optional, URL


# ------------------------------------------------------------------------------
class LoginForm(FlaskForm):
    """
    Login form for authenticating users into the site.

    Author:  Glenn Boynton vibe coded using Perplexity AI Workspace
    Modified:  2025-11-23
    """

    email = StringField("Email", validators=[DataRequired(), Email()])
    password = PasswordField(
        "Password",
        validators=[DataRequired(), Length(min=6, max=128)],
    )
    submit = SubmitField("Login")


# ------------------------------------------------------------------------------
class RegisterForm(FlaskForm):
    """
    Registration form for developer accounts.

    Admins can later reassign roles, but this form defaults to a
    developer-oriented workflow.

    Author:  Glenn Boynton vibe coded using Perplexity AI Workspace
    Modified:  2025-11-23
    """

    full_name = StringField(
        "Full Name",
        validators=[DataRequired(), Length(min=2, max=120)],
    )
    email = StringField("Email", validators=[DataRequired(), Email()])
    password = PasswordField(
        "Password",
        validators=[DataRequired(), Length(min=8, max=128)],
    )
    submit = SubmitField("Register")


# ------------------------------------------------------------------------------
class ApiIntegrationForm(FlaskForm):
    """
    Form for creating or updating API integration records.

    Author:  Glenn Boynton vibe coded using Perplexity AI Workspace
    Modified:  2025-11-23
    """

    name = StringField("Name", validators=[DataRequired()])
    system_name = StringField("System Name", validators=[DataRequired()])
    base_url = StringField("Base URL", validators=[DataRequired(), URL()])
    endpoint_path = StringField(
        "Endpoint Path", validators=[DataRequired(), Length(max=255)]
    )
    http_method = SelectField(
        "HTTP Method",
        choices=["GET", "POST", "PUT", "DELETE", "PATCH"],
        validators=[DataRequired()],
    )
    status = SelectField(
        "Status",
        choices=["enabled", "disabled", "error"],
        validators=[DataRequired()],
    )
    auth_type = SelectField(
        "Auth Type",
        choices=["none", "api_key", "basic"],
        validators=[DataRequired()],
    )
    api_key = StringField("API Key / Credentials", validators=[Optional()])
    notes = TextAreaField("Notes", validators=[Optional()])
    docusaurus_doc_path = StringField(
        "Docusaurus Doc Path", validators=[Optional(), Length(max=255)]
    )
    submit = SubmitField("Save")


# ------------------------------------------------------------------------------
class SiteSettingForm(FlaskForm):
    """
    Form for editing simple site configuration values.

    For now, this form just represents a single key/value item. A more
    advanced settings UI could extend this pattern to structured models.

    Author:  Glenn Boynton vibe coded using Perplexity AI Workspace
    Modified:  2025-11-23
    """

    key = StringField("Key", validators=[DataRequired()])
    value = StringField("Value", validators=[DataRequired()])
    submit = SubmitField("Save")
