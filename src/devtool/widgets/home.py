from textual import on
from textual.app import ComposeResult
from textual.containers import Horizontal, Vertical
from textual.widget import Widget
from textual.widgets import Button
from textual_pyfiglet import FigletWidget

from screens.new_project import NewProjectScreen


class Home(Widget):

    def compose(self) -> ComposeResult:

        yield FigletWidget(
            "DEV TOOLS",
            classes="title",
            font="ansi_shadow",
            animate=True,
            animation_type="gradient",
            justify="center",
            fps=5,
            colors=["lightblue", "grey"],
        )
        with Vertical(classes="menu"):
            with Horizontal(classes="buttons"):
                yield Button("📊 Project Stats", id="stats", variant="primary")
                yield Button("🚀 New Project", id="new_project", variant="success")
                yield Button("⚙  Utilities", id="utils")
                yield Button("✖  Exit", id="exit", variant="error")

    @on(Button.Pressed, "#exit")
    def handle_exit(self, event: Button.Pressed) -> None:
        self.app.exit()

    @on(Button.Pressed, "#stats")
    def handle_stats(self, event: Button.Pressed) -> None:
        self.app.notify("Opening Project Stats...")

    @on(Button.Pressed, "#utils")
    def handle_utils(self, event: Button.Pressed) -> None:
        self.app.notify("Opening utils...")

    @on(Button.Pressed, "#new_project")
    def handle_new(self, event: Button.Pressed) -> None:
        self.app.notify("Creating New Project...")
        self.app.push_screen(NewProjectScreen())
