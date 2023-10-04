"""
File in charge of loading the k3s installer classes
"""

from tty_ov import TTY
from .install_k3s_linux import InstallK3sLinux
from .install_k3s_mac import InstallK3sMac
from .install_k3s_windows import InstallK3sWindows
from .install_k3s_rasberry_pi import InstallK3sRaspberryPi


class InstallK3s:
    """ Install K3s on the correct device """

    def __init__(self, tty: TTY, success: int = 0, err: int = 84, error: int = 84) -> None:
        self.install_mac = InstallK3sMac(tty, success, err, error)
        self.install_linux = InstallK3sLinux(tty, success, err, error)
        self.install_raspberrypi = InstallK3sRaspberryPi(
            tty,
            success,
            err,
            error
        )
        self.install_windows = InstallK3sWindows(
            tty,
            success,
            err,
            error
        )

    def test_k3s_installation_class(self) -> None:
        """ Test the k3s installation class """
        self.install_mac.test_class_install_k3s_mac()
        self.install_linux.test_class_install_k3s_linux()
        self.install_windows.test_class_install_k3s_windows()
        self.install_raspberrypi.test_class_install_k3s_raspberry_pi()
