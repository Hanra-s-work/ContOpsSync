"""
File in charge of containing the class that will uninstall kubectl for linux distributions.
"""

import os
from platform import machine, platform
import display_tty
import requests
from tqdm import tqdm
from tty_ov import TTY


class UninstallKubectlLinux:
    """ The class in charge of uninstalling kubernetes for linux """

    def __init__(self, tty: TTY, success: int = 0, err: int = 84, error: int = 84) -> None:
        # ---- System Codes ----
        self.success = success
        self.err = err
        self.error = error
        # ---- Parent classes ----
        self.tty = tty
        # ---- TTY rebinds ----
        self.print_on_tty = self.tty.print_on_tty
        self.run = self.tty.run_command
        self.function_help = self.tty.function_help
        # ---- Download options ----
        self.download_options = {
            "choco": False,
            "scoop": False,
            "winget": False
        }
        # ---- The Disp option ----
        self.disp = display_tty.IDISP
        self.disp.toml_content["PRETTIFY_OUTPUT"] = False
        self.disp.toml_content["PRETTY_OUTPUT_IN_BLOCS"] = False

    def _uninstall_kubectl(self) -> int:
        """ Uninstall the kubectl file in the system """
        self.print_on_tty(
            self.tty.info_colour,
            ""
        )
        self.disp.sub_sub_title("Uninstalling Kubernetes")
        status = self.run(
            [
                "sudo",
                "rm",
                "/usr/local/bin/kubectl"
            ]
        )
        if status != self.tty.success:
            self.print_on_tty(
                self.tty.error_colour,
                "Error uninstalling Kubernetes for Linux\n"
            )
            self.tty.current_tty_status = self.tty.err
            return self.tty.current_tty_status
        self.tty.current_tty_status = status
        return self.tty.current_tty_status

    def _has_snap(self) -> bool:
        """ Returns true if the user has snap [package manager] installed """
        self.print_on_tty(
            self.tty.info_colour,
            "Checking if the user has snap installed:"
        )
        self.tty.current_tty_status = self.run(
            [
                "snap",
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

    def _has_brew(self) -> bool:
        """ Returns true if the user has brew [package manager] installed """
        self.print_on_tty(
            self.tty.info_colour,
            "Checking if the user has brew installed:"
        )
        self.tty.current_tty_status = self.run(
            [
                "brew",
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

    def _uninstall_for_snap(self) -> int:
        """ Uninstall Kubectl using snap """
        self.disp.sub_sub_title("Uninstalling Kubectl via Snap")
        status = self.run(
            [
                "sudo",
                "snap",
                "remove",
                "kubectl",
                "--classic"
            ]
        )
        if status != self.tty.success:
            self.print_on_tty(
                self.tty.error_colour,
                "Error uninstalling Kubernetes for Linux, reverting to manual install\n"
            )
            self.tty.current_tty_status = self.tty.err
            return self.tty.current_tty_status
        self.print_on_tty(
            self.tty.success_colour,
            ""
        )
        self.disp.success_message("Uninstalled Kubectl using snap ;-)")
        self.tty.current_tty_status = self.tty.success
        return self.tty.current_tty_status

    def _uninstall_for_brew(self) -> int:
        """ Uninstall Kubectl using brew """
        self.disp.sub_sub_title("Uninstalling Kubectl via Brew")
        status = self.run(
            [
                "sudo",
                "brew",
                "uninstall",
                "kubectl"
            ]
        )
        if status != self.tty.success:
            self.print_on_tty(
                self.tty.error_colour,
                "Error uninstalling Kubectl for Linux, reverting to manual install\n"
            )
            self.tty.current_tty_status = self.tty.err
            return self.tty.current_tty_status
        self.disp.success_message("Uninstalled Kubectl using brew ;-)")
        self.tty.current_tty_status = self.tty.success
        return self.tty.current_tty_status

    def uninstall_kubectl(self) -> int:
        """ Uninstall kubectl for linux """
        self.print_on_tty(self.tty.help_title_colour, "")
        self.disp.title("Downloading Kubernetes for Linux")
        if self._has_snap() is True:
            if self._uninstall_for_snap() == self.success:
                return self.success
        elif self._has_brew() is True:
            if self._uninstall_for_brew() == self.success:
                return self.success
        status = self._uninstall_kubectl()
        if status != self.success:
            self.print_on_tty(
                self.tty.error_colour,
                "Error uninstalling Kubernetes for Linux\n"
            )
            self.tty.current_tty_status = self.tty.error
            return self.tty.current_tty_status

        self.print_on_tty(
            self.tty.success_colour,
            "Kubernetes has successfully been uninstalled\n"
        )
        self.tty.current_tty_status = self.tty.success
        return self.tty.current_tty_status

    def main(self) -> int:
        """ Uninstall kubernetes on Linux """
        return self.uninstall_kubectl()

    def test_class_uninstall_kubectl_linux(self) -> int:
        """ Test the class install kubectl linux """
        self.print_on_tty(
            self.tty.info_colour,
            "This is a test message from the uninstall kubectl linux class\n"
        )
        return 0
