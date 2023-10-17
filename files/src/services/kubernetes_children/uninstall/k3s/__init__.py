"""
File in charge of loading the k3s installer classes
"""

from tty_ov import TTY
from .uninstall_k3s_linux import UninstallK3sLinux
from .uninstall_k3s_mac import UninstallK3sMac
from .uninstall_k3s_windows import UninstallK3sWindows


class UninstallK3s:
    """ Install K3s on the correct device """

    def __init__(self, tty: TTY, success: int = 0, err: int = 84, error: int = 84) -> None:
        self.uninstall_mac = UninstallK3sMac(tty, success, err, error)
        self.uninstall_linux = UninstallK3sLinux(tty, success, err, error)
        self.uninstall_windows = UninstallK3sWindows(
            tty,
            success,
            err,
            error
        )

    def test_k3s_installation_class(self) -> None:
        """ Test the k3s installation class """
        self.uninstall_mac.test_class_uninstall_k3s_mac()
        self.uninstall_linux.test_class_uninstall_k3s_linux()
        self.uninstall_windows.test_class_uninstall_k3s_windows()
