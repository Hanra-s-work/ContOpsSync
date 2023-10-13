"""
File in charge of containing the docker installation for windows systems
"""


import display_tty
import requests
from tqdm import tqdm
from tty_ov import TTY


class InstallDockerWindows:
    """ The class in charge of installing docker on a Windows """

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
        self.installer_path = "https://desktop.docker.com/win/main/amd64/Docker%20Desktop%20Installer.exe"
        # ---- destination file ----
        self.destination_file = "docker_installer.exe"

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

    def is_wsl_installed(self) -> bool:
        """ Check if wsl is installed """
        self.print_on_tty(
            self.tty.info_colour,
            "Checking if wsl is installed:\n"
        )
        self.tty.current_tty_status = self.run(
            [
                "wsl",
                "--version",
                ">nul",
                "2>nul"
            ]
        )
        self.print_on_tty(
            self.tty.info_colour,
            "WSL status: "
        )

        if self.tty.current_tty_status != self.tty.success:
            self.print_on_tty(self.tty.error_colour, "[KO]\n")
            return False
        self.print_on_tty(self.tty.success_colour, "[OK]\n")
        self.tty.current_tty_status = self.tty.success
        return True

    def restart_prompt(self) -> int:
        """ Prompt the user to restart his computer """
        self.print_on_tty(
            self.tty.info_colour,
            "Please restart your computer when you can\n"
        )
        reponse = self.tty.ask_question.ask_question(
            "Do you wish to restart your computer?",
            "bool"
        )
        if reponse == True:
            self.print_on_tty(
                self.tty.info_colour,
                "Restarting computer\n"
            )
            self.tty.current_tty_status = self.run(
                [
                    "shutdown",
                    "/r",
                    "/t 10"
                ]
            )
        self.tty.current_tty_status = self.tty.success
        return self.tty.current_tty_status

    def install_wsl(self) -> int:
        """ Install wsl """
        self.print_on_tty(
            self.tty.info_colour,
            "Installing wsl:\n"
        )
        self.tty.current_tty_status = self.run(
            [
                "powershell",
                "-ExecutionPolicy Bypass",
                "-Command ",
                "\"Start-Process",
                "powershell",
                "-Verb RunAs",
                "-ArgumentList '",
                "Enable-WindowsOptionalFeature",
                "-Online",
                "-FeatureName",
                "Microsoft-Windows-Subsystem-Linux",
                "-NoRestart"
                "'\"",
                ";",
                "exit $LASTEXITCODE"
            ]
        )
        self.print_on_tty(
            self.tty.info_colour,
            "WSL installation status: "
        )

        if self.tty.current_tty_status != self.tty.success:
            self.print_on_tty(self.tty.error_colour, "[KO]\n")
            return self.err
        self.print_on_tty(self.tty.success_colour, "[OK]\n")
        self.disp.sub_title("Setting wsl2 as default")
        status = self.run(
            [
                "wsl",
                "--set-default-version",
                "2"
            ]
        )
        self.print_on_tty(
            self.tty.info_colour,
            "Setting wsl2 as default status:"
        )
        if status != self.success:
            self.print_on_tty(self.tty.error_colour, "[KO]\n")

            return self.tty.error
        self.print_on_tty(self.tty.success_colour, "[OK]\n")
        self.tty.current_tty_status = self.tty.success
        return self.success

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
                ">nul",
                "2>nul"
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
        self.disp.sub_sub_title("Downloading docker executable")
        status = self._download_file(
            self.installer_path,
            self.destination_file
        )
        self.print_on_tty(
            self.tty.info_colour,
            "Download status:"
        )
        if status != self.success:
            self.print_on_tty(self.tty.error_colour,"[KO]\n")
            return self.err
        self.print_on_tty(self.tty.success_colour,"[OK]\n")
        return self.tty.current_tty_status

    def _install_docker_via_script(self) -> int:
        """ Install docker via the script """
        self.print_on_tty(self.tty.info_colour, "")
        self.disp.sub_sub_title("Installing docker via the executable")
        self.print_on_tty(
            self.tty.info_colour,
            "Installing docker via script:"
        )
        status = self.super_run(
            [
                self.destination_file
            ]
        )
        self.print_on_tty(
            self.tty.info_colour,
            "Installation status (docker):"
        )
        if status != self.tty.success:
            self.print_on_tty(self.tty.error_colour,"[KO]\n")
            return self.err
        self.print_on_tty(self.tty.success_colour,"[OK]\n")
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
                ">nul",
                "2>nul"
            ]
        )
        self.print_on_tty(
            self.tty.info_colour,
            "Installation status (docker):"
        )
        if status != self.tty.success:
            self.print_on_tty(self.tty.error_colour,"[KO]\n")
            return self.err
        self.print_on_tty(self.tty.success_colour,"[OK]\n")
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
            self.print_on_tty(self.tty.error_colour,"[KO]\n")
            return self.err
        self.print_on_tty(self.tty.success_colour,"[OK]\n")
        return self.tty.current_tty_status

    def main(self) -> int:
        """ Install docker on the current system """
        self.print_on_tty(self.tty.info_colour, "")
        self.disp.sub_title("Installing docker")
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

    def test_class_install_docker_windows(self) -> None:
        """ Test the class install docker Windows """
        self.print_on_tty(
            self.tty.info_colour,
            "This is a test message from the install docker Windows class"
        )
