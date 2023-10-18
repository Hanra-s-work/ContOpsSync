"""
File in charge of containing the class that will install k3s for Windows distributions.
"""

import display_tty
from tty_ov import TTY


class InstallK3sWindows:
    """ The class in charge of installing k3s for Windows """

    def __init__(self, tty: TTY, success: int = 0, err: int = 84, error: int = 84) -> None:
        self.tty = tty
        self.success = success
        self.err = err
        self.error = error
        self.print_on_tty = self.tty.print_on_tty
        self.super_run = self.tty.run_as_admin
        self.run = self.tty.run_command
        # ---- The Disp option ----
        self.disp = display_tty.IDISP
        self.disp.toml_content["PRETTIFY_OUTPUT"] = False
        self.disp.toml_content["PRETTY_OUTPUT_IN_BLOCS"] = False

    def is_k3s_installed(self) -> bool:
        """ Returns true if k3s is installed """
        self.print_on_tty(
            self.tty.info_colour,
            "Checking if k3s is installed (Windows):"
        )
        self.tty.current_tty_status = self.run(
            [
                "k3s",
                "--version",
                ">nul",
                "2>nul"
            ]
        )
        if self.tty.current_tty_status != self.tty.success:
            self.print_on_tty(self.tty.error_colour, "[KO]\n")
            return False
        self.print_on_tty(self.tty.success_colour, "[OK]\n")
        self.tty.current_tty_status = self.tty.success
        return True

    def get_k3s_token(self) -> int:
        """ Get the master token for k3s """
        self.print_on_tty(self.tty.info_colour, "")
        self.disp.warning_message(
            "At the time of writing this program, k3s is not natively supported on Windows"
        )
        self.tty.current_tty_status = self.tty.error
        return self.error

    def main(self) -> int:
        """ The main function of the class """
        self.print_on_tty(self.tty.info_colour, "")
        self.disp.warning_message(
            "At the time of writing this program, k3s is not natively supported on Windows"
        )
        self.tty.current_tty_status = self.tty.error
        return self.error

    def test_class_install_k3s_windows(self) -> None:
        """ Test the class install k3s windows """
        self.print_on_tty(
            self.tty.info_colour,
            "This is a test message from the install k3s Windows class\n"
        )
