import shutil
from pathlib import Path

template_dir = Path(__file__).parent.parent / "templates" / "fastapi"


class FastApiCreator:
    @classmethod
    def create(cls, name: str, project_directory: Path) -> None:

        project_path = project_directory / name
        shutil.copytree(template_dir, project_path)
