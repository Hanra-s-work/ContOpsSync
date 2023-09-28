"""
File in charge of containing the class that will install kubernetes for linux distributions.
"""

import os
import display_tty
import requests
from tqdm import tqdm
from tty_ov import TTY
from .k3d import InstallK3d
from .kind import InstallKind
from .kubectl import InstallKubectl
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
        self.kind = InstallKind(tty, success, err, error)
        self.kubectl = InstallKubectl(tty, success, err, error)
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
        """ Install kubectl for linux """
        return self.kubectl.install_linux.main()

    def install_minikube(self) -> int:
        """ Install the minikube software """
        return self.minikube.install_linux.main()

    def install_kind(self) -> int:
        """ Install the kind software """
        return self.kind.install_linux.main()

    def install_k3s(self) -> int:
        """ Install the k3s software """
        self.disp.sub_sub_title("Installing k3s")
        status = self.download_file(self.k3s_link, self.k3s_file_name)
        if status != self.success:
            self.print_on_tty(
                self.tty.error_colour,
                "Error downloading the k3s install script\n"
            )
            return self.err
        status = self.run(["chmod", "+x", self.k3s_file_name])
        if status != self.success:
            self.print_on_tty(
                self.tty.error_colour,
                "Error granting execution permissions to the k3s install script\n"
            )
            return self.err
        return self.run(["bash", "-c", self.k3s_file_name])

    def install_k3d(self) -> int:
        """ Install the k3d software """
        return self.k3d.install_linux.main()

    def install_k8s(self) -> int:
        """ Install the k8s software """
        self.disp.sub_sub_title("Installing k8s")
        status = self.download_file(self.k8s_link, self.k8s_file_name)
        if status != self.success:
            self.print_on_tty(
                self.tty.error_colour,
                "Error downloading the k8s install script\n"
            )
            return self.err
        status = self.run(["chmod", "+x", self.k8s_file_name])
        if status != self.success:
            self.print_on_tty(
                self.tty.error_colour,
                "Error granting execution permissions to the k8s install script\n"
            )
            return self.err
        return self.run(["bash", "-c", self.k8s_file_name])

    def install_kubeadm(self) -> int:
        """ Install the kubeadm software """

    def main(self) -> int:
        """ The main function of the program """

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
