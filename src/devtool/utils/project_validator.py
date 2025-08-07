import os
from pathlib import Path


def validate_project(name: str, project_type: str, directory: Path) -> str | None:
    if not name:
        return ("Please enter a project name!",)

    if not project_type:
        return "Please select a project type!"

    if not directory:
        return "Please enter a directory path!"

    if name in os.listdir(directory):
        return f"There is already a directory named: {name}"

    if not os.path.exists(directory):
        return f"Directory does not exist: {directory}"

    if not os.access(directory, os.W_OK):
        return f"No write permission for: {directory}"
