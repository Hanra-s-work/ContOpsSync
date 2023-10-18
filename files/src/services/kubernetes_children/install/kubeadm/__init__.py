"""
File in charge of loading the kubeadm installer classes
"""

from tty_ov import TTY
from .install_kubeadm_linux import InstallKubeadmLinux
from .install_kubeadm_mac import InstallKubeadmMac
from .install_kubeadm_windows import InstallKubeadmWindows


class InstallKubeadm:
    """ Install kubeadm on the correct device """

    def __init__(self, tty: TTY, success: int = 0, err: int = 84, error: int = 84) -> None:
        self.install_mac = InstallKubeadmMac(tty, success, err, error)
        self.install_linux = InstallKubeadmLinux(tty, success, err, error)
        self.install_windows = InstallKubeadmWindows(
            tty,
            success,
            err,
            error
        )

    def test_kubeadm_installation_class(self) -> None:
        """ Test the kubeadm installation class """
        self.install_mac.test_class_install_kubeadm_mac()
        self.install_linux.test_class_install_kubeadm_linux()
        self.install_windows.test_class_install_kubeadm_windows()
