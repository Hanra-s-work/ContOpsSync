"""
File in charge of loading the kubectl installer classes
"""

from tty_ov import TTY
from .install_kubernetes_linux import InstallKubectlLinux
from .install_kubernetes_mac import InstallKubectlMac
from .install_kubernetes_windows import InstallKubectlWindows


class InstallKubectl:
    """ Install Kubectl on the correct device """

    def __init__(self, tty: TTY, success: int = 0, err: int = 84, error: int = 84) -> None:
        self.install_mac = InstallKubectlMac(tty, success, err, error)
        self.install_linux = InstallKubectlLinux(tty, success, err, error)
        self.install_windows = InstallKubectlWindows(
            tty,
            success,
            err,
            error
        )

    def test_kubectl_installation_class(self) -> None:
        """ Test the kubectl installation class """
        self.install_mac.test_class_install_kubectl_mac()
        self.install_linux.test_class_install_kubectl_linux()
        self.install_windows.test_class_install_kubectl_windows()
