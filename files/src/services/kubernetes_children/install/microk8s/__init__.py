"""
File in charge of loading the MicroK8s installer classes
"""

from tty_ov import TTY
from .install_microk8s_linux import InstallMicroK8sLinux
from .install_microk8s_mac import InstallMicroK8sMac
from .install_microk8s_windows import InstallMicroK8sWindows


class InstallMicroK8s:
    """ Install MicroK8s on the correct device """

    def __init__(self, tty: TTY, success: int = 0, err: int = 84, error: int = 84) -> None:
        self.install_mac = InstallMicroK8sMac(tty, success, err, error)
        self.install_linux = InstallMicroK8sLinux(tty, success, err, error)
        self.install_windows = InstallMicroK8sWindows(tty, success, err, error)

    def test_microk8s_installation_class(self) -> None:
        """ Test the MicroK8s installation class """
        self.install_mac.test_class_install_microk8s_mac()
        self.install_linux.test_class_install_microk8s_linux()
        self.install_windows.test_class_install_microk8s_windows()
