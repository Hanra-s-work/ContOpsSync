"""
File in charge of containing the class that will install k3d for macos distributions.
"""

import os
import display_tty
import requests
from tqdm import tqdm
from tty_ov import TTY


class InstallK3dMac:
    """ The class in charge of installing k3d for linux """

    def __init__(self, tty: TTY, success: int = 0, err: int = 84, error: int = 84) -> None:
        self.tty = tty
        self.success = success
        self.err = err
        self.error = error
        self.print_on_tty = self.tty.print_on_tty

    def main(self) -> int:
        """ The main function of the class """
        return self.success

    def is_k3d_installed(self) -> bool:
        """ Returns true if k3d is installed """
        self.print_on_tty(
            self.tty.info_colour,
            "Checking if k3d is installed:\n"
        )
        self.tty.current_tty_status = self.run(
            [
                "k3d",
                "--version",
                ">/dev/null",
                "2>/dev/null"
            ]
        )
        self.print_on_tty(
            self.tty.info_colour,
            "K3d status: "
        )

        if self.tty.current_tty_status != self.tty.success:
            self.print_on_tty(self.tty.error_colour, "[KO]\n")
            return False
        self.print_on_tty(self.tty.success_colour, "[OK]\n")
        self.tty.current_tty_status = self.tty.success
        return True

    def test_class_install_k3d_mac(self) -> None:
        """ Test the class install k3d MacOS """
        self.print_on_tty(
            self.tty.info_colour,
            "This is a test message from the install k3d MacOS class\n"
        )
