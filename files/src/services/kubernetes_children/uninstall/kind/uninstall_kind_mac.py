"""
File in charge of containing the class that will install kind for macos distributions.
"""

from tty_ov import TTY


class UninstallKindMac:
    """ The class in charge of installing kind for linux """

    def __init__(self, tty: TTY, success: int = 0, err: int = 84, error: int = 84) -> None:
        self.tty = tty
        self.print_on_tty = self.tty.print_on_tty
        self.success = success
        self.err = err
        self.error = error

    def main(self) -> int:
        """ The main function of the class """
        return self.success

    def test_class_uninstall_kind_mac(self) -> None:
        """ Test the class uninstall kind MacOS """

        self.print_on_tty(
            self.tty.info_colour,
            "This is a test message from the uninstall kind MacOS class\n"
        )
