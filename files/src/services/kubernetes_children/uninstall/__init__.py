"""
File in charge of linking the system installer classes tot the main installer class for kubernetes
"""

from .uninstall_kubernetese_windows import UninstallKubernetesWindows
from .uninstall_kubernetese_linux import UninstallKubernetesLinux
from .uninstall_kubernetese_mac import UninstallKubernetesMac

__all__ = ["UninstallKubernetesWindows",
           "UninstallKubernetesLinux", "UninstallKubernetesMac"]


class Uninstall:
    """ The class in charge of grouping the os specific kubernetes installers """

    def __init__(self) -> None:
        self.uninstall_kubernetes_linux = UninstallKubernetesLinux
        self.uninstall_kubernetes_windows = UninstallKubernetesWindows
        self.uninstall_kubernetes_mac = UninstallKubernetesMac

    def test_class_install(self) -> int:
        """ Test the Install class of kubernetes """
        print("This is a test message from the Install class of kubernetes")
        return 0
