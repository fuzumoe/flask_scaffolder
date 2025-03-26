from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


def bind_app(app: Flask) -> None:
    db.init_app(app)
