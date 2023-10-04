"""
File in charge of containing the class that will install kind for linux distributions.
"""

import os
import display_tty
import requests
from tqdm import tqdm
from tty_ov import TTY


class InstallMinikubeLinux:
    """ The class in charge of installing kind for linux """

    def __init__(self, tty: TTY, success: int = 0, err: int = 84, error: int = 84) -> None:
        self.tty = tty
        self.success = success
        self.err = err
        self.error = error
        self.print_on_tty = self.tty.print_on_tty

    def main(self) -> int:
        """ The main function of the class """
        return self.success

    def test_class_install_minikube_linux(self) -> None:
        """ Test the class install minikube linux """
        self.print_on_tty(
            self.tty.info_colour,
            "This is a test message from the install minikube Linux class"
        )
