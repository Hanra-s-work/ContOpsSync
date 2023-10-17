"""
File in charge of loading the k8s installer classes
"""

from tty_ov import TTY
from .uninstall_k8s_linux import UninstallK8sLinux
from .uninstall_k8s_mac import UninstallK8sMac
from .uninstall_k8s_windows import UninstallK8sWindows


class UninstallK8s:
    """ Uninstall K8s on the correct device """

    def __init__(self, tty: TTY, success: int = 0, err: int = 84, error: int = 84) -> None:
        self.uninstall_mac = UninstallK8sMac(tty, success, err, error)
        self.uninstall_linux = UninstallK8sLinux(tty, success, err, error)
        self.uninstall_windows = UninstallK8sWindows(
            tty,
            success,
            err,
            error
        )

    def test_k8s_installation_class(self) -> None:
        """ Test the k8s installation class """
        self.uninstall_mac.test_class_uninstall_k8s_mac()
        self.uninstall_linux.test_class_uninstall_k8s_linux()
        self.uninstall_windows.test_class_uninstall_k8s_windows()
