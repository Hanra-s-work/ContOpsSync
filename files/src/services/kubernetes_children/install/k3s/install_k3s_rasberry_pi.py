"""
File in charge of installing k3s on a rasberry pi
"""

import os
import display_tty
import requests
from datetime import datetime
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
        # ---- File options ----
        self.cmdline_file = "/boot/cmdline.txt"
        self.edit_mode = "w"
        self.encoding = "utf-8"
        self.newline = "\n"

    def _get_file_content(self, file_path: str, encoding: str = "utf-8") -> str:
        """ Get the content of a file """
        with open(file_path, "r", encoding=encoding) as file:
            return file.read()

    def _set_file_content(self, file_path: str, content: str, mode: str = "w", encoding: str = "utf-8", newline: str = "\n") -> int:
        """ Set the content of a file """
        self.tty.run_as_admin(
            [
                "echo",
                f"'{content}'",
                f">{file_path}",
            ]
        )
        return self.tty.current_tty_status
        # with open(file_path, mode, encoding=encoding, newline=newline) as file:
        #     file.write(content)
        # return self.success

    def _update_variable_in_string(self, variable: str, value: str, string: str) -> str:
        """ Update a variable in a string """
        variable_value = f"{variable}={value}"
        string = string[:-1]
        if variable not in string:
            string += variable_value
            string += " "
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
            self.print_on_tty(
                self.tty.error_colour,
                "[KO]\n"
            )
            return False
        self.print_on_tty(
            self.tty.success_colour,
            "[OK]\n"
        )
        self.tty.current_tty_status = self.tty.success
        return True

    def is_raspberrypi(self) -> bool:
        """ Check the system to see if we are on a raspberrypi """
        self.print_on_tty(
            self.tty.info_colour,
            "Checking if the system is a raspberry pi:"
        )
        self.tty.current_tty_status = self.run(
            [
                "uname",
                "-m",
                "|",
                "uname",
                "-n",
                "|",
                "grep",
                "-q",
                "raspberrypi"
            ]
        )
        if self.tty.current_tty_status != self.tty.success:
            self.print_on_tty(
                self.tty.error_colour,
                "[KO]\n"
            )
            return False
        self.print_on_tty(
            self.tty.success_colour,
            "[OK]\n"
        )
        self.tty.current_tty_status = self.tty.success
        return True

    def _get_usr_ip(self) -> str:
        """ Get the ip of the machine in order to create a static ip """
        ip_file = "/tmp/your_current_ip.txt"
        self.print_on_tty(
            self.tty.info_colour,
            "Getting the ip of the machine:"
        )
        self.tty.current_tty_status = self.run(
            [
                "hostname",
                "-I",
                f">{ip_file}",
                "2>/dev/null"
            ]
        )
        if self.tty.current_tty_status != self.tty.success:
            self.print_on_tty(
                self.tty.error_colour,
                "[KO]\n"
            )
            return ""
        self.print_on_tty(
            self.tty.success_colour,
            "[OK]\n"
        )
        self.tty.current_tty_status = self.tty.success
        usr_ip = self._get_file_content(ip_file, "utf-8")
        usr_ip = usr_ip.split(" ")[0]
        return usr_ip

    def _get_dns_ip(self) -> str:
        """ Get the ip of the dns for the static ip """
        dns_file = "/tmp/your_current_dns_address.txt"
        self.print_on_tty(
            self.tty.info_colour,
            "Getting the dns of the machine:"
        )
        self.tty.current_tty_status = self.run(
            [
                "cat",
                "/etc/resolv.conf",
                "|",
                "grep",
                "nameserver",
                f">{dns_file}",
                "2>/dev/null"
            ]
        )
        if self.tty.current_tty_status != self.tty.success:
            self.print_on_tty(
                self.tty.error_colour,
                "[KO]\n"
            )
            return ""
        self.print_on_tty(
            self.tty.success_colour,
            "[OK]\n"
        )
        self.tty.current_tty_status = self.tty.success
        dns_ip = self._get_file_content(dns_file, "utf-8")
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

    def _create_hostname(self) -> str:
        """ Create the hostname for the machine """
        hostname = ""
        hostname += f"{self._get_user_name()}-"
        hostname += f"{self._get_computer_name()}-"
        hostname += f"{self._get_date()}"
        return hostname

    def _get_router_name(self) -> str:
        """ Get the name of the current connection form that is used by the system """
        self.print_on_tty(
            self.tty.info_colour,
            "Getting your router name"
        )
        router_name = ""
        router_file_name = "/tmp/your_router_name.txt"
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
                f">{router_file_name}",
                "2>/dev/null"
            ]
        )
        if router_name_status == self.tty.error:
            self.print_on_tty(
                self.tty.error_colour,
                "[KO]\n"
            )
            return ""
        self.print_on_tty(
            self.tty.success_colour,
            "[OK]\n"
        )
        router_name = self._get_file_content(router_file_name, "utf-8")
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
        hostname = self._create_hostname()
        router_name = self._get_router_name()
        auto_dhcpcd = "off"
        if usr_ip == "" or dns_ip == "" or hostname == "" or auto_dhcpcd == "":
            self.print_on_tty(
                self.tty.info_colour,
                "static ip compilation status: "
            )
            self.print_on_tty(
                self.tty.error_colour,
                "[KO]\n"
            )
            return ""
        static_ip = f"ip={usr_ip}::{dns_ip}:{network_mask}:{hostname}:{router_name}:{auto_dhcpcd}"
        self.print_on_tty(
            self.tty.info_colour,
            "static ip compilation status: "
        )
        self.print_on_tty(
            self.tty.success_colour,
            "[OK]\n"
        )
        return static_ip

    def enable_cgroups_if_not(self) -> int:
        """ Enable the cgroups module for the raspberry pi """
        self.print_on_tty(
            self.tty.info_colour,
            "Enabling CGroups:"
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
            self.edit_mode,
            self.encoding,
            self.newline
        )
        self.print_on_tty(
            self.tty.success_colour,
            "[OK]"
        )
        static_ip = self._compile_static_ip()
        if static_ip == "":
            self.tty.current_tty_status = self.tty.error
            return self.err
        self.print_on_tty(
            self.tty.info_colour,
            "Enabling static ip:"
        )
        file_content = self._get_file_content(self.cmdline_file, self.encoding)
        if static_ip not in file_content:
            file_content = self._update_variable_in_string(
                "ip",
                static_ip,
                file_content
            )
        self._set_file_content(
            self.cmdline_file,
            file_content,
            self.edit_mode,
            self.encoding,
            self.newline
        )
        self.print_on_tty(
            self.tty.success_colour,
            "[OK]"
        )
        return self.success

    def main(self) -> int:
        """ Install k3s on RaspberryPi """
        self.print_on_tty(
            self.tty.info_colour,
            ""
        )
        self.disp.sub_title("Installing k3s on RaspberryPi:")
        if not self.is_raspberrypi():
            self.print_on_tty(
                self.tty.error_colour,
                "[KO]\n"
            )
            return self.err
        self.enable_cgroups_if_not()
        return self.success

    def test_class_install_k3s_raspberry_pi(self) -> None:
        """ Test the class install k3s raspberry pi """
        self.print_on_tty(
            self.tty.info_colour,
            "This is a test message from the install k3s raspberry pi class"
        )
