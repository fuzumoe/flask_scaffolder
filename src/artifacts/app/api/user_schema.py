# app/api/user_schema.py
from flask_restx import fields
from app.schemas.base_schema import BaseSchemaAPIModel

# -------------------- User Models --------------------


class UserModel(BaseSchemaAPIModel):
    __modelname__ = "UserModel"

    id = fields.Integer(readonly=True, description="User ID")
    full_name = fields.String(required=True, description="Full name")
    username = fields.String(required=True, description="Username")
    email = fields.String(required=True, description="Email")
    role = fields.String(required=True, description="User role (e.g., admin, user)")


class UserRequestModel(BaseSchemaAPIModel):
    __modelname__ = "UserRequestModel"

    id = fields.Integer(readonly=True, description="User ID")
    full_name = fields.String(required=True, description="Full name")
    username = fields.String(required=True, description="Username")
    email = fields.String(required=True, description="Email")
    password = fields.String(required=False, description="Password")
    role = fields.String(required=True, description="User role (e.g., admin, user)")


class UserUpdateRequestModel(BaseSchemaAPIModel):
    __modelname__ = "UserUpdateRequestModel"

    full_name = fields.String(required=False, description="Full name")
    email = fields.String(required=False, description="Email")
    password = fields.String(required=False, description="Password")
    role = fields.String(required=False, description="User role (e.g., admin, user)")


class UserLoginModel(BaseSchemaAPIModel):
    __modelname__ = "UserLoginModel"

    username = fields.String(required=True, description="Username")
    password = fields.String(required=True, description="Password")


class UserLoginResponseModel(BaseSchemaAPIModel):
    __modelname__ = "UserLoginResponseModel"

    success = fields.Boolean(required=True)
    token = fields.String(required=True)


class UserResponseModel(BaseSchemaAPIModel):
    __modelname__ = "UserResponseModel"

    success = fields.Boolean()
    data = fields.Nested(UserModel.as_model)  # Must call after instantiation
    total = fields.Integer(required=False)
    pages = fields.Integer(required=False)
    current_page = fields.Integer(required=False)
    per_page = fields.Integer(required=False)


# -------------------- Book Borrow Model --------------------


class BookBorrowModel(BaseSchemaAPIModel):
    __modelname__ = "BookBorrow"

    borrowed_until = fields.Date(
        required=True,
        description="The date until the book is borrowed (format: YYYY-MM-DD)",
        example="2025-04-01",
    )


class UserQueryParams(BaseSchemaAPIModel):
    __modelname__ = "UserQuery"

    page = fields.Integer(required=False, description="Page number for pagination")
    per_page = fields.Integer(required=False, description="Number of items per page")
    full_name = fields.String(required=False, description="Filter by full name")
    username = fields.String(required=False, description="Filter by username")
    email = fields.String(required=False, description="Filter by email")
    role = fields.String(required=False, description="Filter by user role")
