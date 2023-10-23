"""
File in charge of allowing you to play the game Snake in your terminal
"""

from time import sleep
from random import randint
# Import the dependencies from asciimatics that are required to create a plain
from asciimatics_overlay_ov import AsciimaticsOverlay
import asciimatics.screen as SCR
import asciimatics.exceptions as EXC
import asciimatics.event as EVE
import asciimatics.renderers as REN
import asciimatics.widgets as WID
import asciimatics.scene as SCE
import asciimatics.effects as EFF
import asciimatics.paths as PAT


class SnakeTUI(AsciimaticsOverlay):
    """ The class for the snake game """

    def __init__(self, win: int = 0, loose: int = 1, error: int = 84) -> None:
        # status game
        self.win = win
        self.success = win
        self.loose = loose
        self.error = error
        # Window functions
        self.screen_main = SCR.Screen
        self.current_event = EVE.Event
        # ---- Binder class ----
        super(AsciimaticsOverlay, self).__init__(
            self.screen_main,
            self.current_event
        )
        # Plyer data (pos)
        self.player_position_x = 0
        self.player_position_y = 0
        # Plyer data (direction)
        self.direction_x = 0
        self.direction_y = 0
        # Plyer data (symbol)
        self.player_character = "*"
        # Plyer data (colour)
        self.player_head_colour = self.colour_yellow
        self.player_head_background_colour = self.colour_default
        self.player_colour = self.colour_green
        self.player_background_colour = self.colour_default
        # Plyer data (speed)
        self.player_speed = 1
        # Plyer data (score)
        self.player_score = 0
        # screen border y
        self.screen_border_y = 5
        # screen border x
        self.screen_border_x = 0
        # Player data (body position)
        # info node
        self.character_node = "character"
        self.position_x_node = "posx"
        self.position_y_node = "posy"
        self.colour_foreground_node = "colour"
        self.colour_background_node = "bg"
        self.player_body_position = [
            {
                self.character_node: self.player_character,
                self.position_x_node: self.player_position_x,
                self.position_y_node: self.player_position_y,
                self.colour_foreground_node: self.player_head_colour,
                self.colour_background_node: self.player_head_background_colour
            }
        ]
        self.screens = []
        # ---- Apple info ----
        self.apple_character = "@"
        self.apple_colour = self.colour_red
        self.apple_background_colour = self.colour_default
        self.apple_position_x = 0
        self.apple_position_y = 0
        self.has_been_eaten = False
        # ---- Game status ----
        self.game_over = False

    def _get_key(self) -> None:
        """ Get the key pressed by the user """
        self.current_event = self.screen_main.get_key()

    def _action_arrow_down(self) -> None:
        """ Change the direction of the player to down """
        self.direction_x = 0
        self.direction_y = self.player_speed

    def _action_arrow_up(self) -> None:
        """ Change the direction of the player to up """
        self.direction_x = 0
        self.direction_y = self.player_speed * (-1)

    def _action_arrow_left(self) -> None:
        """ Change the direction of the player to the left """
        self.direction_x = self.player_speed * (-1)
        self.direction_y = 0

    def _action_arrow_right(self) -> None:
        """ Change the direction of the player to the right """
        self.direction_x = self.player_speed
        self.direction_y = 0

    def _update_direction(self) -> None:
        """ Update the direction of the player """
        if self.is_it_this_key(self.current_event, self.screen_main.KEY_DOWN) is True:
            self._action_arrow_down()
        elif self.is_it_this_key(self.current_event, self.screen_main.KEY_UP) is True:
            self._action_arrow_up()
        elif self.is_it_this_key(self.current_event, self.screen_main.KEY_LEFT) is True:
            self._action_arrow_left()
        elif self.is_it_this_key(self.current_event, self.screen_main.KEY_RIGHT) is True:
            self._action_arrow_right()

    def _update_map(self) -> None:
        """ Update the map """
        if self.game_over is False:
            self._move_player()

            self.player_body_position.append(
                {
                    self.character_node: self.player_character,
                    self.position_x_node: self.player_position_x,
                    self.position_y_node: self.player_position_y,
                    self.colour_foreground_node: self.player_head_colour,
                    self.colour_background_node: self.player_head_background_colour
                }
            )
            self.player_body_position[-2][self.colour_foreground_node] = self.player_colour
            self.player_body_position[-2][self.colour_background_node] = self.player_background_colour
            self.player_body_position.pop(0)

    def _place_apple_randomly(self) -> None:
        """ Place the apple randomly on the map  """
        if self.has_been_eaten is True:
            prev_x = self.apple_position_x
            prev_y = self.apple_position_y
            self.apple_position_x = randint(
                0,
                (self.screen_main.width - self.screen_border_x - 1)
            )
            self.apple_position_y = randint(
                0,
                (self.screen_main.height - self.screen_border_y - 1)
            )
            if self.apple_position_x == prev_x and self.apple_position_y == prev_y:
                if (randint(0, 10) % 2) == 1:
                    self.apple_position_x += 1
                else:
                    self.apple_position_y += 1

    def _is_apple_eaten(self) -> None:
        """ Check if the apple has been eaten """
        if self.game_over is False:
            if self.player_position_x == self.apple_position_x and self.player_position_y == self.apple_position_y:
                self.has_been_eaten = True
                self.player_score += 1
                self._place_apple_randomly()
                self.player_body_position.append(
                    {
                        self.character_node: self.player_character,
                        self.position_x_node: (self.player_position_x - self.direction_x),
                        self.position_y_node: (
                            self.player_position_y - self.direction_y
                        )
                    }
                )
            else:
                self.has_been_eaten = False

    def _move_player(self) -> None:
        """ Move the player """
        if self.player_position_x == 0 and self.direction_x < 0:
            self.player_position_x = self.screen_main.width - 1
        elif self.player_position_x == self.screen_main.width - self.screen_border_x - 1 and self.direction_x > 0:
            self.player_position_x = 0
        else:
            self.player_position_x += self.direction_x

        if self.player_position_y == 0 and self.direction_y < 0:
            self.player_position_y = self.screen_main.height - 1
        elif self.player_position_y == self.screen_main.height - self.screen_border_y - 1 and self.direction_y > 0:
            self.player_position_y = 0
        else:
            self.player_position_y += self.direction_y

    def _has_bitten_itself(self) -> bool:
        """ Check if the player has bitten itself """
        if self.has_been_eaten is True:
            return False
        if len(self.player_body_position) > 1:
            node = self.player_body_position
            for index in range(0, (len(self.player_body_position) - 2), 1):
                if node[index]["posx"] == self.player_position_x and node[index]["posy"] == self.player_position_y:
                    return True
        return False

    def _game_over_message(self) -> int:
        """ Display the game over message """
        self.screen_main.print_at(
            "Game over !",
            0,
            0,
            colour=self.colour_red,
            bg=self.colour_default
        )
        self.screen_main.print_at(
            f"Your score is {self.player_score}",
            0,
            1,
            colour=self.colour_red,
            bg=self.colour_default
        )
        self.screen_main.refresh()
        sleep(3)
        return self.success

    def _mainloop(self) -> int:
        """ The main loop of the game """
        cont = True
        progress = 0
        self.has_been_eaten = True
        self._place_apple_randomly()
        while cont is True:
            self._get_key()
            self._update_direction()
            self._update_map()
            self.screen_main.print_at(f"progress = {progress}", 0, 0)
            self.screen_main.print_at(
                f"posx = {self.player_position_x}, posy = {self.player_position_y}, aposx = {self.apple_position_x} aposy = {self.apple_position_y}", 0, 1)
            self.screen_main.print_at(f"keys = {self.current_event}", 0, 2)
            self.screen_main.print_at(
                f"screen dimensions = {self.get_screen_dimensions()}",
                0,
                3
            )
            self.screen_main.print_at(
                f"player_score = {self.player_score}",
                0,
                4
            )
            self.mvprintw_colour(
                self.apple_character,
                (self.apple_position_x + self.screen_border_x),
                (self.apple_position_y + self.screen_border_y),
                colour=self.apple_colour,
                bg=self.apple_background_colour
            )
            self.print_array_cloud_points(
                self.player_body_position,
                iposx=self.screen_border_x,
                iposy=self.screen_border_y,
                colour=self.player_colour,
                bg=self.player_background_colour
            )
            if self._has_bitten_itself() is True:
                cont = False
                self.game_over = True
                if self._game_over_message() == self.success:
                    continue
                else:
                    return self.success
                # break
            if self.current_event is not None:
                if self.is_it_this_key(self.current_event, "q") is True:
                    cont = False
                    break
            self.screen_main.refresh()
            sleep(0.2)
            self._is_apple_eaten()
            self.screen_main.clear()
            progress += 1
        return self.success

    def main(self, screen: SCR.Screen) -> int:
        """ The main function of the class """
        self.screens.append(screen)
        self.screen_main = screen
        self._get_key()
        self.update_initial_pointers(self.current_event, self.screen_main)
        return self._mainloop()

    def run(self) -> int:
        """ The function in charge of starting the game """
        return SCR.Screen.wrapper(self.main)

    def help(self) -> int:
        """ Print the help of the game """
        return self.success


# from random import randint
# from asciimatics.screen import Screen

# def demo(screen):
#     while True:
#         screen.print_at('Hello world!',
#                         randint(0, screen.width), randint(0, screen.height),
#                         colour=randint(0, screen.colours - 1),
#                         bg=randint(0, screen.colours - 1))
#         ev = screen.get_key()
#         if ev in (ord('Q'), ord('q')):
#             return
#         screen.refresh()

# Screen.wrapper(demo)

if __name__ == "__main__":
    snake_tui = SnakeTUI()
    snake_tui.run()
