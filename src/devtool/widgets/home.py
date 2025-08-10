from textual import on
from textual.app import ComposeResult
from textual.containers import Horizontal, Vertical
from textual.widget import Widget
from textual.widgets import Button
from textual.widgets import Static


from devtool.screens.new_project import NewProjectScreen
from devtool.screens.stats import StatsScreen
from devtool.config import HOME_TITLE


class Home(Widget):

    def compose(self) -> ComposeResult:

        yield Static(
            HOME_TITLE,
            classes="title",
        )
        with Vertical(classes="menu"):
            with Horizontal(classes="buttons"):
                yield Button("📊 Project Stats", id="stats", variant="primary")
                yield Button("🚀 New Project", id="new_project", variant="success")
                yield Button("✖  Exit", id="exit", variant="error")

    @on(Button.Pressed, "#exit")
    def handle_exit(self, event: Button.Pressed) -> None:
        self.app.exit()

    @on(Button.Pressed, "#stats")
    def handle_stats(self, event: Button.Pressed) -> None:
        self.app.notify("Opening Project Stats...")
        self.app.push_screen(StatsScreen())

    @on(Button.Pressed, "#new_project")
    def handle_new(self, event: Button.Pressed) -> None:
        self.app.notify("Creating New Project...")
        self.app.push_screen(NewProjectScreen())
