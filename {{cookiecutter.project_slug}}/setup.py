"""Allows for package installation."""

from distutils.core import setup

setup(
    name="{{cookiecutter.project_name}}",
    version="{{cookiecutter.version}}",
    description="{{cookiecutter.project_short_description}}",
    author="{{cookiecutter.full_name}}",
    author_email="{{cookiecutter.email}}",
)
