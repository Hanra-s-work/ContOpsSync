"""
File in charge of containing the class that will install k3s for macos distributions.
"""

import os
import display_tty
import requests
from tqdm import tqdm
from tty_ov import TTY


class InstallK3sMac:
    """ The class in charge of installing k3s for linux """

    def __init__(self, tty: TTY, success: int = 0, err: int = 84, error: int = 84) -> None:
        self.tty = tty
        self.success = success
        self.err = err
        self.error = error
        self.print_on_tty = self.tty.print_on_tty
        self.run = self.tty.run_command
        # ---- The Disp option ----
        self.disp = display_tty.IDISP
        self.disp.toml_content["PRETTIFY_OUTPUT"] = False
        self.disp.toml_content["PRETTY_OUTPUT_IN_BLOCS"] = False
        # ---- k3s token file ----
        self.k3s_token_file = "/var/lib/rancher/k3s/server/node-token"
        # ---- k3s token save file ----
        self.token_save_file = "/tmp/k3s_token.txt"

    def main(self) -> int:
        """ The main function of the class """
        return self.success

    def is_k3s_installed(self) -> bool:
        """ Returns true if k3s is installed """
        self.print_on_tty(
            self.tty.info_colour,
            "Checking if k3s is installed:"
        )
        self.tty.current_tty_status = self.run(
            [
                "k3s",
                "--version",
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

    def get_k3s_token(self) -> int:
        """ Get the master token for k3s """
        self.print_on_tty(
            self.tty.info_colour,
            "Getting the k3s master token:\n"
        )
        self.tty.current_tty_status = self.run(
            [
                "sudo",
                "cat",
                self.k3s_token_file
            ]
        )
        self.print_on_tty(
            self.tty.info_colour,
            "K3s master token status: "
        )
        if self.tty.current_tty_status != self.tty.success:
            self.print_on_tty(self.tty.error_colour, "[KO]\n")
            return self.error
        self.print_on_tty(self.tty.info_colour, "")
        self.disp.inform_message(
            [
                f"Saving the token to : {self.token_save_file}"
            ]
        )
        status = self.run(
            [
                "sudo",
                "cat",
                self.k3s_token_file,
                f">{self.token_save_file}",
                "2>/dev/null"
            ]
        )
        self.print_on_tty(
            self.tty.info_colour,
            "Saving the token status: "
        )
        if status != self.success:
            self.print_on_tty(self.tty.error_colour, "[KO]\n")
            return self.error
        self.print_on_tty(self.tty.success_colour, "[OK]\n")
        return self.success

    def test_class_install_k3s_mac(self) -> None:
        """ Test the class install k3s MacOS """
        self.print_on_tty(
            self.tty.info_colour,
            "This is a test message from the install k3s MacOS class"
        )
