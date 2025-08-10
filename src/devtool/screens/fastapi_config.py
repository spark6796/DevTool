import threading
from pathlib import Path

from textual.app import ComposeResult
from textual.containers import Horizontal, Vertical
from textual.screen import Screen
from textual.widgets import Button, Select, Static

from devtool.project_creators.fastapi_creater import FastApiCreator
from devtool.config import FASTAPI_TITLE

class FastApiConfigScreen(Screen):

    def __init__(self, project_name: str, project_directory: Path):
        super().__init__()
        self.project_name = project_name
        self.project_directory = project_directory

    def compose(self) -> ComposeResult:

        with Vertical(classes="options-group"):
            yield Static(
                FASTAPI_TITLE,
                classes="config-title",
            )
            yield Static("Package Manager:", classes="field-label")
            yield Select(
                [
                    ("uv", "uv"),
                ],
                id="package_manager",
                prompt="Select Package manager",
                value="uv",
                disabled=True,
                classes="field-select",
            )

            with Horizontal(classes="options-buttons"):
                yield Button("Create Project", variant="success", id="create_fastapi")
                yield Button("Back", variant="default", id="back")

    def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == "back":
            self.app.pop_screen()

        elif event.button.id == "create_fastapi":

            self.app.notify(f"🚀 Creating FastApi app: {self.project_name}...")

            def runner(name: str, directory: Path):
                result = FastApiCreator.create(name, directory)
                if result != 0:
                    error_msg = f"❌ Error creating project: {str(result.stderr)}"
                    self.app.call_from_thread(
                        self.app.notify, error_msg, severity="error"
                    )

            thread = threading.Thread(
                target=runner,
                args=[self.project_name, self.project_directory],
                daemon=True,
            )
            thread.start()

            final_path = Path(self.project_directory) / self.project_name

            self.app.notify(
                f"✅ FastApi project '{self.project_name}' created successfully! at {final_path}"
            )

            self.app.pop_screen()
            self.app.pop_screen()
