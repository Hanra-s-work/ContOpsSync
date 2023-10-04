"""
File in charge of loading the minikube installer classes
"""

from tty_ov import TTY
from .install_minikube_linux import InstallMinikubeLinux
from .install_minikube_mac import InstallMinikubeMac
from .install_minikube_windows import InstallMinikubeWindows


class InstallMinikube:
    """ Install minikube on the correct device """

    def __init__(self, tty: TTY, success: int = 0, err: int = 84, error: int = 84) -> None:
        self.install_mac = InstallMinikubeMac(tty, success, err, error)
        self.install_linux = InstallMinikubeLinux(tty, success, err, error)
        self.install_windows = InstallMinikubeWindows(
            tty,
            success,
            err,
            error
        )

    def test_minikube_installation_class(self) -> None:
        """ Test the minikube installation class """
        self.install_mac.test_class_install_minikube_mac()
        self.install_linux.test_class_install_minikube_linux()
        self.install_windows.test_class_install_minikube_windows()
