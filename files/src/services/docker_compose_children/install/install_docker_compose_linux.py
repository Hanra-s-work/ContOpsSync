"""
File in charge of containing the docker installation for mac systems
"""


from time import sleep
from tty_ov import TTY
from tqdm import tqdm
import display_tty
import requests


class InstallDockerComposeLinux:
    """ The class in charge of installing docker on linux """

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
        # ---- temporary dockerfile ----
        self.temporary_dockerfile = "/tmp/docker_compose.yaml"
        # ---- Ping delay ----
        self.ping_delay = 100
        # ---- Docker port version ----
        self.docker_port_version = "5001"
        # ---- Ping url ----
        self.ping_url = f"http://localhost:{self.docker_port_version}"

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

    def is_docker_compose_installed(self) -> bool:
        """ Returns true if Docker-compose is installed """
        self.print_on_tty(
            self.tty.info_colour,
            "Checking if Docker-compose is installed:\n"
        )
        self.tty.current_tty_status = self.run(
            [
                "sudo",
                "docker-compose",
                "--version",
                ">/dev/null",
                "2>/dev/null"
            ]
        )
        self.print_on_tty(
            self.tty.info_colour,
            "Docker-compose status: "
        )

        if self.tty.current_tty_status != self.tty.success:
            self.print_on_tty(self.tty.error_colour, "[KO]\n")
            return False
        self.print_on_tty(self.tty.success_colour, "[OK]\n")
        self.tty.current_tty_status = self.tty.success
        return True

    def is_docker_installed(self) -> bool:
        """ Returns true if Docker is installed """
        self.print_on_tty(
            self.tty.info_colour,
            "Checking if Docker is installed:\n"
        )
        self.tty.current_tty_status = self.run(
            [
                "sudo",
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
        self.print_on_tty(
            self.tty.info_colour,
            "Adding you to the docker groupe\n"
        )
        self.run(
            [
                "sudo",
                "usermod",
                "-aG",
                "docker",
                "$USER"
            ]
        )
        if self.tty.current_tty_status != self.success:
            self.print_on_tty(
                self.tty.error_colour,
                "Error adding you to the docker groupe\n"
            )
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

    def _add_docker_to_the_user(self) -> int:
        """ Add the docker binary to the user groupe (grants it the same rights as the user) """
        self.print_on_tty(self.tty.info_colour, "")
        self.disp.sub_sub_title("Adding docker to the user")
        status = self.run(
            [
                "sudo",
                "usermod",
                "-aG",
                "docker",
                "$USER"
            ]
        )
        self.print_on_tty(
            self.tty.info_colour,
            "Adding docker to the user, status:"
        )
        if status != self.tty.success:
            self.print_on_tty(self.tty.error_colour, "[KO]\n")
            return self.err
        self.print_on_tty(self.tty.success_colour, "[OK]\n")
        return self.tty.current_tty_status

    def _has_pip(self) -> bool:
        """ Check if pip is installed """
        self.print_on_tty(
            self.tty.info_colour,
            "Checking if pip is installed:\n"
        )
        self.tty.current_tty_status = self.run(
            [
                "pip3",
                "--version",
                ">/dev/null",
                "2>/dev/null"
            ]
        )
        self.print_on_tty(
            self.tty.info_colour,
            "Pip status: "
        )
        if self.tty.current_tty_status != self.tty.success:
            self.print_on_tty(self.tty.error_colour, "[KO]\n")
            return False
        self.print_on_tty(self.tty.success_colour, "[OK]\n")
        self.tty.current_tty_status = self.tty.success
        return True

    def _ensure_pip(self) -> int:
        """ Ensure pip is installed """
        self.print_on_tty(self.tty.info_colour, "")
        self.disp.sub_sub_title("Ensuring pip is installed")
        self.print_on_tty(
            self.tty.info_colour,
            "Installing pip:"
        )
        status = self.run(
            [

                "sudo",
                "python3",
                "-m",
                "ensurepip",
                "--upgrade"
            ]
        )
        self.print_on_tty(
            self.tty.info_colour,
            "Installation status (pip):"
        )
        if status != self.tty.success:
            self.print_on_tty(self.tty.error_colour, "[KO]\n")
            return self.err
        self.print_on_tty(self.tty.success_colour, "[OK]\n")
        return self.tty.current_tty_status

    def _install_docker_compose_binary(self) -> int:
        """ Install docker-compose binary """
        self.print_on_tty(self.tty.info_colour, "")
        self.disp.sub_sub_title("Installing docker-compose binary")
        self.print_on_tty(
            self.tty.info_colour,
            "Installing docker-compose:"
        )
        status = self.run(
            [
                "sudo",
                "pip3",
                "install",
                "docker-compose"
            ]
        )
        self.print_on_tty(
            self.tty.info_colour,
            "Installation status (docker-compose):"
        )
        if status != self.tty.success:
            self.print_on_tty(self.tty.error_colour, "[KO]\n")
            return self.err
        self.print_on_tty(self.tty.success_colour, "[OK]\n")
        return self.tty.current_tty_status

    def _save_to_file(self, content: str = "", file_name: str = "a.txt") -> int:
        """ Save the content to a file """
        self.print_on_tty(self.tty.info_colour, "")
        self.disp.sub_sub_title("Saving content to a file")
        self.print_on_tty(
            self.tty.info_colour,
            f"Saving content to file: {file_name}"
        )
        try:
            with open(file_name, "w", encoding="utf-8", newline="\n") as file:
                file.write(content)
            self.print_on_tty(
                self.tty.success_colour,
                f"File saved to: {file_name}\n"
            )
            self.tty.current_tty_status = self.tty.success
            return self.tty.current_tty_status
        except Exception as err:
            self.print_on_tty(
                self.tty.error_colour,
                f"Error saving file: {err}\n"
            )
            self.tty.current_tty_status = self.tty.error
            return self.tty.current_tty_status

    def _deploy_docker_compose(self, file_path: str) -> int:
        """ Deploy a docker-compose.yaml file """
        self.print_on_tty(self.tty.info_colour, "")
        self.disp.sub_sub_title(f"Deploying {file_path} file")
        self.print_on_tty(
            self.tty.info_colour,
            f"Deploying docker-compose file: {file_path}"
        )
        status = self.run(
            [
                "docker-compose",
                "-f",
                file_path,
                "up",
                "-d"
            ]
        )
        self.print_on_tty(
            self.tty.info_colour,
            f"Deploying {file_path} file status:"
        )
        if status != self.tty.success:
            self.print_on_tty(self.tty.error_colour, "[KO]\n")
            return self.err
        self.print_on_tty(
            self.tty.success_colour,
            f"{file_path} file deployed successfully\n"
        )
        return self.tty.current_tty_status

    def _request_url_until_delay(self, url: str, delay: int) -> int:
        """ Request an URL until it's available or the delay is reached """
        self.print_on_tty(self.tty.info_colour, "")
        self.disp.sub_sub_title(
            f"Requesting {url} until delay or response is reached")
        self.print_on_tty(
            self.tty.info_colour,
            f"Requesting url: {url}"
        )
        try:
            request = requests.get(
                url,
                allow_redirects=True,
                timeout=delay,
                stream=True
            )
            self.print_on_tty(
                self.tty.success_colour,
                f"{url} requested successfully\n"
            )
            self.print_on_tty(
                self.tty.info_colour,
                f"request content: {request.content}"
            )
            if request.status_code == 200:
                self.tty.current_tty_status = self.tty.success
                return self.tty.current_tty_status
            self.tty.current_tty_status = self.tty.error
            return self.tty.current_tty_status
        except requests.RequestException as err:
            self.print_on_tty(
                self.tty.error_colour,
                f"Error requesting url: {err}\n"
            )
            self.tty.current_tty_status = self.tty.error
            return self.tty.current_tty_status
        except Exception:
            self.run(
                [
                    "wget",
                    url
                ]
            )
            return self.tty.current_tty_status

    def _testing_image_deployment(self, url: str) -> int:
        """ Querying the url to check if the image is up to date """
        self.print_on_tty(self.tty.info_colour, "")
        self.disp.sub_sub_title(
            f"Querying {url} to check if the image is up to date")
        status = self._request_url_until_delay(url, self.ping_delay)
        self.print_on_tty(
            self.tty.info_colour,
            f"Querying {url} status:"
        )
        if status != self.tty.success:
            self.print_on_tty(self.tty.error_colour, "[KO]\n")
            return self.err
        self.print_on_tty(self.tty.success_colour, "[OK]\n")
        return self.tty.current_tty_status

    def _test_docker_compose_installation(self) -> int:
        """ Try deploying a docker-compose.yaml file in order to test to see if the installation was successefull """
        docker_compose_file_content = f"""
version: '3'
services:
  webapp:
    ports:
      - {self.docker_port_version}:8000
    image: python:3.7-alpine
    command: "python -m http.server 8000
"""
        self.print_on_tty(self.tty.info_colour, "")
        self.disp.sub_sub_title("Testing docker-compose installation")
        status = self._save_to_file(
            docker_compose_file_content,
            self.temporary_dockerfile
        )
        if status != self.success:
            return self.error
        status = self._deploy_docker_compose(self.temporary_dockerfile)
        if status != self.success:
            return self.error
        sleep(1)
        status = self._testing_image_deployment(self.ping_url)
        return self.tty.success

    def _install_docker_compose(self) -> int:
        """ Install docker-compose """
        self.print_on_tty(self.tty.info_colour, "")
        self.disp.sub_title("Installing docker-compose")
        status = self._add_docker_to_the_user()
        if status != self.success:
            return self.error
        if self._has_pip() is False:
            status = self._ensure_pip()
            if status != self.success:
                return self.error
        status = self._install_docker_compose_binary()
        self.print_on_tty(
            self.tty.info_colour,
            "Docker-compose installation status:"
        )
        if status != self.success:
            self.print_on_tty(self.tty.error_colour, "[KO]\n")
            return self.error
        self.print_on_tty(self.tty.success_colour, "[OK]\n")
        status = self._test_docker_compose_installation()
        self.print_on_tty(
            self.tty.info_colour,
            "Docker-compose test status:"
        )
        if status != self.success:
            self.print_on_tty(self.tty.error_colour, "[KO]\n")
            return self.error
        self.print_on_tty(self.tty.success_colour, "[OK]\n")
        return self.tty.success

    def main(self) -> int:
        """ Install docker on the current system """
        self.print_on_tty(self.tty.info_colour, "")
        self.disp.sub_title("Installing docker")
        self.print_on_tty(self.tty.info_colour, "")
        self.disp.inform_message(
            "In order to install docker-compose, docker needs to be installed beforehand."
        )
        if self.is_docker_installed() is False:
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
        return self._install_docker_compose()

    def test_class_install_docker_compose_linux(self) -> None:
        """ Test the class install docker-compose Linux """
        self.print_on_tty(
            self.tty.info_colour,
            "This is a test message from the install docker-compose Linux class\n"
        )
