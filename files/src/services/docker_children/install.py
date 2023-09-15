"""
File in charge of installing docker on the system
"""

import disp
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
        # ---- TTY rebinds ----
        self.print_on_tty = self.tty.print_on_tty
        self.run = self.tty.run_command
        self.function_help = self.tty.function_help
        # ---- Installer links ----
        self.docker_windows = "https://desktop.docker.com/win/main/amd64/Docker%20Desktop%20Installer.exe"
        self.docker_mac_intel = "https://desktop.docker.com/mac/main/amd64/Docker.dmg"
        self.docker_mac_arm = "https://desktop.docker.com/mac/main/arm64/Docker.dmg"

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

    def install_for_mac(self) -> int:
        pass

    def install_for_linux(self) -> int:
        pass

    def install_for_windows(self) -> int:
        pass

    def main(self) -> int:
        """ The workflow dispatcher """
        current_system = system()
        if current_system == "Windows":
            return self.install_for_windows()
        elif current_system == "Linux":
            return self.install_for_linux()
        elif current_system == "Darwin" or current_system == "Java":
            return self.install_for_mac()
