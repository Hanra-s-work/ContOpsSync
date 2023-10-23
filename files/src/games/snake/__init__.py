"""
File in charge of linking the Snake files
"""

from .snake import SnakeTUI


class Snake:
    """ The Snake game but in your terminal """

    def __init__(self, win: int = 0, loose: int = 1, error: int = 84) -> None:
        self.snake_tui = SnakeTUI(win, loose, error)

    def help(self) -> int:
        """ Print the help of the game """
        return self.snake_tui.help()

    def run(self) -> int:
        """ Run the game """
        return self.snake_tui.run()
