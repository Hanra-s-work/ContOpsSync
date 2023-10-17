"""
File in charge of linking the system uninstaller classes tot the main uninstaller class for kubernetes
"""

from .uninstall_kubernetes_windows import UninstallKubernetesWindows
from .uninstall_kubernetes_linux import UninstallKubernetesLinux
from .uninstall_kubernetes_mac import UninstallKubernetesMac

__all__ = [
    "UninstallKubernetesWindows",
    "UninstallKubernetesLinux",
    "UninstallKubernetesMac"
]


class Uninstall:
    """ The class in charge of grouping the os specific kubernetes uninstallers """

    def __init__(self) -> None:
        self.uninstall_kubernetes_linux = UninstallKubernetesLinux
        self.uninstall_kubernetes_windows = UninstallKubernetesWindows
        self.uninstall_kubernetes_mac = UninstallKubernetesMac

    def test_class_uninstall(self) -> int:
        """ Test the Uninstall class of kubernetes """
        print("This is a test message from the Uninstall class of kubernetes")
        return 0
