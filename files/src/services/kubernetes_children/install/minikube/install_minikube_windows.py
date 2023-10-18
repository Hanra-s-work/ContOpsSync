"""
File in charge of containing the class that will install kind for Windows distributions.
"""

import os
import display_tty
import requests
from tqdm import tqdm
from tty_ov import TTY


class InstallMinikubeWindows:
    """ The class in charge of installing kind for Windows """

    def __init__(self, tty: TTY, success: int = 0, err: int = 84, error: int = 84) -> None:
        self.tty = tty
        self.success = success
        self.err = err
        self.error = error
        self.print_on_tty = self.tty.print_on_tty
        self.run = self.tty.run_command

    def is_minikube_installed(self) -> bool:
        """ Returns true if minikube is installed """
        self.print_on_tty(
            self.tty.info_colour,
            "Checking if minikube is installed:"
        )
        self.tty.current_tty_status = self.run(
            [
                "minikube",
                "version",
                ">nul",
                "2>nul"
            ]
        )
        if self.tty.current_tty_status != self.success:
            self.print_on_tty(self.tty.error_colour, "[KO]\n")
            return False
        self.print_on_tty(self.tty.success_colour, "[OK]\n")
        self.tty.current_tty_status = self.success
        return True

    def main(self) -> int:
        """ The main function of the class """
        return self.success

    def test_class_install_minikube_windows(self) -> None:
        """ Test the class install minikube windows """
        self.print_on_tty(
            self.tty.info_colour,
            "This is a test message from the install minikube Windows class\n"
        )
