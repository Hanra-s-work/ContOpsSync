"""
File in charge of installing k3s on a rasberry pi
"""

import os
import uuid
from datetime import datetime

import requests
import display_tty
from tqdm import tqdm
from tty_ov import TTY


class InstallK3sRaspberryPi:
    """ The class in charge of installing k3s on a Raspberry Pi """

    def __init__(self, tty: TTY, success: int = 0, err: int = 84, error: int = 84) -> None:
        # ---- The status codes ----
        self.success = success
        self.err = err
        self.error = error
        # ---- The TTY options ----
        self.tty = tty
        self.print_on_tty = self.tty.print_on_tty
        self.super_run = self.tty.run_as_admin
        self.run = self.tty.run_command
        # ---- The Disp option ----
        self.disp = display_tty.IDISP
        self.disp.toml_content["PRETTIFY_OUTPUT"] = False
        self.disp.toml_content["PRETTY_OUTPUT_IN_BLOCS"] = False
        # ---- Installed path ----
        self.installer_path = "https://get.k3s.io/"
        # ---- File locations ----
        self.cmdline_file = "/boot/cmdline.txt"
        self.config_file_path = "/boot/config.txt"
        self.release_file = "/etc/os-release"
        self.k3s_token_file = "/var/lib/rancher/k3s/server/node-token"
        self.dns_file = "/etc/resolv.conf"
        self.installer_file = "./k3s_installer.sh"
        # ---- File rights ----
        self.edit_mode = "w"
        self.encoding = "utf-8"
        self.newline = "\n"
        # ---- Token file ----
        self.token_save_file = "~/your_master_token.txt"
        # ---- K3s Host name file ----
        self.k3s_hostname_file = "/etc/your_k3s_hostname.txt"
        # ---- Dns file ----
        self.dns_save_file = "/tmp/your_current_dns_address.txt"
        # ---- IP file ----
        self.ip_save_file = "/tmp/your_current_ip.txt"
        # ---- Router file ----
        self.router_save_file = "/tmp/your_router_name.txt"

    def _get_file_content(self, file_path: str, encoding: str = "utf-8") -> str:
        """ Get the content of a file """
        with open(file_path, "r", encoding=encoding) as file:
            return file.read()

    def _set_file_content(self, file_path: str, content: str, newline: str = "\n") -> int:
        """ Set the content of a file """
        content = content.replace("\r\n", newline)
        self.tty.run_as_admin(
            [
                "echo",
                "-n",
                f"'{content}'",
                f">{file_path}",
            ]
        )
        return self.tty.current_tty_status

    def _update_variable_in_string(self, variable: str, value: str, string: str) -> str:
        """ Update a variable in a string """
        variable_value = f"{variable}={value}"
        string = string[:-1]
        if variable not in string:
            string += " "
            string += variable_value
            string += "\n"
            return string
        if variable_value not in string:
            string1, string2 = string.split(variable)
            buffer_index = 0
            if len(string2) > 0 and string2[0] == "=":
                for i in string2:
                    if i == " ":
                        buffer_index = +1
                        break
                    buffer_index += 1
                string2 = string2[buffer_index:]
            string = f"{string1} {variable_value} {string2}"
        string += "\n"
        return string

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

    def is_k3s_installed(self) -> bool:
        """ Returns true if k3s is installed """
        self.print_on_tty(
            self.tty.info_colour,
            "Checking if k3s is installed:\n"
        )
        self.tty.current_tty_status = self.run(
            [
                "k3s",
                "--version",
                ">/dev/null",
                "2>/dev/null"
            ]
        )
        self.print_on_tty(
            self.tty.info_colour,
            "K3s status: "
        )

        if self.tty.current_tty_status != self.tty.success:
            self.print_on_tty(self.tty.error_colour, "[KO]\n")
            return False
        self.print_on_tty(self.tty.success_colour, "[OK]\n")
        self.tty.current_tty_status = self.tty.success
        return True

    def is_raspberrypi(self) -> bool:
        """ Check the system to see if we are on a raspberrypi """
        self.print_on_tty(
            self.tty.info_colour,
            "Checking if the system is a raspberry pi:\n"
        )
        self.tty.current_tty_status = self.run(
            [
                "uname",
                "-n",
                "|",
                "grep",
                "-q",
                "raspberrypi"
            ]
        )
        self.print_on_tty(
            self.tty.info_colour,
            "Is Rasberry Pi status: "
        )
        if self.tty.current_tty_status != self.tty.success:
            self.print_on_tty(self.tty.error_colour, "[KO]\n")
            return False
        self.print_on_tty(self.tty.success_colour, "[OK]\n")
        self.tty.current_tty_status = self.tty.success
        return True

    def _get_usr_ip(self) -> str:
        """ Get the ip of the machine in order to create a static ip """
        self.print_on_tty(
            self.tty.info_colour,
            "Getting the IP of the machine:\n"
        )
        self.tty.current_tty_status = self.run(
            [
                "hostname",
                "-I",
                f">{self.ip_save_file}",
                "2>/dev/null"
            ]
        )
        self.print_on_tty(
            self.tty.info_colour,
            "Machine IP status: "
        )

        if self.tty.current_tty_status != self.tty.success:
            self.print_on_tty(self.tty.error_colour, "[KO]\n")
            return ""
        self.print_on_tty(self.tty.success_colour, "[OK]\n")
        self.tty.current_tty_status = self.tty.success
        usr_ip = self._get_file_content(self.ip_save_file, "utf-8")
        usr_ip = usr_ip.replace("\n", " ")
        usr_ip = usr_ip.split(" ")[0]
        return usr_ip

    def _get_dns_ip(self) -> str:
        """ Get the ip of the dns for the static ip """
        self.print_on_tty(
            self.tty.info_colour,
            "Getting the dns of the machine:\n"
        )
        self.tty.current_tty_status = self.run(
            [
                "cat",
                self.dns_file,
                "|",
                "grep",
                "nameserver",
                f">{self.dns_save_file}",
                "2>/dev/null"
            ]
        )
        self.print_on_tty(
            self.tty.info_colour,
            "DNS status: "
        )
        if self.tty.current_tty_status != self.tty.success:
            self.print_on_tty(self.tty.error_colour, "[KO]\n")
            return ""
        self.print_on_tty(self.tty.success_colour, "[OK]\n")
        self.tty.current_tty_status = self.tty.success
        dns_ip = self._get_file_content(self.dns_save_file, "utf-8")
        dns_ip = dns_ip.replace("\n", " ")
        dns_ip = dns_ip.split(" ")[1]
        return dns_ip

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

    def _get_current_hostname_if_exists(self) -> str:
        """ Get the current hostname if it exists """
        current_hostname = self._get_file_content(
            self.cmdline_file,
            self.encoding
        )
        if "ip" in current_hostname:
            current_hostname = current_hostname.split("ip=")[1]
            current_hostname = current_hostname.split(" ")[0]
            current_hostname = current_hostname.split("\n")[0]
            static_ip = current_hostname.split(":")
            if len(static_ip) == 6:
                current_hostname = static_ip[3]
                return current_hostname
        else:
            return self._create_hostname()

    def _get_router_name(self) -> str:
        """ Get the name of the current connection form that is used by the system """
        self.print_on_tty(
            self.tty.info_colour,
            "Getting your router name: \n"
        )
        router_name = ""
        ip = self._get_usr_ip()
        router_name_status = self.run(
            [
                "ifconfig",
                "|",
                "grep",
                "-B1",
                f"'{ip}'",
                "|",
                "cut",
                "-d",
                "\":\"",
                "-f",
                "1",
                "|",
                "cut",
                "-d",
                "\" \"",
                "-f",
                "1",
                f">{self.router_save_file}",
                "2>/dev/null"
            ]
        )
        self.print_on_tty(
            self.tty.info_colour,
            "Router name status: "
        )
        if router_name_status == self.tty.error:
            self.print_on_tty(self.tty.error_colour, "[KO]\n")
            return ""
        self.print_on_tty(self.tty.success_colour, "[OK]\n")
        router_name = self._get_file_content(self.router_save_file, "utf-8")
        router_name = router_name.replace("\n", " ")
        router_name = router_name.split(" ")[0]
        return router_name

    def _compile_static_ip(self) -> str:
        """ compile the required data for the static ip """
        self.print_on_tty(
            self.tty.info_colour,
            "Compiling the static ip:\n"
        )
        usr_ip = self._get_usr_ip()
        dns_ip = self._get_dns_ip()
        network_mask = "255.255.255.0"
        hostname = self._get_current_hostname_if_exists()
        router_name = self._get_router_name()
        auto_configuration_here_off = "off"
        self.print_on_tty(
            self.tty.info_colour,
            "static ip compilation status: "
        )
        if usr_ip == "" or dns_ip == "" or hostname == "" or auto_configuration_here_off == "":
            self.print_on_tty(self.tty.error_colour, "[KO]\n")
            return ""
        static_ip = f"{usr_ip}::{dns_ip}:{network_mask}:{hostname}:{router_name}:{auto_configuration_here_off}"
        self.print_on_tty(self.tty.success_colour, "[OK]\n")
        return static_ip

    def _check_if_cgroup_is_running(self) -> int:
        """ Check if the cgroup is running, returns success if true """
        self.print_on_tty(
            self.tty.info_colour,
            "Checking if the cgroup is running:\n"
        )
        self.tty.current_tty_status = self.run(
            [
                "status=\"$(grep",
                "memory",
                "/proc/cgroups",
                "|",
                "while",
                "read",
                "-r",
                "n",
                "n",
                "n",
                "enabled;",
                "do",
                "echo",
                "$enabled;",
                "done)\";",
                "if [ $status -eq 0 ];",
                "then",
                "exit 1;",
                "else",
                "exit 0;",
                "fi;"
            ]
        )
        self.print_on_tty(
            self.tty.info_colour,
            "CGroup status: "
        )
        if self.tty.current_tty_status != self.tty.success:
            self.print_on_tty(self.tty.error_colour, "[KO]\n")
            return self.err
        self.print_on_tty(self.tty.success_colour, "[OK]\n")
        return self.success

    def _enable_cgroups_if_not(self) -> int:
        """ Enable the cgroups module for the raspberry pi """
        self.print_on_tty(
            self.tty.info_colour,
            "Enabling CGroups:\n"
        )
        var1 = "cgroup_memory"
        val1 = "1"
        var2 = "cgroup_enable"
        val2 = "memory"
        file_content = self._get_file_content(self.cmdline_file, self.encoding)
        if f"{var1}={val1}" not in file_content:
            file_content = self._update_variable_in_string(
                var1,
                val1,
                file_content
            )
        if f"{var2}={val2}" not in file_content:
            file_content = self._update_variable_in_string(
                var2,
                val2,
                file_content
            )
        self._set_file_content(
            self.cmdline_file,
            file_content,
            self.newline
        )
        self.print_on_tty(
            self.tty.info_colour,
            "CGroup status: "
        )
        self.print_on_tty(self.tty.success_colour, "[OK]\n")
        static_ip = self._compile_static_ip()
        if static_ip == "":
            self.tty.current_tty_status = self.tty.error
            return self.err
        self.print_on_tty(
            self.tty.info_colour,
            "Enabling static ip:\n"
        )
        file_content = self._get_file_content(self.cmdline_file, self.encoding)
        if static_ip.split(":")[0] not in file_content:
            file_content = self._update_variable_in_string(
                "ip",
                static_ip,
                file_content
            )
        self._set_file_content(
            self.cmdline_file,
            file_content,
            self.newline
        )
        self.print_on_tty(
            self.tty.info_colour,
            "Ip status: "
        )
        self.print_on_tty(self.tty.success_colour, "[OK]\n")
        return self.success

    def _force_64bit_boot(self) -> int:
        """ Force the raspberry pi to boot in 64 bit mode if this is not already the case """
        self.print_on_tty(
            self.tty.info_colour,
            "Forcing the raspberry pi to boot in 64 bit mode:\n"
        )
        config_content = self._get_file_content(
            file_path=self.config_file_path,
            encoding=self.encoding
        )
        if "arm_64bit=1" not in config_content:
            config_content += "arm_64bit=1\n"
            status = self._set_file_content(
                file_path=self.config_file_path,
                content=config_content,
                newline=self.newline
            )
            if status == self.err:
                self.print_on_tty(
                    self.tty.info_colour,
                    "Force 64 bit boot status: "
                )
                self.print_on_tty(self.tty.error_colour, "[KO]\n")
                return self.err
        self.print_on_tty(
            self.tty.info_colour,
            "Force 64 bit boot status: "
        )
        self.print_on_tty(self.tty.success_colour, "[OK]\n")
        return self.success

    def _installation_failed_message(self) -> None:
        """ the message to display when the installation fails """
        self.print_on_tty(
            self.tty.info_colour,
            "Installation status k3s: "
        )
        self.print_on_tty(self.tty.error_colour, "[KO]\n")

    def _enabeling_iptables(self) -> int:
        """ Refresh the iptables to make sure they are up to date """
        self.print_on_tty(
            self.tty.info_colour,
            "Refreshing iptables:\n"
        )
        self.tty.current_tty_status = self.run(
            [
                "sudo",
                "su",
                "-c",
                "'iptables",
                "-F'",
                "&&",
                "sudo",
                "su",
                "-c",
            ]
        )

    def _check_pi_base_flavor(self) -> str:
        """ Check if the distribution the raspberry pi os is based on is Ubuntu or Debian """
        self.print_on_tty(
            self.tty.info_colour,
            "Checking if the raspberry pi is based on Ubuntu or Debian:\n"
        )
        self.tty.current_tty_status = self.run(
            [
                "cat",
                self.release_file,
                "|",
                "grep",
                "-q",
                "ubuntu"
            ]
        )
        if self.tty.current_tty_status == self.tty.success:
            self.print_on_tty(
                self.tty.info_colour,
                "Raspberry pi base flavor status: "
            )
            self.print_on_tty(self.tty.success_colour, "[OK]\n")
            return "ubuntu"
        self.tty.current_tty_status = self.run(
            [
                "cat",
                self.release_file,
                "|",
                "grep",
                "-q",
                "debian"
            ]
        )
        self.print_on_tty(
            self.tty.info_colour,
            "Raspberry pi base flavor status: "
        )
        if self.tty.current_tty_status == self.tty.success:
            self.print_on_tty(self.tty.success_colour, "[OK]\n")
            return "debian"
        self.print_on_tty(self.tty.error_colour, "[KO]\n")
        return ""

    def _install_extra_ubuntu_dependencies(self) -> int:
        """ Install extra ubuntu dependencies for vxlan support """
        self.print_on_tty(
            self.tty.info_colour,
            "Installing extra ubuntu dependencies:\n"
        )
        status = self.run(
            [
                "sudo",
                "su",
                "-c",
                "\"apt",
                "install",
                "-y",
                "linux-modules-extra-raspi\""
            ]
        )
        if status != self.tty.success:
            self.print_on_tty(
                self.tty.info_colour,
                "Extra ubuntu dependencies status: "
            )
            self.print_on_tty(self.tty.success_colour, "[KO]\n")
            return self.err
        self.print_on_tty(
            self.tty.info_colour,
            "Extra ubuntu dependencies status: "
        )
        self.print_on_tty(self.tty.success_colour, "[OK]\n")

    def _install_extra_debian_dependencies(self) -> int:
        """ Install extra debian dependencies for vxlan support """
        self.print_on_tty(
            self.tty.info_colour,
            "Installing extra debian dependencies:\n"
        )
        status = self.run(
            [
                "sudo",
                "su",
                "-c",
                "\"apt",
                "install",
                "-y",
                "libavcodec-extra",
                "ttf-mscorefonts-installer",
                "unrar",
                "chromium-codecs-ffmpeg-extra",
                "gstreamer1.0-libav",
                "gstreamer1.0-plugins-ugly",
                "gstreamer1.0-vaapi\""
            ]
        )
        if status != self.tty.success:
            self.print_on_tty(
                self.tty.info_colour,
                "Extra debian dependencies status: "
            )
            self.print_on_tty(self.tty.success_colour, "[KO]\n")
            return self.err
        self.print_on_tty(
            self.tty.info_colour,
            "Extra debian dependencies status: "
        )
        self.print_on_tty(self.tty.success_colour, "[OK]\n")

    def _prepping_failed_message(self) -> None:
        """ The message to display when the prepping fails """
        self.print_on_tty(
            self.tty.info_colour,
            "Prepping status: "
        )
        self.print_on_tty(self.tty.error_colour, "[KO]\n")

    def _prepare_board(self) -> int:
        """ Prepare the files and all the required elements for a successefull k3s installation """
        self.print_on_tty(self.tty.info_colour, "")
        self.disp.sub_sub_title(
            "Preparing the board for the installation of k3s"
        )
        status = self._enable_cgroups_if_not()
        if status == self.err:
            self._installation_failed_message()
            return status
        status = self._force_64bit_boot()
        if status == self.err:
            self._installation_failed_message()
            return status
        pi_system = self._check_pi_base_flavor()
        if pi_system == "ubuntu":
            status = self._install_extra_ubuntu_dependencies()
            if status == self.err:
                self._installation_failed_message()
                return status
        if pi_system == "debian":
            status = self._install_extra_debian_dependencies()
            if status == self.err:
                self._installation_failed_message()
                return self.err
        self.print_on_tty(
            self.tty.info_colour,
            "Prepping status: "
        )
        self.print_on_tty(self.tty.success_colour, "[OK]\n")
        return self.success

    def get_k3s_installer(self) -> int:
        """ Download the k3s installer """
        self.print_on_tty(
            self.tty.info_colour,
            "Downloading the k3s installer:\n"
        )
        status = self._download_file(self.installer_path, self.installer_file)
        self.print_on_tty(
            self.tty.info_colour,
            "K3s installer status: "
        )
        if status != self.success:
            self.print_on_tty(self.tty.error_colour, "[KO]\n")
            return self.error
        self.print_on_tty(self.tty.success_colour, "[OK]\n")
        return self.success

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
        self.print_on_tty(
            self.tty.info_colour,
            ""
        )
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

    def _install_master_k3s(self, force_docker: bool = False) -> int:
        """ Install the k3s version for the master node (the one managing the others) """
        self.tty.setenv(["K3S_KUBECONFIG_MODE", '"644"'])
        self.tty.setenv(["K3S_FORCE_INSTALL_DOCKER", "0"])
        self.tty.setenv(
            [
                "K3S_NODE_NAME",
                self._get_file_content(self.k3s_hostname_file, self.encoding)
            ]
        )
        install_line = [
            "chmod",
            "+x",
            self.installer_file,
            "&&",
            "sudo",
            self.installer_file
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
        self.tty.setenv(["K3S_FORCE_INSTALL_DOCKER", "0"])
        self.tty.setenv(
            [
                "K3S_NODE_NAME",
                self._get_file_content(self.k3s_hostname_file, self.encoding)
            ]
        )
        install_line = [
            "chmod",
            "+x",
            self.installer_file,
            "&&",
            "sudo",
            self.installer_file
        ]
        if force_docker is True:
            self.tty.setenv(["K3S_FORCE_INSTALL_DOCKER", "1"])
            install_line.append("--docker")
        self.run(install_line)
        return self.tty.success

    def main(self, install_as_slave: bool = False, force_docker: bool = False, master_token: str = "", master_ip: str = "") -> int:
        """ Install k3s on RaspberryPi """
        self.print_on_tty(
            self.tty.info_colour,
            ""
        )
        self.disp.sub_title("Installing k3s on RaspberryPi:")
        if not self.is_raspberrypi():
            self.print_on_tty(
                self.tty.info_colour,
                ""
            )
            self.disp.inform_message(
                [
                    "You are not on a Raspberry Pi",
                    "Thus, this section of the program is not suited for you"
                ]
            )
            self._installation_failed_message()
            return self.err
        status = self._prepare_board()
        if status != self.success:
            self._installation_failed_message()
            return self.error
        self.print_on_tty(self.tty.info_colour, "")
        self.disp.sub_sub_title("Checking cgroup status")
        response = self._check_if_cgroup_is_running()
        self.print_on_tty(self.tty.info_colour, "cgroup status:")
        if response != self.success:
            self.print_on_tty(self.tty.error_colour, "[KO]\n")
            self._installation_failed_message()
            self.print_on_tty(self.tty.error_colour, "")
            self.disp.error_message("The cgroup is not running")
            self.print_on_tty(self.tty.info_colour, "")
            self.disp.inform_message(
                [
                    "The cgroup has been enabled but is not running.",
                    "Please reboot your system and try again the same way run this program."
                ]
            )
            return self.error
        self.print_on_tty(self.tty.success_colour, "[OK]\n")
        status = self.get_k3s_installer()
        if status != self.success:
            self._installation_failed_message()
            return self.error
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
        return self.success

    def test_class_install_k3s_raspberry_pi(self) -> None:
        """ Test the class install k3s raspberry pi """
        self.print_on_tty(
            self.tty.info_colour,
            "This is a test message from the install k3s raspberry pi class\n"
        )
