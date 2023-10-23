"""
File in charge of grouping the TUI games together
"""
# Third party imports
import asciimatics
# Local application imports
from .sokoban import Sokoban
from .pong import Pong
from .snake import Snake
from .tetris import Tetris
from .pacman import Pacman
from .breakout import Breakout
from .space_invaders import SpaceInvaders


class Games:
    """ The class in charge of gathering the created games """

    def __init__(self):
        self.games = list()
        self._load_game_menu()
        self.win = 0
        self.loose = 1
        self.error = 84

    def _create_game_line(self, game_name: str, game_description: str, game: object) -> dict:
        game_line = dict()
        game_line["name"] = game_name
        game_line["description"] = game_description
        game_line["game"] = game(self.win, self.loose, self.error)
        if hasattr(game_line["game"], "help") is True:
            game_line["help"] = game_line["game"].help
        return game_line

    def _add_game_line_to_choices(self, game_line: dict) -> None:
        self.games.append(game_line)

    def _load_game_menu(self) -> None:
        """ Load the game menu """
        self._add_game_line_to_choices(
            self._create_game_line(
                "Sokoban",
                "Please help me tidy these boxes.",
                Sokoban
            )
        )
        self._add_game_line_to_choices(
            self._create_game_line(
                "Snake",
                "Ouch, don't bite your tail as you grow.",
                Snake
            )
        )
        self._add_game_line_to_choices(
            self._create_game_line("Pong", "Lets play ping pong.", Pong)
        )
        self._add_game_line_to_choices(
            self._create_game_line("Tetris", "How high will you go.", Tetris)
        )
        self._add_game_line_to_choices(
            self._create_game_line("Pacman", "Eat up little child.", Pacman)
        )
        self._add_game_line_to_choices(
            self._create_game_line(
                "Breakout",
                "Let's get rid of all these bricks.",
                Breakout
            )
        )
        self._add_game_line_to_choices(
            self._create_game_line(
                "Space invaders",
                "Please save our planet.",
                SpaceInvaders
            )
        )
