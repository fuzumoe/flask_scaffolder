# 💪 Flask Scaffolder

**flask-scaffolder** is a CLI tool for generating Flask-based project structures with built-in:
Project Layout:
```txt
├── site-packages/
│   ├── flask_scaffolder/
│   │   ├── __init__.py
│   │   ├── cli.py
│   │   └── core.py
│   └── artifacts/
│       └── (contents of artifacts)
```

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