"""
File in charge of containing the class that will install kubernetes for linux distributions.
"""

import display_tty
import requests
from tqdm import tqdm
from tty_ov import TTY
from .k3d import UninstallK3d
from .k3s import UninstallK3s
from .k8s import UninstallK8s
from .kind import UninstallKind
from .kubectl import UninstallKubectl
from .microk8s import UninstallMicroK8s
from .minikube import UninstallMinikube


class UninstallKubernetesLinux:
    """ The class in charge of uninstalling kubernetes for linux """

    def __init__(self, tty: TTY, success: int = 0, err: int = 84, error: int = 84) -> None:
        # ---- System Codes ----
        self.success = success
        self.err = err
        self.error = error
        # ---- Parent classes ----
        self.tty = tty
        self.k3d = UninstallK3d(tty, success, err, error)
        self.k3s = UninstallK3s(tty, success, err, error)
        self.k8s = UninstallK8s(tty, success, err, error)
        self.kind = UninstallKind(tty, success, err, error)
        self.kubectl = UninstallKubectl(tty, success, err, error)
        self.microk8s = UninstallMicroK8s(tty, success, err, error)
        self.minikube = UninstallMinikube(tty, success, err, error)
        # ---- TTY rebinds ----
        self.print_on_tty = self.tty.print_on_tty
        self.run = self.tty.run_command
        self.function_help = self.tty.function_help
        # ---- Download options ----
        self.download_options = {
            "choco": False,
            "scoop": False,
            "winget": False
        }
        # ---- The Disp option ----
        self.disp = display_tty.IDISP
        self.disp.toml_content["PRETTIFY_OUTPUT"] = False
        self.disp.toml_content["PRETTY_OUTPUT_IN_BLOCS"] = False

    def uninstall_kubectl(self) -> int:
        """ Uninstall kubectl for linux """
        return self.kubectl.uninstall_linux.main()

    def uninstall_minikube(self) -> int:
        """ Uninstall the minikube software """
        return self.minikube.uninstall_linux.main()

    def uninstall_kind(self) -> int:
        """ Uninstall the kind software """
        return self.kind.uninstall_linux.main()

    def uninstall_k3s(self) -> int:
        """ Uninstall the k3s software """
        return self.k3s.uninstall_linux.main()

    def uninstall_k3d(self) -> int:
        """ Uninstall the k3d software """
        return self.k3d.uninstall_linux.main()

    def uninstall_k8s(self) -> int:
        """ Uninstall the k8s software """
        return self.k8s.uninstall_linux.main()

    def uninstall_microk8s(self) -> int:
        """ Uninstall the microk8s software """
        return self.microk8s.uninstall_linux.main()

    def uninstall_kubeadm(self) -> int:
        """ Uninstall the kubeadm software """
        return self.print_on_tty(
            self.tty.info_colour,
            "This option is not yet available due to system requirements that would be long and difficult to verify for each linux distribution"
        )

    def main(self) -> int:
        """ The main function of the program """
        self.print_on_tty(
            self.tty.info_colour,
            ""
        )
        self.disp.inform_message([
            "Nothing to see here."
            "This is just a regular empty main function"
        ])

    def test_class_uninstall_kubernetes_linux(self) -> int:
        """ Test the class install kubernetes linux """
        self.print_on_tty(
            self.tty.info_colour,
            "This is a test message from the uninstall kubernetes linux class\n"
        )
        self.kind.test_kind_uninstallation_class()
        self.kubectl.test_kubectl_uninstallation_class()
        self.minikube.test_minikube_uninstallation_class()
        return self.success
