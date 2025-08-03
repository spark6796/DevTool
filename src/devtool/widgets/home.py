from textual.app import ComposeResult
from textual.widget import Widget
from textual_pyfiglet import FigletWidget

class Home(Widget):

    def compose(self) -> ComposeResult:

        yield FigletWidget(
            "DEV TOOLS",
            classes="title",
            font="ansi_shadow",
            animate=True, 
            animation_type="gradient", 
            justify='center', 
            colors=['lightblue','grey']
        )