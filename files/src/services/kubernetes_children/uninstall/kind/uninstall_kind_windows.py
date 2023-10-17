"""
File in charge of containing the class that will install kind for Windows distributions.
"""

from tty_ov import TTY


class UninstallKindWindows:
    """ The class in charge of installing kind for Windows """

    def __init__(self, tty: TTY, success: int = 0, err: int = 84, error: int = 84) -> None:
        self.tty = tty
        self.success = success
        self.err = err
        self.error = error

    def main(self) -> int:
        """ The main function of the class """
        return self.success

    def test_class_uninstall_kind_windows(self) -> None:
        """ Test the class uninstall kind windows """
        print("This is a test message from the uninstall kind Windows class")
