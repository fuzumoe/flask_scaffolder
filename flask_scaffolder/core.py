# flask_scaffolder/core.py
import logging
import os
import shutil
import subprocess

from jinja2 import Environment, FileSystemLoader


def setup_logger(log_file_path: str):
    logger = logging.getLogger("flask_scaffolder")
    logger.setLevel(logging.INFO)
    logger.handlers.clear()

    console_handler = logging.StreamHandler()
    console_handler.setFormatter(logging.Formatter("🔧 %(levelname)s: %(message)s"))
    logger.addHandler(console_handler)

    file_handler = logging.FileHandler(log_file_path)
    file_handler.setFormatter(
        logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
    )
    logger.addHandler(file_handler)

    return logger


def render_jinja_template(template_dir, template_file, output_path, context, logger):
    if os.path.exists(output_path):
        logger.info(f"⏩ Skipped rendering .env (already exists): {output_path}")
        return
    env = Environment(loader=FileSystemLoader(template_dir))
    template = env.get_template(template_file)
    content = template.render(context)
    with open(output_path, "w") as f:
        f.write(content)
    logger.info(f"✅ Rendered: {output_path}")


def copy_file(src_dir, file_name, dest_dir, logger):
    src = os.path.join(src_dir, file_name)
    dst = os.path.join(dest_dir, file_name)
    if os.path.exists(dst):
        logger.info(f"⏩ Skipped (already exists): {dst}")
        return
    try:
        shutil.copy(src, dst)
        logger.info(f"✅ Copied: {dst}")
    except Exception as e:
        logger.error(f"❌ Failed to copy {file_name}: {e}")


def copy_directory(src_dir, dst_dir, logger):
    dest = os.path.join(dst_dir, os.path.basename(src_dir))
    if os.path.exists(dest):
        logger.info(f"⏩ Skipped directory (already exists): {dest}")
        return
    try:
        shutil.copytree(src_dir, dest)
        logger.info(f"✅ Cloned directory: {dest}")
    except Exception as e:
        logger.error(f"❌ Failed to copy directory {src_dir}: {e}")


def scaffold_project(target_dir: str, context: dict):
    os.makedirs(target_dir, exist_ok=True)

    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    artifacts_dir = os.path.join(base_dir, "artifacts")

    log_file_path = os.path.join(target_dir, "scaffold.log")
    logger = setup_logger(log_file_path)
    logger.info("🚀 Starting project scaffold...")

    render_jinja_template(
        artifacts_dir, ".env.j2", os.path.join(target_dir, ".env"), context, logger
    )
    _copy_main_files(artifacts_dir, target_dir, logger)
    _copy_optional_dirs(artifacts_dir, target_dir, logger)
    _setup_virtualenv_and_dependencies(target_dir, logger)


def _copy_main_files(artifacts_dir: str, target_dir: str, logger):
    for f in [
        ".gitignore",
        "requirements.txt",
        ".pre-commit-config.yaml",
        "pyproject.toml",
    ]:
        copy_file(artifacts_dir, f, target_dir, logger)

    app_dir = os.path.join(artifacts_dir, "app")
    if os.path.exists(app_dir):
        copy_directory(app_dir, target_dir, logger)
    else:
        logger.warning("⚠️ 'app/' not found in artifacts")


def _copy_optional_dirs(artifacts_dir: str, target_dir: str, logger):
    for folder in [".vscode", "templates", "static"]:
        path = os.path.join(artifacts_dir, folder)
        if os.path.exists(path):
            copy_directory(path, target_dir, logger)
        else:
            logger.warning(f"⚠️ '{folder}/' not found in artifacts")


def _setup_virtualenv_and_dependencies(target_dir: str, logger):
    logger.info("📦 Creating virtual environment and installing dependencies...")
    venv_path = os.path.join(target_dir, ".venv")

    if not os.path.exists(venv_path):
        try:
            import venv

            venv.create(venv_path, with_pip=True)
            logger.info(f"✅ Created virtual environment: {venv_path}")
        except Exception as e:
            logger.error(f"❌ Failed to create venv: {e}")
            return
    else:
        logger.info(f"⏩ Skipped virtual environment (already exists): {venv_path}")

    pip_path = os.path.join(venv_path, "bin", "pip")
    py_path = os.path.join(venv_path, "bin", "python")
    requirements = os.path.join(target_dir, "requirements.txt")
    pre_commit = os.path.join(target_dir, ".pre-commit-config.yaml")

    try:
        if os.path.exists(pip_path) and os.path.exists(requirements):
            subprocess.run([pip_path, "install", "-r", requirements], check=True)
            logger.info("✅ Installed requirements")

        if not os.path.exists(os.path.join(target_dir, ".git")):
            subprocess.run(["git", "init"], cwd=target_dir, check=True)
            logger.info("✅ Initialized Git repository")

        if os.path.exists(pre_commit) and os.path.exists(py_path):
            subprocess.run(
                [".venv/bin/python", "-m", "pre_commit", "install"],
                cwd=target_dir,
                check=True,
            )
            logger.info("✅ pre-commit installed and hooks set")
        else:
            logger.warning("⚠️ Missing pre-commit config or Python executable")

    except Exception as e:
        logger.error(f"❌ Error during post-install: {e}")
