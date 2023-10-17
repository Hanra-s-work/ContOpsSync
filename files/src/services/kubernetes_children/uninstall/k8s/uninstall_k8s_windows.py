"""
File in charge of containing the class that will install k8s for Windows distributions.
"""

import display_tty
from tty_ov import TTY


class UninstallK8sWindows:
    """ The class in charge of installing k8s for Windows """

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

    def main(self) -> int:
        """ The main function of the class """
        self.print_on_tty(
            self.tty.info_colour,
            "There is no known installation script for installing Kubernetes(k8s) on Windows"
        )
        self.print_on_tty(
            self.tty.info_colour,
            "Please install microk8s when on windows."
        )
        return self.tty.success

    def test_class_uninstall_k8s_windows(self) -> None:
        """ Test the class install k8s windows """
        self.print_on_tty(
            self.tty.info_colour,
            "This is a test message from the install k8s Windows class\n"
        )
