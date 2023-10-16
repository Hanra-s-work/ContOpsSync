"""
File in charge of containing the class that will install k3s for linux distributions.
"""

import os
import uuid
from datetime import datetime

import requests
import display_tty
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
        self.super_run = self.tty.run_as_admin
        # ---- The Disp option ----
        self.disp = display_tty.IDISP
        self.disp.toml_content["PRETTIFY_OUTPUT"] = False
        self.disp.toml_content["PRETTY_OUTPUT_IN_BLOCS"] = False
        # ---- k3s installation script ----
        self.k3s_link = "https://get.k3s.io"
        self.k3s_file_name = "/tmp/k3s_install.sh"
        # ---- File rights ----
        self.edit_mode = "w"
        self.encoding = "utf-8"
        self.newline = "\n"
        # ---- k3s token file ----
        self.k3s_token_file = "/var/lib/rancher/k3s/server/node-token"
        # ---- k3s token save file ----
        self.token_save_file = "~/your_master_token.txt"
        # ---- K3s Host name file ----
        self.k3s_hostname_file = "/etc/your_k3s_hostname.txt"

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
        except Exception:
            self.run(
                [
                    "wget",
                    "--progress=bar:force",
                    "-O",
                    filepath,
                    url
                ]
            )
            self.print_on_tty(
                self.tty.success_colour,
                f"File downloaded to: {filepath}\n"
            )
            self.tty.current_tty_status = self.tty.success
            return self.tty.current_tty_status

    def _get_file_content(self, file_path: str, encoding: str = "utf-8") -> str:
        """ Get the content of a file """
        with open(file_path, "r", encoding=encoding) as file:
            return file.read()

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
            self.print_on_tty(self.tty.error_colour, "[KO]\n")
            return False
        self.print_on_tty(self.tty.success_colour, "[OK]\n")
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
            self.print_on_tty(self.tty.error_colour, "[KO]\n")
            return False
        self.print_on_tty(self.tty.success_colour, "[OK]\n")
        self.tty.current_tty_status = self.tty.success
        return True

    def _installation_failed_message(self) -> None:
        """ the message to display when the installation fails """
        self.print_on_tty(
            self.tty.info_colour,
            "Installation status k3s: "
        )
        self.print_on_tty(self.tty.error_colour, "[KO]\n")

    def _get_user_name(self) -> str:
        """ Get the username of the user """
        username = os.getlogin()
        return username

    def _get_computer_name(self) -> str:
        """ Get the computer name of the machine """
        computer_name = os.uname()[1]
        return computer_name

    def _get_date(self) -> str:
        """ Get the date of the machine """
        date = datetime.now()
        compiled_date = ""
        compiled_date += f"{date.day}-"
        compiled_date += f"{date.month}-"
        compiled_date += f"{date.year}-"
        compiled_date += f"{date.hour}h"
        compiled_date += f"{date.minute}m"
        compiled_date += f"{date.second}s"
        return compiled_date

    def _create_uuid(self) -> str:
        """ Create a uuid for the username """
        return str(uuid.uuid4())

    def _create_short_uuid(self) -> str:
        """ Create a shorter version fo the uuid for the username """
        return self._create_uuid()[:8]

    def _create_hostname(self) -> str:
        """ Create the hostname for the machine """
        self.print_on_tty(
            self.tty.info_colour,
            "Creating the k3s hostname for the system:"
        )
        hostname = ""
        hostname += f"{self._get_user_name()}-"
        hostname += f"{self._get_computer_name()}-"
        hostname += f"{self._get_date()}-"
        hostname += f"{self._create_short_uuid()}"
        self.print_on_tty(
            self.tty.info_colour,
            "Hostname status: "
        )
        if hostname == "":
            self.print_on_tty(self.tty.error_colour, "[KO]\n")
            return ""
        self.print_on_tty(self.tty.success_colour, "[OK]\n")
        self.print_on_tty(
            self.tty.info_colour,
            f"Saving hostname to {self.k3s_hostname_file}"
        )
        status = self.super_run(
            [
                "echo",
                f"\"{hostname}\"",
                f">{self.k3s_hostname_file}",
                "2>/dev/null"
            ]
        )
        self.print_on_tty(
            self.tty.info_colour,
            "Hostname save status: "
        )
        if status != self.success:
            self.print_on_tty(self.tty.error_colour, "[KO]\n")
            return hostname
        self.print_on_tty(self.tty.success_colour, "[OK]\n")
        return hostname

    def _install_master_k3s(self, force_docker: bool = False) -> int:
        """ Install the k3s version for the master node (the one managing the others) """
        self.tty.setenv(["K3S_KUBECONFIG_MODE", '"644"'])
        install_line = [
            "chmod",
            "+x",
            self.k3s_file_name,
            "&&",
            "sudo",
            self.k3s_file_name
        ]
        if force_docker is True:
            self.tty.setenv(["K3S_FORCE_INSTALL_DOCKER", "1"])
            install_line.append("--docker")

        self.run(install_line)
        self.get_k3s_token()
        return self.tty.success

    def _install_slave_k3s(self, force_docker: bool = False, master_token: str = "", master_ip: str = "") -> int:
        """ Install the k3s version for the slave, the one being managed by the masters """
        if master_token == "" or master_ip == "":
            self.print_on_tty(
                self.tty.error_colour,
                "Master token or master ip is empty\n"
            )
            self.tty.current_tty_status = self.tty.error
            return self.error
        self.tty.setenv(["K3S_KUBECONFIG_MODE", '"644"'])
        self.tty.setenv(["K3S_TOKEN", f"{master_token}"])
        self.tty.setenv(["K3S_URL", f"https://{master_ip}:6443"])
        self.tty.setenv(
            [
                "K3S_NODE_NAME",
                self._get_file_content(self.k3s_hostname_file, self.encoding)
            ]
        )
        install_line = [
            "chmod",
            "+x",
            self.k3s_file_name,
            "&&",
            "sudo",
            self.k3s_file_name
        ]
        if force_docker is True:
            self.tty.setenv(["K3S_FORCE_INSTALL_DOCKER", "1"])
            install_line.append("--docker")
        self.run(install_line)
        return self.tty.success

    def _manual_installation(self, install_as_slave: bool = False, force_docker: bool = False, master_token: str = "", master_ip: str = "") -> int:
        """ Install k3s manually """
        self.disp.sub_sub_title("Installing k3s")
        status = self._download_file(self.k3s_link, self.k3s_file_name)
        if status != self.success:
            self.print_on_tty(
                self.tty.error_colour,
                "Error downloading the k3s install script\n"
            )
            return self.err
        status = self.run(["sudo ", "chmod", "+x", self.k3s_file_name])
        self.print_on_tty(
            self.tty.info_colour,
            "Download status (k3s):"
        )
        if status != self.success:
            self.print_on_tty(self.tty.error_colour, "[KO]\n")
            self.print_on_tty(
                self.tty.error_colour,
                "Error granting execution permissions to the k3s install script\n"
            )
            return self.err
        self.print_on_tty(self.tty.success_colour, "[OK]\n")
        if install_as_slave is True:
            status = self._install_slave_k3s(
                force_docker,
                master_token,
                master_ip
            )
            if status != self.success:
                self._installation_failed_message()
                return self.error
        else:
            status = self._install_master_k3s(force_docker)
            if status != self.success:
                self._installation_failed_message()
                return self.error
        self.print_on_tty(
            self.tty.info_colour,
            "Installation status status: "
        )
        self.print_on_tty(self.tty.success_colour, "[OK]\n")

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
            self.print_on_tty(self.tty.error_colour, "[KO]\n")
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
        self.print_on_tty(self.tty.success_colour, "[OK]\n")
        self.print_on_tty(self.tty.success_colour, "")
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

        self.print_on_tty(self.tty.success_colour, "[OK]\n")
        self.print_on_tty(self.tty.success_colour, "")
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
            self.print_on_tty(self.tty.error_colour, "[KO]\n")
            return False
        self.print_on_tty(self.tty.success_colour, "[OK]\n")
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
            self.print_on_tty(self.tty.error_colour, "[KO]\n")
            return self.error
        self.print_on_tty(self.tty.info_colour, "")
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
            self.print_on_tty(self.tty.error_colour, "[KO]\n")
            return self.error
        self.print_on_tty(self.tty.success_colour, "[OK]\n")
        return self.success

    def main(self, install_as_slave: bool = False, force_docker: bool = False, master_token: str = "", master_ip: str = "") -> int:
        """ The main function of the class """
        if self._manual_installation(install_as_slave, force_docker, master_token, master_ip) != self.success:
            if self._has_yay() is True:
                status = self._install_for_aur()
                if status == self.success:
                    return status
            if self._has_brew() is True:
                status = self._install_for_brew()
                if status == self.success:
                    return status
        return self.success

    def test_class_install_k3s_linux(self) -> None:
        """ Test the class install k3s linux """
        self.print_on_tty(
            self.tty.info_colour,
            "This is a test message from the install k3s Linux class"
        )
