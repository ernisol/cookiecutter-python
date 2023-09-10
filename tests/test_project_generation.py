import os
from contextlib import contextmanager

import pytest
from cookiecutter.utils import rmtree


@contextmanager
def inside_dir(dirpath):
    """Execute code from inside the given directory."""
    old_path = os.getcwd()
    try:
        os.chdir(dirpath)
        yield
    finally:
        os.chdir(old_path)


@contextmanager
def bake_in_temp_dir(cookies, *args, **kwargs):
    """Deletes the tmp directory after project's generation."""
    result = cookies.bake(*args, **kwargs)
    try:
        yield result
    finally:
        rmtree(str(result.project_path))


def test_bake_with_defaults(cookies):
    with bake_in_temp_dir(cookies) as generated_project:
        assert generated_project.project_path.is_dir()
        assert generated_project.exit_code == 0
        assert generated_project.exception is None

        found_toplevel_files = [
            file.name for file in generated_project.project_path.iterdir()
        ]
        expected_files = [
            ".github",
            "project",
            "tests",
            ".gitignore",
            ".pre-commit-config.yaml",
            "CHANGELOG.md",
            "setup.cfg",
            "tox.ini",
        ]
        assert all([file in found_toplevel_files for file in expected_files])


@pytest.mark.parametrize("linter", ["black", "ruff", "ruff-fix"])
def test_lint_baked_project(cookies, linter):
    """Test linter execution on newly generated project."""
    with bake_in_temp_dir(cookies) as generated_project:
        with inside_dir(generated_project.project_path):
            os.system(f"tox -e {linter}")
