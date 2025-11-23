flask_mcp_api_site/
├─ app.py
├─ config.py
├─ requirements.txt
├─ .gitignore
├─ .env.example
├─ run_dev.sh
├─ api/
│  └─ __init__.py
├─ app/
│  ├─ __init__.py
│  ├─ extensions.py
│  ├─ models.py
│  ├─ forms.py
│  ├─ security.py
│  ├─ api_utils.py
│  ├─ mcp_integration.py
│  ├─ routes/
│  │  ├─ __init__.py
│  │  ├─ auth.py
│  │  ├─ admin.py
│  │  ├─ api_admin.py
│  │  ├─ developer.py
│  │  └─ operator.py
│  ├─ templates/
│  │  ├─ base.html
│  │  ├─ layout/
│  │  │  ├─ _navbar.html
│  │  │  └─ _flash.html
│  │  ├─ auth/
│  │  │  ├─ login.html
│  │  │  └─ register.html
│  │  ├─ dashboard.html
│  │  ├─ admin/
│  │  │  ├─ users.html
│  │  │  └─ settings.html
│  │  ├─ api_admin/
│  │  │  ├─ integrations.html
│  │  │  └─ integration_form.html
│  │  ├─ developer/
│  │  │  └─ my_integrations.html
│  │  └─ operator/
│  │     └─ status_dashboard.html
│  └─ static/
│     ├─ scss/
│     │  ├─ main.scss
│     │  └─ _theme.scss
│     ├─ css/
│     │  └─ main.css      # compiled at runtime by Flask-Scss
│     └─ js/
│        └─ main.js
