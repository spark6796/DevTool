import threading
from pathlib import Path

from textual.app import ComposeResult
from textual.containers import Horizontal, Vertical
from textual.screen import Screen
from textual.widgets import Button, Checkbox, Select, Static
from textual_pyfiglet import FigletWidget

from config import svelte_addons
from project_creators.svelte_creator import SvelteCreator


class SvelteConfigScreen(Screen):

    def __init__(self, project_name: str, project_directory: Path):
        super().__init__()
        self.project_name = project_name
        self.project_directory = project_directory

    def compose(self) -> ComposeResult:

        with Vertical(classes="options-group"):
            yield FigletWidget(
                "Svelte",
                classes="config-title",
                font="ansi_shadow",
                animate=True,
                animation_type="gradient",
                justify="center",
                fps=5,
                colors=["red", "orange"],
            )
            yield Static("Template:", classes="field-label")
            yield Select(
                [
                    ("Demo App", "demo"),
                    ("Minimal/Skeleton", "minimal"),
                    ("Library", "library"),
                ],
                id="svelte_template",
                prompt="Select template",
                value="demo",
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
                yield Button("Create Project", variant="success", id="create_svelte")
                yield Button("Back", variant="default", id="back")

        with Vertical(classes="addon-group"):
            yield Static("Add-ons :", classes="addon-label")
            yield Checkbox(id="prettier", value=True, label="Prettier (code formatter)")
            yield Checkbox(id="eslint", value=True, label="ESLint (linter)")
            yield Checkbox(id="vitest", value=False, label="Vitest (unit testing)")
            yield Checkbox(
                id="playwright", value=False, label="Playwright (browser testing)"
            )
            yield Checkbox(
                id="tailwindcss", value=False, label="Tailwind CSS (css framework)"
            )
            yield Checkbox(
                id="sveltekit-adapter",
                value=False,
                label="SvelteKit Adapter (deployment)",
            )
            yield Checkbox(id="drizzle", value=False, label="Drizzle (database orm)")
            yield Checkbox(id="lucia", value=False, label="Lucia (authentication)")
            yield Checkbox(
                id="mdsvex", value=False, label="MDsveX (Markdown in Svelte)"
            )
            yield Checkbox(
                id="paraglide", value=False, label="Paraglide (internationalization)"
            )

    def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == "back":
            self.app.pop_screen()

        elif event.button.id == "create_svelte":
            template = self.query_one("#svelte_template", Select).value
            typescript = self.query_one("#typescript_choice", Select).value

            selected_addons = []

            for addon_id in svelte_addons:
                checkbox = self.query_one(f"#{addon_id}", Checkbox)
                if checkbox.value:
                    selected_addons.append(addon_id)

            self.app.notify(f"🚀 Creating Svelte app: {self.project_name}...")

            thread = threading.Thread(
                target=SvelteCreator.create,
                args=[self.project_name, template, typescript, selected_addons],
                daemon=True,
            )
            thread.start()

            final_path = Path(self.project_directory) / self.project_name

            self.app.notify(
                f"✅ Svelte project '{self.project_name}' created successfully! at {final_path}"
            )

            self.app.pop_screen()
            self.app.pop_screen()
