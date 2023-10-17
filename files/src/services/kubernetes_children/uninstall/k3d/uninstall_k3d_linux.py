"""
File in charge of containing the class that will install k3d for linux distributions.
"""

from os.path import exists, isfile
import display_tty
from tty_ov import TTY


class UninstallK3dLinux:
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
        # ---- File rights ----
        self.edit_mode = "w"
        self.encoding = "utf-8"
        self.newline = "\n"
        # ---- k3d uninstall file ----
        self.k3d_binary = "/usr/local/bin/k3d"
        self.k3d_uninstall_file = "/usr/local/bin/k3d-uninstall.sh"
        self.k3d_agent_uninstall_file = "/usr/local/bin/k3d-agent-uninstall.sh"

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

    def _file_exists(self, file: str) -> bool:
        """ Returns true if the file exists """
        self.print_on_tty(
            self.tty.info_colour,
            f"Checking if the file ({file}) exists:"
        )
        if exists(file) is False:
            self.print_on_tty(self.tty.error_colour, "[KO]\n")
            return False
        if isfile(file) is False:
            self.print_on_tty(self.tty.error_colour, "[KO]\n")
            return False
        self.print_on_tty(self.tty.success_colour, "[OK]\n")
        return True

    def _is_k3d_installed(self) -> bool:
        """ Returns true if k3d is installed """
        self.print_on_tty(
            self.tty.info_colour,
            "Checking if k3d is installed:"
        )
        self.tty.current_tty_status = self.run(
            [
                "k3d",
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

    def _uninstall_for_aur(self) -> int:
        """ Uninstall k3d for aur """
        self.print_on_tty(
            self.tty.info_colour,
            "Uninstalling k3d for aur:"
        )
        self.tty.current_tty_status = self.run(
            [
                "yay",
                "-R",
                "k3d-bin"
            ]
        )
        self.print_on_tty(
            self.tty.info_colour,
            "Aur k3d uninstallation status:"
        )
        if self.tty.current_tty_status != self.tty.success:
            self.print_on_tty(self.tty.error_colour, "[KO]\n")
            return self.tty.error
        self.print_on_tty(self.tty.success_colour, "[OK]\n")
        return self.tty.success

    def _uninstall_for_brew(self) -> int:
        """ Uninstall k3d for brew """
        self.print_on_tty(
            self.tty.info_colour,
            "Uninstalling k3d for brew:"
        )
        self.tty.current_tty_status = self.run(
            [
                "brew",
                "uninstall",
                "k3d"
            ]
        )
        self.print_on_tty(
            self.tty.info_colour,
            "Brew k3d uninstallation status:"
        )
        if self.tty.current_tty_status != self.tty.success:
            self.print_on_tty(self.tty.error_colour, "[KO]\n")
            return self.tty.error
        self.print_on_tty(self.tty.success_colour, "[OK]\n")
        return self.tty.success

    def _manual_uninstallation(self) -> int:
        """ Remove k3d if it was installed manually """
        self.print_on_tty(
            self.tty.info_colour,
            "Checking if k3d was installed manually:"
        )
        if self._file_exists(self.k3d_binary) is True:
            self.print_on_tty(
                self.tty.info_colour,
                "Uninstalling k3d program:"
            )
            self.tty.current_tty_status = self.run(
                [
                    "sudo",
                    "rm",
                    "--recursive",
                    "--verbose",
                    "--force",
                    "--no-clobber",
                    self.k3d_binary
                ]
            )
            self.print_on_tty(
                self.tty.info_colour,
                "Manual uninstallation status:"
            )
            if self.tty.current_tty_status != self.tty.success:
                self.print_on_tty(self.tty.error_colour, "[KO]\n")
                return self.tty.error
            self.print_on_tty(self.tty.success_colour, "[OK]\n")
            return self.tty.success

        if self._file_exists(self.k3d_agent_uninstall_file) is True:
            self.print_on_tty(
                self.tty.info_colour,
                "Uninstalling k3d manually:"
            )
            self.tty.current_tty_status = self.run(
                [
                    "sudo",
                    self.k3d_agent_uninstall_file
                ]
            )
            self.print_on_tty(
                self.tty.info_colour,
                "manual uninstallation status:"
            )
            if self.tty.current_tty_status != self.tty.success:
                self.print_on_tty(self.tty.error_colour, "[KO]\n")
                return self.tty.error
            self.print_on_tty(self.tty.success_colour, "[OK]\n")
            return self.tty.success

        if self._file_exists(self.k3d_uninstall_file) is True:
            self.print_on_tty(
                self.tty.info_colour,
                "Uninstalling k3d manually:"
            )
            self.tty.current_tty_status = self.run(
                [
                    "sudo",
                    self.k3d_uninstall_file
                ]
            )
            self.print_on_tty(
                self.tty.info_colour,
                "manual uninstallation status:"
            )
            if self.tty.current_tty_status != self.tty.success:
                self.print_on_tty(self.tty.error_colour, "[KO]\n")
                return self.tty.error
            self.print_on_tty(self.tty.success_colour, "[OK]\n")
            return self.tty.success
        self.print_on_tty(
            self.tty.info_colour,
            "manual uninstallation status:"
        )
        self.print_on_tty(self.tty.error_colour, "[KO]\n")
        return self.tty.error

    def main(self) -> int:
        """ The main function of the class """
        self.print_on_tty(self.tty.info_colour, "Uninstalling k3d:")
        if self._manual_uninstallation() != self.success:
            if self._has_yay() is True:
                status = self._uninstall_for_aur()
                if status == self.success:
                    return status
            if self._has_brew() is True:
                status = self._uninstall_for_brew()
                if status == self.success:
                    return status
        return self.success

    def test_class_uninstall_k3d_linux(self) -> None:
        """ Test the class uninstall k3d linux """
        self.print_on_tty(
            self.tty.info_colour,
            "This is a test message from the uninstall k3d Linux class\n"
        )
