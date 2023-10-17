"""
File in charge of containing the class that will install k3d for Windows distributions.
"""

import os
import display_tty
import requests
from tqdm import tqdm
from tty_ov import TTY


class InstallMicroK8sWindows:
    """ The class in charge of installing k3d for Windows """

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

    def _has_chocolatey(self) -> bool:
        """ Check if chocolatey is installed """
        self.print_on_tty(
            self.tty.info_colour,
            "Checking if the user has chocolatey installed:"
        )
        self.tty.current_tty_status = self.run(
            [
                "choco",
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

    def _install_chocolatey(self) -> int:
        """ Attempt to install chocolatey """
        self.print_on_tty(
            self.tty.info_colour,
            "Attempting to install chocolatey:"
        )
        status = self.super_run(
            [
                "Set-ExecutionPolicy",
                "Bypass",
                "-Scope",
                "Process",
                "-Force;",
                "[System.Net.ServicePointManager]::SecurityProtocol",
                "=",
                "[System.Net.ServicePointManager]::SecurityProtocol",
                "-bor",
                "3072;",
                "iex",
                "((New-Object",
                "System.Net.WebClient).DownloadString('",
                "https://community.chocolatey.org/install.ps1",
                "'))"
            ]
        )
        self.print_on_tty(
            self.tty.info_colour,
            "Installation status (Chocolatey):"
        )
        if status != self.tty.success:
            self.print_on_tty(self.tty.error_colour, "[KO]\n")
            return self.err
        self.print_on_tty(self.tty.success_colour, "[OK]\n")
        return self.success

    def _install_k3d_via_chocolatey(self) -> int:
        """ Install the k3d package on windows using chocolatey """
        self.print_on_tty(
            self.tty.info_colour,
            "Installing k3d via chocolatey:"
        )
        status = self.super_run(
            [
                "choco",
                "install",
                "k3d",
                "-y"
            ]
        )
        self.print_on_tty(
            self.tty.info_colour,
            "Installation status (k3d):"
        )
        if status != self.tty.success:
            self.print_on_tty(self.tty.error_colour, "[KO]\n")
            return self.err
        self.print_on_tty(self.tty.success_colour, "[OK]\n")
        return self.success

    def main(self) -> int:
        """ The main function of the class """
        if not self._has_chocolatey():
            self.print_on_tty(
                self.tty.info_colour,
                "Chocolatey is not installed on your system, attempting to install it"
            )
            status = self._install_chocolatey()
            if status != self.success:
                self.print_on_tty(
                    self.tty.error_colour,
                    "Error installing chocolatey, please install it before continuing"
                )
                return self.err
        self.print_on_tty(
            self.tty.success_colour,
            ""
        )
        self.disp.sub_sub_title("Installing k3d")
        status = self._install_k3d_via_chocolatey()
        return status

    def test_class_install_microk8s_windows(self) -> None:
        """ Test the class install k3d windows """
        self.print_on_tty(
            self.tty.info_colour,
            "This is a test message from the install k3d Windows class\n"
        )
