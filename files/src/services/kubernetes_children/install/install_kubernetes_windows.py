"""
File in charge of downloading kubernetes for windows
"""

import requests
import display_tty
from tqdm import tqdm
from tty_ov import TTY
from .k3d import InstallK3d
from .k3s import InstallK3s
from .kind import InstallKind
from .kubectl import InstallKubectl
from .microk8s import InstallMicroK8s
from .minikube import InstallMinikube


class InstallKubernetesWindows:
    """ The script in charge of installing the kubernetes interpreter for windows """

    def __init__(self, tty: TTY, success: int = 0, err: int = 84, error: int = 84) -> None:
        # ---- System Codes ----
        self.success = success
        self.err = err
        self.error = error
        # ---- Parent classes ----
        self.tty = tty
        self.k3d = InstallK3d(tty, success, err, error)
        self.k3s = InstallK3s(tty, success, err, error)
        self.microk8s = InstallMicroK8s(tty, success, err, error)
        self.kind = InstallKind(tty, success, err, error)
        self.kubectl = InstallKubectl(tty, success, err, error)
        self.minikube = InstallMinikube(tty, success, err, error)
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

    def download_file(self, url: str, filepath: str) -> int:
        """ Download a file from a url """
        self.print_on_tty(
            self.tty.info_colour,
            f"Downloading file from url: {url}\n"
        )
        try:
            request = requests.get(
                url,
                allow_redirects=True,
                timeout=10,
                stream=True
            )
            with open(filepath, "wb") as file:
                total_length = int(request.headers.get('content-length'))
                chunk_size = 1024
                for chunk in tqdm(
                    request.iter_content(chunk_size=chunk_size),
                    total=(total_length // chunk_size)+1,
                    unit='KB'
                ):
                    if chunk:
                        file.write(chunk)
                        file.flush()
            self.print_on_tty(
                self.tty.success_colour,
                f"File downloaded to: {filepath}\n"
            )
            self.tty.current_tty_status = self.tty.success
            return self.tty.current_tty_status
        except requests.RequestException as err:
            self.print_on_tty(
                self.tty.error_colour,
                f"Error downloading file: {err}\n"
            )
            self.tty.current_tty_status = self.tty.error
            return self.tty.current_tty_status

    def install_kubectl(self) -> int:
        """ The main function in charge of installing kubernetes on windows """
        return self.kubectl.install_windows.main()

    def install_minikube(self) -> int:
        """ Install the minikube software """

    def install_kind(self) -> int:
        """ Install the kind software """

    def install_k3s(self) -> int:
        """ Install the k3s software """

    def install_k3d(self) -> int:
        """ Install the k3s software """

    def install_k8s(self) -> int:
        """ Install the k8s software """

    def install_microk8s(self) -> int:
        """ Install the microk8s software """

    def install_kubeadm(self) -> int:
        """ Install the kubeadm software """

    def is_k3s_installed(self) -> bool:
        """ Check if k3s is installed """
        return self.k3s.install_windows.is_k3s_installed()

    def is_k3d_installed(self) -> bool:
        """ Check if k3d is installed """
        return self.k3d.install_windows.is_k3d_installed()

    def get_master_token(self) -> int:
        """ Get the master token """
        return self.k3s.install_windows.get_k3s_token()

    def main(self) -> int:
        """ The main function of the class """
        return 0

    def test_class_install_kubernetes_windows(self) -> int:
        """ Test the class install kubernetes windows """
        self.print_on_tty(
            self.tty.info_colour,
            "This is a test message from the install kubernetes windows class\n"
        )
        self.kind.test_kind_installation_class()
        self.kubectl.test_kubectl_installation_class()
        self.minikube.test_minikube_installation_class()
        return self.tty.success
