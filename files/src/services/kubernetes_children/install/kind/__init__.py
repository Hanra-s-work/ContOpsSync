"""
File in charge of loading the kubectl installer classes
"""

from tty_ov import TTY
from .install_kind_linux import InstallKindLinux
from .install_kind_mac import InstallKindMac
from .install_kind_windows import InstallKindWindows


class InstallKind:
    """ Install Kubectl on the correct device """

    def __init__(self, tty: TTY, success: int = 0, err: int = 84, error: int = 84) -> None:
        self.install_mac = InstallKindMac(tty, success, err, error)
        self.install_linux = InstallKindLinux(tty, success, err, error)
        self.install_windows = InstallKindWindows(
            tty,
            success,
            err,
            error
        )

    def test_kind_installation_class(self) -> None:
        """ Test the kubectl installation class """
        self.install_mac.test_class_install_kind_mac()
        self.install_linux.test_class_install_kind_linux()
        self.install_windows.test_class_install_kind_windows()
