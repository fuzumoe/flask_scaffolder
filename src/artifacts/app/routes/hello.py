# app/api/routes/hello.py
from flask_restx import Namespace, Resource
from app.api.hello_schema import HelloSchema

path = "/hello"
namespace = Namespace("hello", description="Hello World operations")

hello_schema = HelloSchema(namespace)


@namespace.route("/")
class HelloResource(Resource):
    @hello_schema.expect_model()
    def post(self):
        data = namespace.payload
        name = data.get("name")
        greeting = data.get("greeting", "Hello")
        return {"message": f"{greeting}, {name}!"}
