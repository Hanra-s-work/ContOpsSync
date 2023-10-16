"""
Class in charge of forcing k3s to use Docker when it starts
"""

import display_tty
from tty_ov import TTY


class ForceDockerWindows:
    """ The class in charge of forcing docker for the system """

    def __init__(self, tty: TTY, success: int = 0, err: int = 84, error: int = 84) -> None:
        self.success = success
        self.err = err
        self.error = error
        # ---- The TTY options ----
        self.tty = tty
        self.print_on_tty = self.tty.print_on_tty
        self.super_run = self.tty.run_as_admin
        self.run = self.tty.run_command
        # ---- The Disp option ----
        self.disp = display_tty.IDISP
        self.disp.toml_content["PRETTIFY_OUTPUT"] = False
        self.disp.toml_content["PRETTY_OUTPUT_IN_BLOCS"] = False
        # ---- Filepaths ----
        self.k3s_service_file = "/etc/systemd/system/k3s.service"

    def main(self) -> int:
        """ The main function of the class """
        self.print_on_tty(
            self.tty.info_colour,
            "This option is not yet available for Windows due to k3s not supporting this system."
        )
        return self.success
