import threading
from pathlib import Path

from textual.app import ComposeResult
from textual.containers import Horizontal, Vertical
from textual.screen import Screen
from textual.widgets import Button, Checkbox, Select, Static

from devtool.config import react_addons, REACT_TITLE
from devtool.project_creators.react_creator import ReactCreator


class ReactConfigScreen(Screen):

    def __init__(self, project_name: str, project_directory: Path):
        super().__init__()
        self.project_name = project_name
        self.project_directory = project_directory

    def compose(self) -> ComposeResult:

        with Vertical(classes="options-group"):
            yield Static(
                REACT_TITLE,
                classes="config-title",
            )
            yield Static("Template:", classes="field-label")
            yield Select(
                # Using nextjs as of now will add vite,react raw later..
                [
                    ("Next.js", "nextjs"),
                ],
                id="react_framework",
                prompt="Select framework",
                value="nextjs",
                disabled=True,
            )

            yield Static("TypeScript:", classes="field-label")
            yield Select(
                [
                    ("Yes (recommended)", "typescript"),
                    ("No (JavaScript only)", "javascript"),
                ],
                id="typescript_choice",
                prompt="Use TypeScript?",
                value="typescript",
            )

            with Horizontal(classes="options-buttons"):
                yield Button("Create Project", variant="success", id="create_react")
                yield Button("Back", variant="default", id="back")

        with Vertical(classes="addon-group"):
            yield Static("Options:", classes="addon-label")
            yield Checkbox(id="eslint", value=True, label="ESLint (linter)")
            yield Checkbox(
                id="tailwindcss", value=True, label="Tailwind CSS (utility-first CSS)"
            )
            yield Checkbox(id="src_directory", value=True, label="Use src/ directory")

            yield Checkbox(
                id="app_router", value=True, label="App Router (Next.js recommended)"
            )
            yield Checkbox(
                id="turbopack", value=False, label="Turbopack for development"
            )

    def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == "back":
            self.app.pop_screen()

        elif event.button.id == "create_react":
            typescript = self.query_one("#typescript_choice", Select).value

            selected_addons = []

            for addon_id in react_addons:
                checkbox = self.query_one(f"#{addon_id}", Checkbox)
                if checkbox.value:
                    selected_addons.append(addon_id)

            self.app.notify(f"🚀 Creating React app: {self.project_name}...")

            thread = threading.Thread(
                target=ReactCreator.create,
                args=[self.project_name, typescript, selected_addons],
                daemon=True,
            )
            thread.start()

            final_path = Path(self.project_directory) / self.project_name

            self.app.notify(
                f"✅ React project '{self.project_name}' created successfully! at {final_path}"
            )

            self.app.notify(
                "Please be patient let the project setup it may take a while...",severity="information"
            )

            self.app.pop_screen()
            self.app.pop_screen()
