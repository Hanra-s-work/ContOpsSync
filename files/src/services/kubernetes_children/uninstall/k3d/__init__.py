"""
File in charge of loading the k3d installer classes
"""

from tty_ov import TTY
from .uninstall_k3d_linux import UninstallK3dLinux
from .uninstall_k3d_mac import UninstallK3dMac
from .uninstall_k3d_windows import UninstallK3dWindows


class UninstallK3d:
    """ Install K3d on the correct device """

    def __init__(self, tty: TTY, success: int = 0, err: int = 84, error: int = 84) -> None:
        self.uninstall_mac = UninstallK3dMac(tty, success, err, error)
        self.uninstall_linux = UninstallK3dLinux(tty, success, err, error)
        self.uninstall_windows = UninstallK3dWindows(
            tty,
            success,
            err,
            error
        )

    def test_k3d_uninstallation_class(self) -> None:
        """ Test the k3d installation class """
        self.uninstall_mac.test_class_uninstall_k3d_mac()
        self.uninstall_linux.test_class_uninstall_k3d_linux()
        self.uninstall_windows.test_class_uninstall_k3d_windows()
