"""
File in charge of loading the kind installer classes
"""

from tty_ov import TTY
from .uninstall_kind_linux import UninstallKindLinux
from .uninstall_kind_mac import UninstallKindMac
from .uninstall_kind_windows import UninstallKindWindows


class UninstallKind:
    """ Uninstall Kind on the correct device """

    def __init__(self, tty: TTY, success: int = 0, err: int = 84, error: int = 84) -> None:
        self.uninstall_mac = UninstallKindMac(tty, success, err, error)
        self.uninstall_linux = UninstallKindLinux(tty, success, err, error)
        self.uninstall_windows = UninstallKindWindows(
            tty,
            success,
            err,
            error
        )

    def test_kind_uninstallation_class(self) -> None:
        """ Test the kind installation class """
        self.uninstall_mac.test_class_uninstall_kind_mac()
        self.uninstall_linux.test_class_uninstall_kind_linux()
        self.uninstall_windows.test_class_uninstall_kind_windows()
