"""
File in charge of linking the system installer classes tot the main installer class for kubernetes
"""

from .install_kubernetese_windows import InstallKubernetesWindows
from .install_kubernetese_linux import InstallKubernetesLinux
from .install_kubernetese_mac import InstallKubernetesMac

__all__ = ["InstallKubernetesWindows", "InstallKubernetesLinux", "InstallKubernetesMac"]

class Install:
    """ The class in charge of grouping the os specific kubernetes installers """
    def __init__(self) -> None:
        self.install_kubernetes_linux = InstallKubernetesLinux
        self.install_kubernetes_windows = InstallKubernetesWindows
        self.install_kubernetes_mac = InstallKubernetesMac
    def test_class_install(self) -> int:
        """ Test the Install class of kubernetes """
        print("This is a test message from the Install class of kubernetes")
        return 0
