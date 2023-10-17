"""
File in charge of containing the class that will uninstall kind for Windows distributions.
"""

from tty_ov import TTY


class UninstallMinikubeWindows:
    """ The class in charge of uninstalling kind for Windows """

    def __init__(self, tty: TTY, success: int = 0, err: int = 84, error: int = 84) -> None:
        self.tty = tty
        self.success = success
        self.err = err
        self.error = error
        self.print_on_tty = self.tty.print_on_tty

    def main(self) -> int:
        """ The main function of the class """
        return self.success

    def test_class_uninstall_minikube_windows(self) -> None:
        """ Test the class uninstall minikube windows """
        self.print_on_tty(
            self.tty.info_colour,
            "This is a test message from the uninstall minikube Windows class"
        )
