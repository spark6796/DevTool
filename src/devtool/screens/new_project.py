import os
import shutil
import subprocess
import threading
import tkinter as tk
from pathlib import Path
from tkinter import filedialog

from textual.app import ComposeResult
from textual.containers import Container, Horizontal
from textual.screen import Screen
from textual.widgets import Button, Input, Select, Static

from devtool.screens.fastapi_config import FastApiConfigScreen
from devtool.screens.react_config import ReactConfigScreen
from devtool.screens.svelte_config import SvelteConfigScreen
from devtool.utils.project_validator import validate_project


class NewProjectScreen(Screen):

    def compose(self) -> ComposeResult:
        current_dir = os.getcwd()

        with Container(classes="form-container"):

            with Container(classes="form-field"):
                yield Static("Project Name:", classes="field-label")
                yield Input(placeholder="Enter project name...", id="project_name")

            with Container(classes="form-field"):
                yield Static("Project Type:", classes="field-label")
                yield Select(
                    [
                        ("React App", "react_app"),
                        ("Svelte App", "svelte_app"),
                        ("FastAPI App", "fastapi_app"),
                    ],
                    id="project_type",
                    prompt="Select project type",
                )

            with Container(classes="form-field"):
                yield Static("Project Directory:", classes="field-label")

                with Horizontal(classes="directory-row"):
                    yield Input(
                        value=current_dir,
                        placeholder="Enter directory path...",
                        id="project_directory",
                    )
                    yield Button("Browse", id="browse_dir", variant="default")

            with Horizontal(classes="form-buttons"):
                yield Button("Create Project", variant="success", id="create")
                yield Button("Cancel", variant="error", id="cancel")

    def open_folder_dialog(self) -> None:

        def select_folder():
            root = tk.Tk()
            root.withdraw()
            root.attributes("-topmost", True)

            current_dir = self.query_one("#project_directory", Input).value

            selected_folder = filedialog.askdirectory(
                title="Select Project Directory", initialdir=current_dir
            )

            if selected_folder:
                self.app.call_from_thread(self.update_directory_input, selected_folder)

            root.destroy()

        thread = threading.Thread(target=select_folder, daemon=True)
        thread.start()

    def update_directory_input(self, directory: str) -> None:

        self.query_one("#project_directory", Input).value = directory
        self.app.notify(f"Selected directory: {directory}")

    def on_button_pressed(self, event: Button.Pressed) -> None:
        button_id = event.button.id

        if button_id == "cancel":
            self.app.pop_screen()

        elif button_id == "browse_dir":
            self.open_folder_dialog()

        elif button_id == "create":

            name = self.query_one("#project_name", Input).value.strip()
            project_type = str(self.query_one("#project_type", Select).value)
            directory = Path(self.query_one("#project_directory", Input).value.strip())

            error_msg = validate_project(name, project_type, directory)

            if error_msg:
                self.app.notify(error_msg, severity="error")
                return

            project_path = Path(directory)

            self.create_project(name, project_type, project_path)

    def check_node_installation(self) -> bool:
        try:
            subprocess.run(
                ["node", "--version"], check=True, stdout=subprocess.DEVNULL, shell=True
            )
            subprocess.run(
                ["npm", "--version"], check=True, stdout=subprocess.DEVNULL, shell=True
            )
            self.app.notify("Node.js and npm are installed.", severity="success")
            return True
        except (subprocess.CalledProcessError, FileNotFoundError):
            self.app.notify(
                "❌ Node.js and npm are required to create React or Svelte projects.",
                severity="error",
            )
            return False
        except Exception as e:
            self.app.notify(
                f"❌ Error checking Node.js installation: {str(e)}", severity="error"
            )
            return False

    def create_project(self, name: str, project_type: str, directory: Path) -> None:
        try:
            original_cwd = os.getcwd()
            os.chdir(directory)

            if project_type in ["react_app", "svelte_app"]:
                has_node = self.check_node_installation()

                if has_node:
                    if project_type == "svelte_app":
                        self.app.push_screen(SvelteConfigScreen(name, directory))
                    else:
                        self.app.push_screen(ReactConfigScreen(name, directory))
                else:
                    self.app.notify(
                        "Using template as Node.js is not installed...",
                        severity="warning",
                    )
                    template_base = Path(__file__).parent.parent / "templates"
                    template_dir = template_base / (
                        "react" if project_type == "react_app" else "svelte"
                    )

                    if not template_dir.exists():
                        self.app.notify(
                            f"❌ Template not found for {project_type}",
                            severity="error",
                        )
                        return

                    project_path = directory / name
                    shutil.copytree(template_dir, project_path)
                    self.app.notify(
                        f"✅ Project created from template at {project_path}",
                        severity="success",
                    )
                    self.app.notify(
                        "⚠️ Install Node.js to use all features: https://nodejs.org",
                        severity="warning",
                    )
                    self.app.pop_screen()

            elif project_type == "fastapi_app":
                self.app.push_screen(FastApiConfigScreen(name, directory))

        except Exception as e:
            os.chdir(original_cwd)
            self.app.notify(f"❌ Error creating project: {str(e)}", severity="error")
