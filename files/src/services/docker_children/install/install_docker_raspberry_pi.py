"""
File in charge of installing docker on a raspberry pi
"""

import display_tty
import requests
from tqdm import tqdm
from tty_ov import TTY


class InstallDockerRaspberryPi:
    """ The class in charge of installing docker on a raspberry pi """

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
        self.installer_path = "https://get.docker.com"
        # ---- destination file ----
        self.destination_file = "/tmp/docker_install.sh"

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

    def is_docker_installed(self) -> bool:
        """ Returns true if Docker is installed """
        self.print_on_tty(
            self.tty.info_colour,
            "Checking if Docker is installed:\n"
        )
        self.tty.current_tty_status = self.run(
            [
                "docker",
                "--version",
                ">/dev/null",
                "2>/dev/null"
            ]
        )
        self.print_on_tty(
            self.tty.info_colour,
            "Docker status: "
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

    def _installation_error_message(self) -> None:
        """ Print the error message """
        self.print_on_tty(
            self.tty.error_colour,
            "Error installing docker\n"
        )

    def _download_script(self) -> int:
        """ Dowload the installer script """
        self.print_on_tty(self.tty.info_colour, "")
        self.disp.sub_sub_title("Downloading docker install script")
        status = self._download_file(
            self.installer_path,
            self.destination_file
        )
        self.print_on_tty(
            self.tty.info_colour,
            "Download status:"
        )
        if status != self.success:
            self.print_on_tty(self.tty.error_colour, "[KO]\n")
            return self.err
        self.print_on_tty(self.tty.success_colour, "[OK]\n")
        return self.tty.current_tty_status

    def _install_docker_via_script(self) -> int:
        """ Install docker via the script """
        self.print_on_tty(self.tty.info_colour, "")
        self.disp.sub_sub_title("Installing docker via the script")
        self.print_on_tty(
            self.tty.info_colour,
            "Installing docker via script:"
        )
        status = self.super_run(
            [
                "chmod",
                "+x",
                self.destination_file,
                "&&",
                self.destination_file
            ]
        )
        self.print_on_tty(
            self.tty.info_colour,
            "Installation status (docker):"
        )
        if status != self.tty.success:
            self.print_on_tty(self.tty.error_colour, "[KO]\n")
            return self.err
        self.print_on_tty(self.tty.success_colour, "[OK]\n")
        return self.tty.current_tty_status

    def _test_docker_installation(self) -> int:
        """ Test the docker installation """
        self.print_on_tty(self.tty.info_colour, "")
        self.disp.sub_sub_title("Testing docker installation")
        self.print_on_tty(
            self.tty.info_colour,
            "Testing docker installation:"
        )
        status = self.run(
            [
                "docker",
                "--version",
                ">/dev/null",
                "2>/dev/null"
            ]
        )
        self.print_on_tty(
            self.tty.info_colour,
            "Installation status (docker):"
        )
        if status != self.tty.success:
            self.print_on_tty(self.tty.error_colour, "[KO]\n")
            return self.err
        self.print_on_tty(self.tty.success_colour, "[OK]\n")
        return self.tty.current_tty_status

    def _test_docker_functionalities(self) -> int:
        """ Testing Docker's capability to pull a hello-world image """
        self.print_on_tty(self.tty.info_colour, "")
        self.disp.sub_sub_title("Testing docker functionalities")
        self.print_on_tty(
            self.tty.info_colour,
            "Testing docker functionalities:"
        )
        self.print_on_tty(self.tty.info_colour, "Pulling hello-world image")
        status = self.run(
            [
                "docker",
                "pull",
                "hello-world"
            ]
        )
        self.print_on_tty(self.tty.info_colour, "Running hello-world image")
        status = self.run(
            [
                "docker",
                "run",
                "hello-world"
            ]
        )
        self.print_on_tty(
            self.tty.info_colour,
            "Functionality status (docker):"
        )
        if status != self.tty.success:
            self.print_on_tty(self.tty.error_colour, "[KO]\n")
            return self.err
        self.print_on_tty(self.tty.success_colour, "[OK]\n")
        return self.tty.current_tty_status

    def main(self) -> int:
        """ Install docker on the current system """
        self.print_on_tty(self.tty.info_colour, "")
        self.disp.sub_title("Installing docker")
        if self.is_raspberrypi() is False:
            self.print_on_tty(
                self.tty.error_colour,
                "This is not a raspberry pi, please use the correct installer"
            )
            return self.err
        status = self._download_script()
        if status != self.success:
            self._installation_error_message()
            return self.err
        status = self._install_docker_via_script()
        if status != self.success:
            self._installation_error_message()
            return self.err
        status = self._test_docker_installation()
        if status != self.success:
            self._installation_error_message()
            return self.err
        status = self._test_docker_functionalities()
        if status != self.success:
            self._installation_error_message()
            return self.err
        self.print_on_tty(
            self.tty.success_colour,
            "Docker installed successfully\n"
        )
        return self.success

    def test_class_install_docker_raspberry_pi(self) -> None:
        """ Test the class install docker raspberry pi """
        self.print_on_tty(
            self.tty.info_colour,
            "This is a test message from the install docker raspberry pi class\n"
        )
