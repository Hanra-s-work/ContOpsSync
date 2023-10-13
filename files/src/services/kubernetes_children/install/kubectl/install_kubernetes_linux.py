"""
File in charge of containing the class that will install kubectl for linux distributions.
"""

import os
from platform import machine, platform
import display_tty
import requests
from tqdm import tqdm
from tty_ov import TTY


class InstallKubectlLinux:
    """ The class in charge of installing kubernetes for linux """

    def __init__(self, tty: TTY, success: int = 0, err: int = 84, error: int = 84) -> None:
        # ---- System Codes ----
        self.success = success
        self.err = err
        self.error = error
        # ---- Parent classes ----
        self.tty = tty
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
        # ---- links for manual installation ----
        self.release_file = "https://cdn.dl.k8s.io/release/stable.txt"
        self.install_file_link_chunk1 = "https://dl.k8s.io/release/"
        self.install_file_link_chunk2 = "/bin/linux/"
        self.install_file_link_chunk3 = "/kubectl"
        self.installer_name = "kubectl"
        self.installer_folder = ".kubectl"
        self.hardware_platform = ""
        self.home = ""
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

    def get_file_content(self, file_path: str) -> str or int:
        """ Get the content of a file """
        if os.path.isfile(file_path) is False:
            self.print_on_tty(
                self.tty.error_colour,
                f"Error getting file content: {file_path} is not a file\n"
            )
            self.tty.current_tty_status = self.tty.error
            return self.tty.current_tty_status
        try:
            with open(file_path, "r", encoding="utf-8", newline="\n") as file:
                content = file.read()
            self.tty.current_tty_status = self.tty.success
            return content
        except OSError as err:
            self.print_on_tty(
                self.tty.error_colour,
                f"Error getting file content: {err}\n"
            )
            self.tty.current_tty_status = self.tty.error
            return self.tty.current_tty_status

    def _get_latest_version(self) -> int:
        """ Get the latest version of the program """
        self.tty.current_tty_status = self.tty.success
        self.print_on_tty(
            self.tty.info_colour,
            "Getting the latest version of Kubernetes for Linux\n"
        )
        version_name = "version.useless"
        status = self.download_file(
            self.release_file,
            version_name
        )
        if status != self.tty.success:
            self.print_on_tty(
                self.tty.error_colour,
                "Error getting the latest release of Kubernetes for Linux\n"
            )
            self.tty.current_tty_status = status
            return self.tty.current_tty_status
        file_content = self.get_file_content(version_name)
        if file_content == self.tty.error:
            self.print_on_tty(
                self.tty.error_colour,
                "Error getting the latest release of Kubernetes for Linux\n"
            )
            self.tty.current_tty_status = self.tty.error
            return self.tty.current_tty_status
        download_link = f"{self.install_file_link_chunk1}{file_content}{self.install_file_link_chunk2}{self.hardware_platform}{self.install_file_link_chunk3}"
        self.installer_name = f"/tmp/{self.installer_name}"
        status = self.download_file(
            download_link,
            self.installer_name
        )
        if self.tty.current_tty_status != self.tty.success:
            self.print_on_tty(
                self.tty.error_colour,
                "Error downloading the latest release of Kubernetes for Linux\n"
            )
            return self.tty.current_tty_status
        self.print_on_tty(
            self.tty.success_colour,
            "Downloaded Kubernetes for Linux\n"
        )
        self.tty.current_tty_status = self.tty.success
        return self.tty.current_tty_status

    def _install_kubectl(self) -> int:
        """ Install the kubectl file in the system """
        self.print_on_tty(
            self.tty.info_colour,
            ""
        )
        self.disp.sub_sub_title("Installing Kubernetes")
        status = self.run(
            [
                "sudo",
                "install",
                "-o root",
                "-g root",
                "-m 0755",
                self.installer_name,
                "/usr/local/bin/kubectl"
            ]
        )
        if status != self.tty.success:
            self.print_on_tty(
                self.tty.error_colour,
                "Error installing Kubernetes for Linux\n"
            )
            self.tty.current_tty_status = self.tty.err
            return self.tty.current_tty_status
        self.tty.current_tty_status = status
        return self.tty.current_tty_status

    def get_hardware_platform(self) -> str:
        """ Get the hardware platform of the current system """
        system_architecture = machine()
        if system_architecture in ("AMD64", "x86_64"):
            return "amd64"
        if system_architecture in ("ARM64", "ARM"):
            return "arm64"
        if system_architecture in "i386":
            if "x64" in platform():
                return "amd64"
        return ""

    def test_installation(self) -> int:
        """ Make sure that the kubectl is installed and operational """
        self.print_on_tty(
            self.tty.info_colour,
            "Testing the installation of Kubernetes for Windows\n"
        )
        self.tty.current_tty_status = self.run(
            [
                "kubectl",
                "version",
                "--output=yaml"
            ]
        )
        if self.tty.current_tty_status != self.tty.success:
            self.print_on_tty(
                self.tty.error_colour,
                "Error testing the installation of Kubernetes for Windows\n"
            )
            return self.tty.current_tty_status
        self.tty.current_tty_status = self.tty.success
        return self.tty.current_tty_status

    def has_snap(self) -> bool:
        """ Returns true if the user has snap [package manager] installed """
        self.print_on_tty(
            self.tty.info_colour,
            "Checking if the user has snap installed:"
        )
        self.tty.current_tty_status = self.run(
            [
                "snap",
                "--version",
                ">/dev/null",
                "2>/dev/null"
            ]
        )
        if self.tty.current_tty_status != self.tty.success:
            self.print_on_tty(self.tty.error_colour, "[KO]\n")
            return False
        self.print_on_tty(self.tty.success_colour, "[OK]\n")
        self.tty.current_tty_status = self.tty.success
        return True

    def has_brew(self) -> bool:
        """ Returns true if the user has brew [package manager] installed """
        self.print_on_tty(
            self.tty.info_colour,
            "Checking if the user has brew installed:"
        )
        self.tty.current_tty_status = self.run(
            [
                "brew",
                "--version",
                ">/dev/null",
                "2>/dev/null"
            ]
        )
        if self.tty.current_tty_status != self.tty.success:
            self.print_on_tty(self.tty.error_colour, "[KO]\n")
            return False
        self.print_on_tty(self.tty.success_colour, "[OK]\n")
        self.tty.current_tty_status = self.tty.success
        return True

    def install_for_snap(self) -> int:
        """ Install Kubectl using snap """
        self.disp.sub_sub_title("Installing Kubectl via Snap")
        status = self.run(
            [
                "snap",
                "install",
                "kubectl",
                "--classic"
            ]
        )
        if status != self.tty.success:
            self.print_on_tty(
                self.tty.error_colour,
                "Error installing Kubernetes for Linux, reverting to manual install\n"
            )
            self.tty.current_tty_status = self.tty.err
            return self.tty.current_tty_status
        status = self.run(
            [
                "kubectl",
                "version",
                "--output=yaml"
            ]
        )
        if status != self.tty.success:
            self.print_on_tty(
                self.tty.error_colour,
                "Error testing the installation of Kubernetes for Linux\n"
            )
            self.tty.current_tty_status = self.tty.err
            return self.tty.current_tty_status
        self.print_on_tty(
            self.tty.success_colour,
            ""
        )
        self.disp.success_message("Installed Kubectl using snap ;-)")
        self.tty.current_tty_status = self.tty.success
        return self.tty.current_tty_status

    def install_for_brew(self) -> int:
        """ Install Kubectl using brew """
        self.disp.sub_sub_title("Installing Kubectl via Brew")
        status = self.run(
            [
                "brew",
                "install",
                "kubectl"
            ]
        )
        if status != self.tty.success:
            self.print_on_tty(
                self.tty.error_colour,
                "Error installing Kubectl for Linux, reverting to manual install\n"
            )
            self.tty.current_tty_status = self.tty.err
            return self.tty.current_tty_status
        self.disp.success_message("Kubectl has successfully been installed.")
        self.disp.sub_sub_title("Testing Kubectl installation")
        status = self.run(
            [
                "kubectl",
                "version",
                "--output=yaml"
            ]
        )
        if status != self.tty.success:
            self.print_on_tty(
                self.tty.error_colour,
                "Error testing the installation of Kubectl for Linux\n"
            )
            self.print_on_tty(
                self.tty.info_colour,
                "Error testing the installation of Kubectl for Linux\n"
            )
            self.tty.current_tty_status = self.tty.err
            return self.tty.current_tty_status
        self.print_on_tty(
            self.tty.success_colour,
            ""
        )
        self.disp.success_message("Installed Kubectl using brew ;-)")
        self.tty.current_tty_status = self.tty.success
        return self.tty.current_tty_status

    def install_kubectl(self) -> int:
        """ Install kubectl for linux """
        self.print_on_tty(self.tty.help_title_colour, "")
        self.disp.title("Downloading Kubernetes for Linux")
        if self.has_snap() is True:
            if self.install_for_snap() == self.success:
                return self.success
        elif self.has_brew() is True:
            if self.install_for_brew() == self.success:
                return self.success
        self.hardware_platform = self.get_hardware_platform()
        if self.hardware_platform == "":
            self.print_on_tty(
                self.tty.error_colour,
                "Error getting the architecture of your system\n"
            )
            self.tty.current_tty_status = self.tty.error
            return self.err
        status = self._get_latest_version()
        if status != self.tty.success:
            self.print_on_tty(
                self.tty.error_colour,
                "Error downloading the latest release of Kubernetes for Linux\n"
            )
            self.tty.current_tty_status = self.tty.error
            return self.tty.current_tty_status
        status = self._install_kubectl()
        if status != self.success:
            self.print_on_tty(
                self.tty.error_colour,
                "Error installing Kubernetes for Linux\n"
            )
            self.tty.current_tty_status = self.tty.error
            return self.tty.current_tty_status
        status = self.test_installation()
        if status != self.success:
            self.print_on_tty(
                self.tty.error_colour,
                "Error testing the installation of Kubernetes for Linux\n"
            )
            self.tty.current_tty_status = self.tty.error
            return self.tty.current_tty_status
        self.print_on_tty(
            self.tty.success_colour,
            "Downloaded Kubernetes for Linux\n"
        )
        self.tty.current_tty_status = self.tty.success
        return self.tty.current_tty_status

    def main(self) -> int:
        """ Install kubernetes on Linux """
        return self.install_kubectl()

    def test_class_install_kubectl_linux(self) -> int:
        """ Test the class install kubectl linux """
        self.print_on_tty(
            self.tty.info_colour,
            "This is a test message from the install kubectl linux class"
        )
        return 0
