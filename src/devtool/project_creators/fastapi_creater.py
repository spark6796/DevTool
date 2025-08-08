import subprocess
from pathlib import Path
import shutil
import os

template_dir = Path(__file__).parent.parent / "templates" / "fastapi"

class FastApiCreator:

    @staticmethod
    def create(
        name: str,
        project_directory: Path
    ) -> subprocess.CompletedProcess:
        project_directory = project_directory / name

        shutil.copytree(template_dir, project_directory)
        
        result1 = subprocess.run(
                ["uv", "init", '--app'],
                check=True,
                capture_output=True,
                shell=True,
                cwd=name,
                text=True
        )
        
        result2 = subprocess.run(
                ["uv", "add", "fastapi",'--extra', "standard"],
                check=True,
                capture_output=True,
                shell=True,
                cwd=name,
                text=True
        )
        
        os.remove(project_directory/'main.py')

        return result2