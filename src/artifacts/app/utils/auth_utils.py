# app/utils/auth_utils.py
import base64
import json
import logging
from datetime import timedelta
from functools import wraps
from http import HTTPStatus
from typing import Any, Optional

from flask import Flask, g, request
from flask_httpauth import HTTPBasicAuth
from flask_jwt_extended import (
    JWTManager,
    create_access_token,
    get_jwt_identity,
    verify_jwt_in_request,
)
from flask_login import login_user

from app.models import db
from app.models.user import User, UserRole


# Logging setup
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


# Auth instances
basic_auth = HTTPBasicAuth()
jwt_auth = JWTManager()


def init_jwt(app: Flask) -> None:
    """Initialize JWT manager with the Flask app."""
    jwt_auth.init_app(app)


def generate_token(user: User) -> str:
    """Generate a JWT token for the given user."""
    user_data = json.dumps(user.to_dict())
    expires = timedelta(days=1)
    return create_access_token(identity=user_data, expires_delta=expires)


def get_user_metadata_from_basic_auth(auth_header: str) -> tuple[str, str]:
    """Decode Basic Auth header into username and password."""
    try:
        scheme, base64_credentials = auth_header.split(" ")
        decoded = base64.b64decode(base64_credentials).decode("utf-8")
        username, password = decoded.split(":")
        return username, password
    except Exception:
        raise ValueError("Invalid Basic Auth header format")


def verify_user_basic(username: str, password: str) -> Optional[User]:
    """Authenticate user via basic auth."""
    user = User.query.filter_by(username=username).first()

    if user and User.check_password(user.password, password):
        login_user(user)
        g.current_user = {
            "username": user.username,
            "user_id": user.id,
        }
        return user

    return None


def verify_user_jwt() -> Optional[User]:
    """Authenticate user via JWT token."""
    verify_jwt_in_request()
    user_identity = json.loads(get_jwt_identity())
    user = User.load_user(user_identity.get("user_id"))

    if user:
        login_user(user)
        g.current_user = {
            "username": user.username,
            "user_id": user.id,
        }
        return user

    return None


def auth_required(allowed_roles: list[UserRole] | None):
    """
    Decorator to protect routes with JWT or Basic Auth,
    and optional role-based authorization.
    """

    def decorator(func: Any):
        @wraps(func)
        def wrapper(*args, **kwargs) -> Any:
            auth_header = request.headers.get("Authorization")

            if not auth_header:
                return {
                    "message": "Missing Authorization header"
                }, HTTPStatus.UNAUTHORIZED

            if auth_header.startswith("Bearer "):
                user = verify_user_jwt()
            elif auth_header.startswith("Basic "):
                try:
                    username, password = get_user_metadata_from_basic_auth(auth_header)
                    user = verify_user_basic(username, password)
                except ValueError:
                    return {
                        "message": "Invalid Basic Auth header"
                    }, HTTPStatus.UNAUTHORIZED
            else:
                return {
                    "message": "Invalid Authorization scheme"
                }, HTTPStatus.UNAUTHORIZED

            if not user:
                return {"message": "Invalid credentials"}, HTTPStatus.UNAUTHORIZED

            # Role check
            if allowed_roles and user.role not in allowed_roles:
                return {
                    "message": "You do not have permission to access this resource"
                }, HTTPStatus.FORBIDDEN

            return func(*args, **kwargs)

        return wrapper

    return decorator
