"""
File in charge of containing the code that will install kubernetes on a mac.
"""

from tty_ov import TTY
import display_tty
from .k3d import UninstallK3d
from .k3s import UninstallK3s
from .kind import UninstallKind
from .kubectl import UninstallKubectl
from .microk8s import UninstallMicroK8s
from .minikube import UninstallMinikube


class UninstallKubernetesMac:
    """ Uninstall the kubernetes on Mac """

    def __init__(self, tty: TTY, success: int = 0, err: int = 84, error: int = 84) -> None:
        # ---- System Codes ----
        self.success = success
        self.err = err
        self.error = error
        # ---- Parent classes ----
        self.tty = tty
        self.k3d = UninstallK3d(tty, success, err, error)
        self.k3s = UninstallK3s(tty, success, err, error)
        self.microk8s = UninstallMicroK8s(tty, success, err, error)
        self.kind = UninstallKind(tty, success, err, error)
        self.kubectl = UninstallKubectl(tty, success, err, error)
        self.minikube = UninstallMinikube(tty, success, err, error)
        # ---- TTY rebinds ----
        self.print_on_tty = self.tty.print_on_tty
        # ---- Download options ----
        self.download_options = {
            "choco": False,
            "scoop": False,
            "winget": False  # ,
            # "manual":False
        }
        # ---- The Disp option ----
        self.disp = display_tty.IDISP
        self.disp.toml_content["PRETTIFY_OUTPUT"] = False
        self.disp.toml_content["PRETTY_OUTPUT_IN_BLOCS"] = False
        # ---- links for manual installation ----
        self.release_file = "https://cdn.dl.k8s.io/release/stable.txt"
        self.install_file_link_chunk1 = "https://dl.k8s.io/release/"
        self.install_file_link_chunk2 = "/bin/windows/amd64/kubectl.exe"
        self.installer_name = "kubectl.exe"
        self.installer_folder = ".kubectl"
        self.home = ""
        self.full_path = ""
        # ---- Testing installation ----
        self.kube_folder = ".kube"
        self.config_file = "config"

    def install_kubectl(self) -> None:
        """ install the kubectl software """
        return self.kubectl.uninstall_mac.uninstall_kubectl()

    def install_minikube(self) -> int:
        """ Install the minikube software """
        self.print_on_tty(
            self.tty.info_colour,
            "The installation script is yet to come for macs."
        )
        return self.success

    def install_kind(self) -> int:
        """ Install the kind software """
        self.print_on_tty(
            self.tty.info_colour,
            "The installation script is yet to come for macs."
        )
        return self.success

    def install_k3s(self) -> int:
        """ Install the k3s software (needs to be written)"""
        self.print_on_tty(
            self.tty.info_colour,
            "The installation script is yet to come for macs."
        )
        return self.success

    def install_k3d(self) -> int:
        """ Install the k3s software """
        self.print_on_tty(
            self.tty.info_colour,
            "The installation script is yet to come for macs."
        )
        return self.success

    def install_k8s(self) -> int:
        """ Install the k8s software """
        self.print_on_tty(
            self.tty.info_colour,
            "The installation script is yet to come for macs."
        )
        return self.success

    def install_microk8s(self) -> int:
        """ Install the k8s software """
        self.print_on_tty(
            self.tty.info_colour,
            "The installation script is yet to come for macs."
        )
        return self.success

    def install_kubeadm(self) -> int:
        """ Install the kubeadm software """
        self.print_on_tty(
            self.tty.info_colour,
            "The installation script is yet to come for macs."
        )
        return self.success

    def main(self) -> None:
        """ Install kubernetes on Mac """
        print("Install kubernetes on Mac - Not created yet")
        return self.success

    def test_class_install_kubernetes_mac(self) -> int:
        """ Test the class install kubernetes mac """
        self.print_on_tty(
            self.tty.info_colour,
            "This is a test message from the install kubernetes mac class\n"
        )
        self.kind.test_kind_uninstallation_class()
        self.kubectl.test_kubectl_uninstallation_class()
        self.minikube.test_minikube_uninstallation_class()
        return self.success
