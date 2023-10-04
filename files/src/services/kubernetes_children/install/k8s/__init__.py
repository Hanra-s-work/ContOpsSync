"""
File in charge of loading the k8s installer classes
"""

from tty_ov import TTY
from .install_k8s_linux import InstallK8sLinux
from .install_k8s_mac import InstallK8sMac
from .install_k8s_windows import InstallK8sWindows


class InstallK8s:
    """ Install K8s on the correct device """

    def __init__(self, tty: TTY, success: int = 0, err: int = 84, error: int = 84) -> None:
        self.install_mac = InstallK8sMac(tty, success, err, error)
        self.install_linux = InstallK8sLinux(tty, success, err, error)
        self.install_windows = InstallK8sWindows(
            tty,
            success,
            err,
            error
        )

    def test_k8s_installation_class(self) -> None:
        """ Test the k8s installation class """
        self.install_mac.test_class_install_k8s_mac()
        self.install_linux.test_class_install_k8s_linux()
        self.install_windows.test_class_install_k8s_windows()
