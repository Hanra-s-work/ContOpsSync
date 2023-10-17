"""
File in charge of loading the minikube installer classes
"""

from tty_ov import TTY
from .uninstall_minikube_linux import UninstallMinikubeLinux
from .uninstall_minikube_mac import UninstallMinikubeMac
from .uninstall_minikube_windows import UninstallMinikubeWindows


class UninstallMinikube:
    """ Uninstall minikube on the correct device """

    def __init__(self, tty: TTY, success: int = 0, err: int = 84, error: int = 84) -> None:
        self.uninstall_mac = UninstallMinikubeMac(tty, success, err, error)
        self.uninstall_linux = UninstallMinikubeLinux(tty, success, err, error)
        self.uninstall_windows = UninstallMinikubeWindows(
            tty,
            success,
            err,
            error
        )

    def test_minikube_uninstallation_class(self) -> None:
        """ Test the minikube uninstallation class """
        self.uninstall_mac.test_class_uninstall_minikube_mac()
        self.uninstall_linux.test_class_uninstall_minikube_linux()
        self.uninstall_windows.test_class_uninstall_minikube_windows()
