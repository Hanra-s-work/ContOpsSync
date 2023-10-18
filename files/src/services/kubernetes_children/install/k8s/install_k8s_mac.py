"""
File in charge of containing the class that will install k8s for macos distributions.
"""

import os
import display_tty
import requests
from tqdm import tqdm
from tty_ov import TTY


class InstallK8sMac:
    """ The class in charge of installing k8s for linux """

    def __init__(self, tty: TTY, success: int = 0, err: int = 84, error: int = 84) -> None:
        self.tty = tty
        self.success = success
        self.err = err
        self.error = error
        self.print_on_tty = self.tty.print_on_tty
        self.run = self.tty.run_command

    def main(self) -> int:
        """ The main function of the class """
        self.print_on_tty(
            self.tty.info_colour,
            "The installation script is yet to come for macs."
        )
        return self.success

    def is_k8s_installed(self) -> bool:
        """ Returns true if k8s is installed """
        self.print_on_tty(
            self.tty.info_colour,
            "Checking if k8s is installed:"
        )
        self.tty.current_tty_status = self.run(
            [
                "kubectl",
                "version",
                "--output=yaml",
                ">/dev/null",
                "2>/dev/null"
            ]
        )
        if self.tty.current_tty_status != self.tty.success:
            self.print_on_tty(self.tty.error_colour, "[KO]\n")
            return False
        self.print_on_tty(self.tty.success_colour, "[OK]\n")
        self.tty.current_tty_status = self.tty.success
        return True

    def test_class_install_k8s_mac(self) -> None:
        """ Test the class install k8s MacOS """
        self.print_on_tty(
            self.tty.info_colour,
            "This is a test message from the install k8s MacOS class\n"
        )
