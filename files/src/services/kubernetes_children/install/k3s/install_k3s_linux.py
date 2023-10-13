"""
File in charge of containing the class that will install k3s for linux distributions.
"""

import display_tty
import requests
from tqdm import tqdm
from tty_ov import TTY


class InstallK3sLinux:
    """ The class in charge of installing k3s for linux """

    def __init__(self, tty: TTY, success: int = 0, err: int = 84, error: int = 84) -> None:
        # ---- tty class ----
        self.tty = tty
        # ---- Status codes ----
        self.success = success
        self.err = err
        self.error = error
        # ---- tty display rebind ----
        self.run = self.tty.run_command
        self.print_on_tty = self.tty.print_on_tty
        self.function_help = self.tty.function_help
        # ---- The Disp option ----
        self.disp = display_tty.IDISP
        self.disp.toml_content["PRETTIFY_OUTPUT"] = False
        self.disp.toml_content["PRETTY_OUTPUT_IN_BLOCS"] = False
        # ---- k3s installation script ----
        self.k3s_link = "https://get.k3s.io"
        self.k3s_file_name = "/tmp/k3s_install.sh"
        # ---- k3s token file ----
        self.k3s_token_file = "/var/lib/rancher/k3s/server/node-token"
        # ---- k3s token save file ----
        self.token_save_file = "/tmp/k3s_token.txt"

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

    def _has_yay(self) -> bool:
        """ Returns true if the user has yay [package manager] installed """
        self.print_on_tty(
            self.tty.info_colour,
            "Checking if the user has yay installed:"
        )
        self.tty.current_tty_status = self.run(
            [
                "yay",
                "--version",
                ">/dev/null",
                "2>/dev/null"
            ]
        )
        if self.tty.current_tty_status != self.tty.success:
            self.print_on_tty(self.tty.error_colour,"[KO]\n")
            return False
        self.print_on_tty(self.tty.success_colour,"[OK]\n")
        self.tty.current_tty_status = self.tty.success
        return True

    def _has_brew(self) -> bool:
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
            self.print_on_tty(self.tty.error_colour,"[KO]\n")
            return False
        self.print_on_tty(self.tty.success_colour,"[OK]\n")
        self.tty.current_tty_status = self.tty.success
        return True

    def _manual_installation(self) -> int:
        """ Install k3s manually """
        self.disp.sub_sub_title("Installing k3s")
        status = self._download_file(self.k3s_link, self.k3s_file_name)
        if status != self.success:
            self.print_on_tty(
                self.tty.error_colour,
                "Error downloading the k3s install script\n"
            )
            return self.err
        status = self.run(["chmod", "+x", self.k3s_file_name])
        self.print_on_tty(
            self.tty.info_colour,
            "Installation status (k3s):"
        )
        if status != self.success:
            self.print_on_tty(self.tty.error_colour,"[KO]\n")
            self.print_on_tty(
                self.tty.error_colour,
                "Error granting execution permissions to the k3s install script\n"
            )
            return self.err
        self.print_on_tty(self.tty.success_colour,"[OK]\n")
        self.tty.setenv(["K3S_KUBECONFIG_MODE", '"644"'])
        return self.run(["bash", "-c", self.k3s_file_name])

    def _install_for_aur(self) -> int:
        """ Install k3s for Aur systems """
        self.disp.sub_sub_title(
            "Installing k3s for Aur (Arch Linux User Repository) systems"
        )
        status = self.run(
            [
                "yay",
                "-S",
                "rancher-k3s-bin"
            ]
        )
        self.print_on_tty(
            self.tty.info_colour,
            "Installation status (k3s):"
        )
        if status != self.tty.success:
            self.print_on_tty(self.tty.error_colour,"[KO]\n")
            self.print_on_tty(
                self.tty.error_colour,
                "Error installing k3s for Aur systems\n"
            )
            self.print_on_tty(
                self.tty.info_colour,
                "Defaulting to default method\n"
            )
            self.tty.current_tty_status = self.tty.err
            return self.tty.current_tty_status
        self.print_on_tty(self.tty.success_colour,"[OK]\n")
        self.print_on_tty(self.tty.success_colour,"")
        self.disp.success_message("Installed k3s using yay ;-)")
        self.tty.current_tty_status = self.tty.success
        return status

    def _install_for_brew(self) -> int:
        """ Install Kubectl using brew """
        self.disp.sub_sub_title("Installing Kubectl via Brew")
        status = self.run(
            [
                "brew",
                "install",
                "k3s"
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
        self.print_on_tty(
            self.tty.info_colour,
            "Installation status (k3s):"
        )
        if status != self.tty.success:
            self.print_on_tty(
                self.tty.error_colour,
                "Error testing the installation of Kubernetes for Linux\n"
            )
            self.tty.current_tty_status = self.tty.err
            return self.tty.current_tty_status

        self.print_on_tty(self.tty.success_colour,"[OK]\n")
        self.print_on_tty(self.tty.success_colour,"")
        self.disp.success_message("Installed k3s using brew ;-)")
        self.tty.current_tty_status = self.tty.success
        return self.tty.current_tty_status

    def is_k3s_installed(self) -> bool:
        """ Returns true if k3s is installed """
        self.print_on_tty(
            self.tty.info_colour,
            "Checking if k3s is installed:"
        )
        self.tty.current_tty_status = self.run(
            [
                "k3s",
                "--version",
                ">/dev/null",
                "2>/dev/null"
            ]
        )
        if self.tty.current_tty_status != self.tty.success:
            self.print_on_tty(self.tty.error_colour,"[KO]\n")
            return False
        self.print_on_tty(self.tty.success_colour,"[OK]\n")
        self.tty.current_tty_status = self.tty.success
        return True

    def get_k3s_token(self) -> int:
        """ Get the master token for k3s """
        self.print_on_tty(
            self.tty.info_colour,
            "Getting the k3s master token:\n"
        )
        self.tty.current_tty_status = self.run(
            [
                "sudo",
                "cat",
                self.k3s_token_file
            ]
        )
        self.print_on_tty(
            self.tty.info_colour,
            "K3s master token status: "
        )
        if self.tty.current_tty_status != self.tty.success:
            self.print_on_tty(self.tty.error_colour,"[KO]\n")
            return self.error
        self.print_on_tty(self.tty.info_colour,"")
        self.disp.inform_message(
            [
                f"Saving the token to : {self.token_save_file}"
            ]
        )
        status = self.run(
            [
                "sudo",
                "cat",
                self.k3s_token_file,
                f">{self.token_save_file}",
                "2>/dev/null"
            ]
        )
        self.print_on_tty(
            self.tty.info_colour,
            "Saving the token status: "
        )
        if status != self.success:
            self.print_on_tty(self.tty.error_colour,"[KO]\n")
            return self.error
        self.print_on_tty(self.tty.success_colour,"[OK]\n")
        return self.success

    def main(self) -> int:
        """ The main function of the class """
        if self._has_yay() is True:
            status = self._install_for_aur()
            if status == self.success:
                return status
        if self._has_brew() is True:
            status = self._install_for_brew()
            if status == self.success:
                return status
        return self._manual_installation()

    def test_class_install_k3s_linux(self) -> None:
        """ Test the class install k3s linux """
        self.print_on_tty(
            self.tty.info_colour,
            "This is a test message from the install k3s Linux class"
        )
