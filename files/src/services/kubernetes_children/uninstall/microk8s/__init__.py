"""
File in charge of loading the MicroK8s uninstaller classes
"""

from tty_ov import TTY
from .uninstall_microk8s_linux import UninstallMicroK8sLinux
from .uninstall_microk8s_mac import UninstallMicroK8sMac
from .uninstall_microk8s_windows import UninstallMicroK8sWindows


class UninstallMicroK8s:
    """ Uninstall MicroK8s on the correct device """

    def __init__(self, tty: TTY, success: int = 0, err: int = 84, error: int = 84) -> None:
        self.uninstall_mac = UninstallMicroK8sMac(tty, success, err, error)
        self.uninstall_linux = UninstallMicroK8sLinux(tty, success, err, error)
        self.uninstall_windows = UninstallMicroK8sWindows(
            tty,
            success,
            err,
            error
        )

    def test_microk8s_installation_class(self) -> None:
        """ Test the MicroK8s installation class """
        self.uninstall_mac.test_class_uninstall_microk8s_mac()
        self.uninstall_linux.test_class_uninstall_microk8s_linux()
        self.uninstall_windows.test_class_uninstall_microk8s_windows()
