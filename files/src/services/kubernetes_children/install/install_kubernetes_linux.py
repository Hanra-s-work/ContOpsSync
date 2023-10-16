"""
File in charge of containing the class that will install kubernetes for linux distributions.
"""

import display_tty
import requests
from tqdm import tqdm
from tty_ov import TTY
from .k3d import InstallK3d
from .k3s import InstallK3s
from .k8s import InstallK8s
from .kind import InstallKind
from .kubectl import InstallKubectl
from .microk8s import InstallMicroK8s
from .minikube import InstallMinikube


class InstallKubernetesLinux:
    """ The class in charge of installing kubernetes for linux """

    def __init__(self, tty: TTY, success: int = 0, err: int = 84, error: int = 84) -> None:
        # ---- System Codes ----
        self.success = success
        self.err = err
        self.error = error
        # ---- Parent classes ----
        self.tty = tty
        self.k3d = InstallK3d(tty, success, err, error)
        self.k3s = InstallK3s(tty, success, err, error)
        self.k8s = InstallK8s(tty, success, err, error)
        self.kind = InstallKind(tty, success, err, error)
        self.kubectl = InstallKubectl(tty, success, err, error)
        self.microk8s = InstallMicroK8s(tty, success, err, error)
        self.minikube = InstallMinikube(tty, success, err, error)
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
        # ---- k3s installation script ----
        self.k3s_link = "https://get.k3s.io"
        self.k3s_file_name = "/tmp/k3s_install.sh"
        # ---- k8s installation script ----
        self.k8s_link = "https://get.k8s.io"
        self.k8s_file_name = "/tmp/k8s_install.sh"

    def _download_file(self, url: str, filepath: str) -> int:
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
        """ Install kubectl for linux """
        return self.kubectl.install_linux.main()

    def install_minikube(self) -> int:
        """ Install the minikube software """
        return self.minikube.install_linux.main()

    def install_kind(self) -> int:
        """ Install the kind software """
        return self.kind.install_linux.main()

    def install_k3s(self, install_as_slave: bool = False, force_docker: bool = False, master_token: str = "", master_ip: str = "") -> int:
        """ Install the k3s software """
        if self.k3s.install_raspberrypi.is_raspberrypi() is True:
            return self.k3s.install_raspberrypi.main(install_as_slave, force_docker, master_token, master_ip)
        return self.k3s.install_linux.main(install_as_slave, force_docker, master_token, master_ip)

    def install_k3d(self, install_as_slave: bool = False, master_token: str = "", master_ip: str = "") -> int:
        """ Install the k3d software """
        if self.k3s.install_raspberrypi.is_raspberrypi() is True:
            return self.k3d.install_raspberrypi.main(install_as_slave, master_token, master_ip)
        return self.k3d.install_linux.main()

    def install_k8s(self) -> int:
        """ Install the k8s software """
        return self.k8s.install_linux.main()

    def install_microk8s(self) -> int:
        """ Install the microk8s software """
        return self.microk8s.install_linux.main()

    def install_kubeadm(self) -> int:
        """ Install the kubeadm software """
        return self.print_on_tty(
            self.tty.info_colour,
            "This option is not yet available due to system requirements that would be long and difficult to verify for each linux distribution"
        )

    def is_k3s_installed(self) -> bool:
        """ Check if k3s is installed """
        if self.k3s.install_raspberrypi.is_raspberrypi() is True:
            return self.k3s.install_raspberrypi.is_k3s_installed()
        return self.k3s.install_linux.is_k3s_installed()

    def is_k3d_installed(self) -> bool:
        """ Check if k3d is installed """
        if self.k3d.install_raspberrypi.is_raspberrypi() is True:
            return self.k3d.install_raspberrypi.is_k3d_installed()
        return self.k3d.install_linux.is_k3d_installed()

    def get_master_token(self) -> int:
        """ Get the master token """
        if self.k3s.install_raspberrypi.is_raspberrypi() is True:
            return self.k3s.install_raspberrypi.get_k3s_token()
        return self.k3s.install_linux.get_k3s_token()

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

    def test_class_install_kubernetes_linux(self) -> int:
        """ Test the class install kubernetes linux """
        self.print_on_tty(
            self.tty.info_colour,
            "This is a test message from the install kubernetes linux class"
        )
        self.kind.test_kind_installation_class()
        self.kubectl.test_kubectl_installation_class()
        self.minikube.test_minikube_installation_class()
        return self.success
