"""
File in charge of containing the class that will uninstall microk8s for linux distributions.
"""

import display_tty
import requests
from tqdm import tqdm
from tty_ov import TTY


class UninstallMicroK8sLinux:
    """ The class in charge of uninstalling k3d for linux """

    def __init__(self, tty: TTY, success: int = 0, err: int = 84, error: int = 84) -> None:
        # ---- tty class ----
        self.tty = tty
        # ---- Status codes ----
        self.success = success
        self.err = err
        self.error = error
        # ---- tty display rebind ----
        self.run = self.tty.run_command
        self.print_on_tty = self.tty.print_on_tty
        self.function_help = self.tty.function_help
        self.super_run = self.tty.run_as_admin
        # ---- The Disp option ----
        self.disp = display_tty.IDISP
        self.disp.toml_content["PRETTIFY_OUTPUT"] = False
        self.disp.toml_content["PRETTY_OUTPUT_IN_BLOCS"] = False

    def _has_yay(self) -> bool:
        """ Returns true if the user has yay [package manager] installed """
        self.print_on_tty(
            self.tty.info_colour,
            "Checking if the user has yay installed:"
        )
        self.tty.current_tty_status = self.run(
            [
                "yay",
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

    def _has_snap(self) -> bool:
        """ Returns true if the user has brew [package manager] installed """
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

    def _uninstall_for_brew(self) -> int:
        """ Uninstall Kubectl using brew """
        self.print_on_tty(
            self.tty.info_colour,
            "Uninstalling microk8s via brew:"
        )
        self.tty.current_tty_status = self.super_run(
            [
                "brew",
                "uninstall",
                "microk8s"
            ]
        )
        self.print_on_tty(
            self.tty.info_colour,
            "Uninstallation status (microk8s):"
        )
        if self.tty.current_tty_status != self.tty.success:
            self.print_on_tty(self.tty.error_colour, "[KO]\n")
            return self.err
        self.print_on_tty(self.tty.success_colour, "[OK]\n")
        return self.success

    def _uninstall_for_yay(self) -> int:
        """ Uninstall k3d using yay """
        self.print_on_tty(
            self.tty.info_colour,
            "Uninstalling microk8s via yay:"
        )
        self.tty.current_tty_status = self.super_run(
            [
                "yay",
                "-R",
                "microk8s"
            ]
        )
        self.print_on_tty(
            self.tty.info_colour,
            "Uninstallation status (microk8s):"
        )
        if self.tty.current_tty_status != self.tty.success:
            self.print_on_tty(self.tty.error_colour, "[KO]\n")
            return self.err
        self.print_on_tty(self.tty.success_colour, "[OK]\n")
        return self.success

    def _uninstall_for_snap(self) -> int:
        """ Uninstall micro Microk8s"""
        self.print_on_tty(
            self.tty.info_colour,
            ""
        )
        self.disp.inform_message(["Uninstalling microk8s for Linux via snap"])
        self.super_run(
            [
                "snap",
                "remove",
                "microk8s"
            ]
        )
        self.print_on_tty(
            self.tty.info_colour,
            "Microk8s uninstallation status: "
        )
        if self.tty.current_tty_status != self.tty.success:
            self.print_on_tty(self.tty.error_colour, "[KO]\n")
            return self.err
        self.print_on_tty(self.tty.success_colour, "[OK]\n")
        return self.success

    def main(self) -> int:
        """ The main function of the class """
        if self._has_yay() is True:
            status = self._uninstall_for_yay()
            if status == self.success:
                return status
        if self._has_brew() is True:
            status = self._uninstall_for_brew()
            if status == self.success:
                return status
        if self._has_snap() is True:
            status = self._uninstall_for_snap()
            if status == self.success:
                return status
        self.print_on_tty(
            self.tty.error_colour,
            ""
        )
        self.disp.error_message(
            "No known package manager found, microk8s will thus not bee installed\n"
        )
        self.tty.current_tty_status = self.error
        return self.error

    def test_class_install_microk8s_linux(self) -> None:
        """ Test the class install microk8s linux """
        self.print_on_tty(
            self.tty.info_colour,
            "This is a test message from the install microk8s Linux class"
        )
