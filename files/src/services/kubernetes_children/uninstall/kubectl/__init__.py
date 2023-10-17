"""
File in charge of loading the kubectl uninstaller classes
"""

from tty_ov import TTY
from .uninstall_kubernetes_linux import UninstallKubectlLinux
from .uninstall_kubernetes_mac import UninstallKubectlMac
from .uninstall_kubernetes_windows import UninstallKubectlWindows


class UninstallKubectl:
    """ Uninstall Kubectl on the correct device """

    def __init__(self, tty: TTY, success: int = 0, err: int = 84, error: int = 84) -> None:
        self.uninstall_mac = UninstallKubectlMac(tty, success, err, error)
        self.uninstall_linux = UninstallKubectlLinux(tty, success, err, error)
        self.uninstall_windows = UninstallKubectlWindows(
            tty,
            success,
            err,
            error
        )

    def test_kubectl_uninstallation_class(self) -> None:
        """ Test the kubectl uninstallation class """
        self.uninstall_mac.test_class_uninstall_kubectl_mac()
        self.uninstall_linux.test_class_uninstall_kubectl_linux()
        self.uninstall_windows.test_class_uninstall_kubectl_windows()
