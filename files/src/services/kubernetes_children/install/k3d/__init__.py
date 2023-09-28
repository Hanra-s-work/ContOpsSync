"""
File in charge of loading the kubectl installer classes
"""

from tty_ov import TTY
from .install_k3d_linux import InstallK3dLinux
from .install_k3d_mac import InstallK3dMac
from .install_k3d_windows import InstallK3dWindows


class InstallK3d:
    """ Install Kubectl on the correct device """

    def __init__(self, tty: TTY, success: int = 0, err: int = 84, error: int = 84) -> None:
        self.install_mac = InstallK3dMac(tty, success, err, error)
        self.install_linux = InstallK3dLinux(tty, success, err, error)
        self.install_windows = InstallK3dWindows(
            tty,
            success,
            err,
            error
        )

    def test_k3d_installation_class(self) -> None:
        """ Test the kubectl installation class """
        self.install_mac.test_class_install_k3d_mac()
        self.install_linux.test_class_install_k3d_linux()
        self.install_windows.test_class_install_k3d_windows()
