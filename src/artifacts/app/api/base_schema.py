# app/api/base_schema.py

from flask_restx import fields, Model, Namespace, Api, reqparse
from werkzeug.datastructures import FileStorage
from http import HTTPStatus


# Wrapper to mark file upload fields (used in query/form data)
class FileField:
    def __init__(self, required=False, help=None, location="files"):
        self.required = required
        self.help = help or "Upload file"
        self.location = location


class BaseSchemaAPIModel:
    def __init__(self, api_or_namespace: Namespace | Api, **kwargs):
        # Use __modelname__ if defined, else fallback to class name
        self.__modelname__ = getattr(
            self.__class__, "__modelname__", self.__class__.__name__
        )
        self._api_or_namespace = (
            api_or_namespace  # Used for .model(), .expect(), .response(), etc.
        )

        self.__fields__ = {}  # Normal RESTX model fields
        self.__file_fields__ = {}  # Special handling for file uploads

        # Collect declared fields and check for tuple mistake
        for name, value in self.__class__.__dict__.items():
            if isinstance(value, tuple):
                raise TypeError(
                    f"Field '{name}' is a tuple. Did you accidentally add a comma?"
                )
            if isinstance(value, fields.Raw):
                self.__fields__[name] = value
            elif isinstance(value, FileField):
                self.__file_fields__[name] = value

        if not self.__fields__ and not self.__file_fields__:
            raise ValueError(f"No fields defined in {self.__modelname__}.")

        # Set attributes from passed-in kwargs (if any)
        for field_name in {**self.__fields__, **self.__file_fields__}:
            setattr(self, field_name, kwargs.get(field_name))

    def as_model(self) -> Model:
        """Registers and returns the RESTX model using the collected fields."""
        return self._api_or_namespace.model(self.__modelname__, self.__fields__)

    def as_queryparser(self) -> reqparse.RequestParser:
        """Creates a query/form parser based on the declared fields and file inputs."""
        parser = reqparse.RequestParser()

        # Add normal fields
        for field_name, field in self.__fields__.items():
            if getattr(field, "readonly", False):
                continue  # Don't allow readonly fields in input
            arg_type = self._resolve_type(field)
            parser.add_argument(
                name=field_name,
                type=arg_type,
                required=getattr(field, "required", False),
                help=f"{field_name} ({arg_type.__name__})",
                location="args",
            )

        # Add file fields
        for field_name, file_field in self.__file_fields__.items():
            parser.add_argument(
                name=field_name,
                type=FileStorage,
                required=file_field.required,
                help=file_field.help,
                location=file_field.location,
            )

        return parser

    # --- Decorator shortcuts for route methods ---

    @property
    def expect(self):
        """@namespace.expect(...) for body model"""
        return self._api_or_namespace.expect(self.as_model())

    @property
    def expect_query(self):
        """@namespace.expect(...) for query or file parser"""
        return self._api_or_namespace.expect(self.as_queryparser())

    def response(self, code=HTTPStatus.OK, message="Success"):
        """@namespace.response(...) shortcut"""
        return self._api_or_namespace.response(code, message)

    def marshal(self, code=HTTPStatus.OK, many=False):
        """@namespace.marshal_with(...) shortcut using this model"""
        return self._api_or_namespace.marshal_with(
            self.as_model(), code=code, as_list=many
        )

    def doc(self, **kwargs):
        """@namespace.doc(...) shortcut for adding Swagger metadata"""
        return self._api_or_namespace.doc(**kwargs)

    def _resolve_type(self, field_obj):
        """Maps RESTX field types to native Python types (for query parser)"""
        type_map = {
            fields.String: str,
            fields.Integer: int,
            fields.Boolean: bool,
            fields.Float: float,
            fields.DateTime: str,
            fields.Raw: str,
            fields.Url: str,
        }
        for field_type, py_type in type_map.items():
            if isinstance(field_obj, field_type):
                return py_type
        return str  # Default fallback type
