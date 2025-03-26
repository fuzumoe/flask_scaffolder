# app/api/hello_schema.py
from flask_restx import fields
from app.api.schemas.base_schema import BaseSchemaAPIModel  # assuming base is here


class HelloSchema(BaseSchemaAPIModel):
    __modelname__ = "Hello"

    name = fields.String(required=True, description="Your name")
    greeting = fields.String(required=False, description="Optional greeting")
