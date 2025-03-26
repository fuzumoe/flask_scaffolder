# === setup.py ===
from setuptools import find_packages, setup

setup(
    name="flask_scaffolder",  # Match the directory and command name
    version="0.1.0",
    description="Flask scaffold CLI",
    author="Your Name",
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        "Jinja2",
    ],
    entry_points={
        "console_scripts": [
            "flask-scaffolder = flask_scaffolder:main",  # Update to match package name
        ]
    },
)
