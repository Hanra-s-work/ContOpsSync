"""
File in charge of installing docker on the system
"""

import os
import display_tty
import requests
from tqdm import tqdm
from tty_ov import TTY
from platform import system


class InstallDocker:
    """ The class in charge of installing docker on the system """

    def __init__(self, tty: TTY, success: int = 0, err: int = 84, error: int = 84) -> None:
        # ---- System Codes ----
        self.success = success
        self.err = err
        self.error = error
        # ---- Parent classes ----
        self.tty = tty
        self.disp = display_tty.IDISP
        # ---- TTY rebinds ----
        self.print_on_tty = self.tty.print_on_tty
        self.run = self.tty.run_command
        self.function_help = self.tty.function_help
        # ---- Disp options ----
        self.disp.toml_content["PRETTIFY_OUTPUT"] = False
        self.disp.toml_content["PRETTY_OUTPUT_IN_BLOCS"] = False
        # ---- Installer links ----
        self.docker_windows = "https://desktop.docker.com/win/main/amd64/Docker%20Desktop%20Installer.exe"
        self.docker_mac_intel = "https://desktop.docker.com/mac/main/amd64/Docker.dmg"
        self.docker_mac_arm = "https://desktop.docker.com/mac/main/arm64/Docker.dmg"
        # ---- System rights ----
        self.program_is_admin = self.is_admin()
        # ---- System scripting ----
        self.windows_script = ""

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

    def check_if_admin_for_windows(self) -> bool:
        """ Check if the current windows user has admin rights """
        command = """
:: Check if the script is running with administrative privileges
net session >nul 2>&1
if %errorLevel% == 0 (
    exit 2
) else (
    exit 3
)
"""
        status = os.system(command)
        if status == 2:
            return True
        return False

    def is_admin(self) -> bool:
        """ Check if the user has admin rights """
        try:
            # On Windows, check if the user has administrator privileges
            if os.name == 'nt':
                return self.check_if_admin_for_windows()
            # On Unix-like systems, check if the user is the root user
            else:
                return os.geteuid() == 0
        except AttributeError:
            return False

    def run_as_windows_admin(self, file: str) -> int:
        """ Run a powershell script as an administrator """
        self.run(
            [
                "powershell.exe",
                "-ExecutionPolicy Bypass",
                f"-File {file}"
            ]
        )

    def install_wsl2(self) -> int:
        """ Install wsl2 on the user's system """
        self.print_on_tty(
            self.tty.info_colour,
            ""
        )
        self.disp.sub_title("Installing wsl package")
        status = self.run(
            [
                "wsl --install"
            ]
        )
        if status != self.tty.success:
            self.print_on_tty(
                self.tty.error_colour,
                ""
            )
            self.disp.error_message("Error installing wsl")
            return self.tty.error
        self.print_on_tty(
            self.tty.success_colour,
            ""
        )
        self.disp.success_message("wsl installed")
        self.print_on_tty(
            self.tty.info_colour,
            ""
        )
        self.disp.sub_title("Setting wsl2 as default")
        status = self.run(
            [
                "wsl --set-default-version 2",
            ]
        )
        if status != self.tty.success:
            self.print_on_tty(
                self.tty.error_colour,
                ""
            )
            self.disp.error_message("Error setting wsl2 as default")
            return self.tty.error
        status = self.run(
            [
                "wsl --install ubuntu"
            ]
        )
        if status != self.tty.success:
            self.print_on_tty(
                self.tty.error_colour,
                ""
            )
            self.disp.error_message("Error installing ubuntu")
            return self.tty.error
        response = self.tty.ask_question.ask_question(
            "For changes to be applied, the system needs to be restarted. Restart now? [(Y)es/(N)o]: ",
            "bool"
        )
        if response is True:
            self.run(
                [
                    "shutdown",
                    "/r",
                    "/t",
                    "00"
                ]
            )
        return self.tty.success

    def install_for_mac(self) -> int:
        pass

    def install_for_linux(self) -> int:
        pass

    def install_for_windows(self) -> int:
        """ Install Docker for windows """
        file_name = f"{os.getcwd()}\\docker_install.ps1"
        self.print_on_tty(
            self.tty.info_colour,
            ""
        )
        self.disp.sub_title("Creating installer script")
        self.disp.sub_title("Adding WSL2 installtion line to script")
        self.disp.sub_title("Adding Docker installtion line to script")
        self.disp.sub_title("Running installer script")
        self.disp.sub_title("Removing installer script")

    def main(self) -> int:
        """ The workflow dispatcher """
        self.print_on_tty(
            self.tty.success_colour,
            ""
        )
        self.disp.title("Installing Docker")
        current_system = system()
        self.disp.inform_message(f"Detected system: {current_system}")
        if current_system == "Windows":
            return self.install_for_windows()
        if current_system == "Linux":
            return self.install_for_linux()
        if current_system == "Darwin" or current_system == "Java":
            return self.install_for_mac()
        self.print_on_tty(
            self.tty.error_colour,
            ""
        )
        self.disp.error_message(f"System {current_system} not supported")
        return self.tty.error
