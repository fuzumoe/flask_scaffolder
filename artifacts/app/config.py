import os
from dotenv import load_dotenv

# Load environment variables from .env
load_dotenv()


class Config:
    # Core App Settings
    SECRET_KEY = os.getenv("SECRET_KEY", "default-secret-key")
    SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URL", "sqlite:///db.sqlite3")
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # Mail settings
    MAIL_SERVER = os.getenv("MAIL_SERVER", "smtp.example.com")
    MAIL_PORT = int(os.getenv("MAIL_PORT", 587))
    MAIL_USE_TLS = os.getenv("MAIL_USE_TLS", "true").lower() == "true"
    MAIL_USERNAME = os.getenv("MAIL_USERNAME")
    MAIL_PASSWORD = os.getenv("MAIL_PASSWORD")

    # API Settings
    API_TITLE = os.getenv("API_TITLE", "APP")
    API_VERSION = os.getenv("API_VERSION", "1.0")
    API_DESCRIPTION = os.getenv("API_DESCRIPTION", "Some app.")

    # RESTX Auth
    API_AUTHORIZATIONS = {
        "basic": {
            "type": "basic",
            "description": "Basic Authentication - Provide `username:password` in Base64.",
        },
        "jwt": {
            "type": "apiKey",
            "in": "header",
            "name": "Authorization",
            "description": "JWT Authentication - Use `Bearer <JWT>` in the header.",
        },
    }

    # App port from environment
    PORT = int(os.getenv("PORT", 5000))


class DevelopmentConfig(Config):
    DEBUG = True


class TestingConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = "sqlite:///:memory:"


class ProductionConfig(Config):
    DEBUG = False
    TESTING = False


# Dictionary to map config names
config_by_name = dict(dev=DevelopmentConfig, test=TestingConfig, prod=ProductionConfig)


def get_config_name():
    """Get the current config name from environment variable or fallback."""
    return os.getenv("FLASK_CONFIG", "dev")
