# 💪 Flask Scaffolder

**flask-scaffolder** is a developer-friendly CLI tool designed to automate the creation of structured, production-ready Flask projects. It simplifies the boilerplate setup by generating a fully-configured project layout tailored to modern development practices.

Whether you're starting a new Flask microservice, prototyping an API backend, or onboarding team members quickly, flask-scaffolder helps you hit the ground running by providing:

🔧 A clean and modular project layout with best practices

📦 A virtual environment ready to go, using venv

🛠️ Pre-configured and extensible configuration files:

.env (rendered dynamically using Jinja2 templates)

.gitignore, requirements.txt, pyproject.toml

.pre-commit-config.yaml for linting and formatting hooks

🚀 Ready-to-use Flask app structure, including:

app/, templates/, and static/ folders

Pre-written routes and initialization boilerplate

📄 Optional VSCode-friendly .vscode/ settings

✅ Easy pre-commit hook setup with one command

🪵 Logging support for both terminal and file

⚙️ Customizable flags for environment settings, SMTP config, secret keys, and more

No more repetitive setup — just scaffold, configure, and start coding. 🔥

## 📁 Project Layout (Internal Package Structure)
```txt
site-packages/
├── flask_scaffolder/                # 🔧 Main Python package
│   ├── __init__.py                  # Package initializer
│   ├── cli.py                       # CLI command logic
│   ├── core.py                      # Core logic for rendering, copying, setup
│   └── artifacts/                   # 📦 Project template files and scaffolding assets
│       ├── app/                     # Default Flask `app/` folder to copy
│       │   ├── __init__.py
│       │   └── routes.py
│       ├── templates/               # HTML templates
│       │   └── base.html
│       ├── static/                  # CSS, JS, etc.
│       │   └── style.css
│       ├── .vscode/                # VSCode workspace recommendations
│       │   └── settings.json
│       ├── .gitignore.j2            # Template for .gitignore
│       ├── .env.j2                  # Template for environment variables
│       ├── requirements.txt         # Default Python dependencies
│       ├── pyproject.toml           # Optional packaging config
│       └── .pre-commit-config.yaml  # Pre-commit hooks setup

```
**📝 Note:** The artifacts/ folder has been placed inside the flask_scaffolder/ package so it's included in the installation and accessible via package-relative paths. This ensures smooth access when copying scaffolding during CLI execution.

- Virtual environment setup
- `.env` rendering (from Jinja templates)
- Pre-configured `.gitignore`, `requirements.txt`, `pyproject.toml`, and `.pre-commit-config.yaml`
- Folder structure copying (e.g., `app/`, `templates/`, `static/`, `.vscode/`)
- Pre-commit hook installation
- Logging to both console and file

---

## 🚀 Installation

### 📦 Local (Editable)
```bash
pip install -e git+https://github.com/fuzumoe/flask_scaffolder.git#egg=flask-scaffolder --break-system-packages
```
or
```bash
git clone https://github.com/yourusername/flask-scaffolder.git
cd flask-scaffolder
pip install -e . --break-system-packages
```

If the `flask-scaffolder` command is not found after installation, add the following to your shell config:

#### For zsh:
```bash
echo 'export PATH="$HOME/.local/bin:$PATH"' >> ~/.zshrc
source ~/.zshrc
```

#### For bash:
```bash
echo 'export PATH="$HOME/.local/bin:$PATH"' >> ~/.bashrc
source ~/.bashrc
```

Then verify:
```bash
flask-scaffolder --help
```

---

## ⚙️ Usage

```bash
flask-scaffolder \
  --output my_project \
  --secret-key supersecret \
  --database-uri sqlite:///db.sqlite3 \
  --api-title "My API" \
  --api-description "Scaffolded with ❤️"
```

### Required

| Flag           | Description                     |
|----------------|---------------------------------|
| `--secret-key` | Flask secret key                |
| `--database-uri` | SQLAlchemy URI (e.g., sqlite:///db.sqlite3) |

### Optional

| Flag               | Default         | Description                              |
|--------------------|-----------------|------------------------------------------|
| `--output`         | `my_project`    | Destination directory                     |
| `--flask-app`      | `run.py`        | Entry point filename                     |
| `--smtp-server`    | `""`            | SMTP server address                      |
| `--smtp-port`      | `587`           | SMTP port                                |
| `--smtp-email`     | `""`            | Email address for outgoing mail          |
| `--smtp-password`  | `""`            | SMTP password                            |
| `--flask-config`   | `dev`           | Flask config profile                     |
| `--api-title`      | `""`            | API Title in generated project           |
| `--api-version`    | `1.0`           | API Version                              |
| `--api-description`| `""`            | Description text for the API             |

---

## 📂 What It Does

📄 Renders `.env` from a Jinja2 template  
👥 Copies project scaffold from `artifacts/` and `app/`  
📦 Creates a Python virtual environment at `.venv/`  
🔧 Installs `requirements.txt`  
🔢 Sets up pre-commit hooks  
🔍 Logs everything to `scaffold.log` in your output directory  

---

## 📁 Project Structure (Example Output)

```
my_project/
├── .env
├── .gitignore
├── .vscode/
├── .venv/
├── app/
├── artifacts/
├── requirements.txt
├── pyproject.toml
├── .pre-commit-config.yaml
├── scaffold.log
└── run.py
```

---

## 🐍 Python Compatibility

- Python 3.8+
- Tested on Python 3.11

--- 