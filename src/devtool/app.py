from textual.app import App, ComposeResult
from textual.widgets import Header

from .widgets.home import Home


class DevTools(App):
    CSS_PATH = "app.tcss"

    def compose(self) -> ComposeResult:
        yield Header(show_clock=True)
        yield Home()
