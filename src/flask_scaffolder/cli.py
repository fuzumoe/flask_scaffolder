# src/flask_scaffolder/cli.py
import argparse

from flask_scaffolder.core import scaffold_project


def main():
    parser = argparse.ArgumentParser(description="Scaffold a Flask project")
    parser.add_argument(
        "--output",
        default="my_project",
        help="Target directory for the scaffolded project.",
    )
    parser.add_argument("--secret-key", required=True)
    parser.add_argument("--database-uri", required=True)
    parser.add_argument("--flask-app", default="run.py")
    parser.add_argument("--smtp-server", default="")
    parser.add_argument("--smtp-port", type=int, default=587)
    parser.add_argument("--smtp-email", default="")
    parser.add_argument("--smtp-password", default="")
    parser.add_argument("--flask-config", default="dev")
    parser.add_argument("--api-title", default="")
    parser.add_argument("--api-version", type=float, default=1.0)
    parser.add_argument("--api-description", default="")
    args = parser.parse_args()

    context = {
        "SECRET_KEY": args.secret_key,
        "DATABASE_URI": args.database_uri,
        "FLASK_APP": args.flask_app,
        "SMTP_SERVER": args.smtp_server,
        "SMTP_PORT": args.smtp_port,
        "SMTP_EMAIL": args.smtp_email,
        "SMTP_PASSWORD": args.smtp_password,
        "FLASK_CONFIG": args.flask_config,
        "API_TITLE": args.api_title,
        "API_VERSION": args.api_version,
        "API_DESCRIPTION": args.api_description,
    }
    scaffold_project(args.output, context)


if __name__ == "__main__":
    main()
