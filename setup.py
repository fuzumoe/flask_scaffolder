# my_project/setup.py
from setuptools import setup

setup(
    name="flask-scaffolder",
    version="0.1.0",
    description="Flask scaffold CLI",
    author="Adam Fuzum",
    author_email="fuzumoe@gmail.com",
    package_dir={"": "src"},  # Look for packages in src/
    packages=["flask_scaffolder"],  # Explicitly specify the package
    include_package_data=True,
    install_requires=[
        "Jinja2",
    ],
    entry_points={
        "console_scripts": [
            "flask-scaffolder = flask_scaffolder.cli:main",
        ]
    },
)
