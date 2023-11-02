import asciimatics.screen as SCR
from asciimatics.widgets import Frame, Layout, Button
from asciimatics.exceptions import NextScene


class MainMenu(Frame):
    def __init__(self, screen):
        super(MainMenu, self).__init__(
            screen,
            screen.height // 2,
            screen.width // 2,
            has_border=True,
            title="Main Menu"
        )

        layout = Layout([1, 1, 1])  # Define a layout with three columns
        self.add_layout(layout)

        layout.add_widget(Button("Play", self._play))
        layout.add_widget(Button("Options", self._options))
        layout.add_widget(Button("Quit", self._quit))

        self.fix()

    def _play(self):
        raise NextScene("Game Scene")

    def _options(self):
        raise NextScene("Options Scene")

    def _quit(self):
        raise NextScene("Exit")


def main(screen):
    scenes = [
        MainMenu(screen)
    ]
    screen.play(scenes, stop_on_resize=True)


if __name__ == "__main__":
    SCR.Screen.wrapper(main)
