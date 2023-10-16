"""
Class in charge of forcing k3s to use Docker when it starts
"""

import display_tty
from tty_ov import TTY


class ForceDockerLinux:
    """ The class in charge of forcing docker for the system """

    def __init__(self, tty: TTY, success: int = 0, err: int = 84, error: int = 84) -> None:
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
        # ---- Filepaths ----
        self.k3s_service_file = "/etc/systemd/system/k3s.service"
        # ---- Configuration filepath ----
        self.k3s_config_file = "/etc/rancher/k3s/k3s.yaml"

    def _is_docker_installed(self) -> bool:
        """ Check if docker is installed """
        self.print_on_tty(
            self.tty.info_colour,
            "Checking if docker is installed:\n"
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
            "Docker installation status:"
        )
        if status == self.success:
            self.print_on_tty(
                self.tty.success_colour,
                "[OK]\n"
            )
            return True
        self.print_on_tty(
            self.tty.error_colour,
            "[KO]\n"
        )
        return False

    def _create_backup(self, file_source: str) -> int:
        """ Create a backup of the file """
        self.print_on_tty(
            self.tty.info_colour,
            f"Creating a backup of file {file_source}:\n"
        )
        status = self.run(
            [
                "sudo"
                "cp",
                "--recursive",
                "--verbose",
                "--force",
                "--no-clobber",
                file_source,
                f"{file_source}.backup"
            ]
        )
        self.print_on_tty(
            self.tty.info_colour,
            "Backup status:"
        )
        if status == self.success:
            self.print_on_tty(
                self.tty.success_colour,
                "[OK]\n"
            )
            return self.success
        self.print_on_tty(
            self.tty.error_colour,
            "[KO]\n"
        )
        return self.error

    def _start_docker_on_k3s_boot(self) -> int:
        """ Start the docker service when k3s starts """
        self.print_on_tty(
            self.tty.info_colour,
            "Starting docker service on k3s boot:\n"
        )
        status = self.run(
            [
                "sudo",
                "sed",
                "-i",
                "s/containerd/docker/g",
                self.k3s_service_file
            ]
        )
        self.print_on_tty(
            self.tty.info_colour,
            "Service start edit status:"
        )
        if status == self.success:
            self.print_on_tty(
                self.tty.success_colour,
                "[OK]\n"
            )
            return self.success
        self.print_on_tty(
            self.tty.error_colour,
            "[KO]\n"
        )
        return self.error

    def _configuration_failed_message(self) -> None:
        """ Print the configuration failed message """
        self.print_on_tty(
            self.tty.error_colour,
            "K3s configuration status:"
        )
        self.print_on_tty(
            self.tty.error_colour,
            "[KO]\n"
        )

    def _update_the_config_file(self) -> int:
        """ Update the configuration file to use docker instead of containerd """
        self.print_on_tty(
            self.tty.info_colour,
            "Updating the configuration file to use docker instead of containerd:\n"
        )
        status = self.run(
            [
                "sudo",
                "sed",
                "-i",
                "s/containerd/docker/g",
                self.k3s_config_file
            ]
        )
        self.print_on_tty(
            self.tty.info_colour,
            "Configuration file update status:"
        )
        if status == self.success:
            self.print_on_tty(
                self.tty.success_colour,
                "[OK]\n"
            )
            return self.success
        self.print_on_tty(
            self.tty.error_colour,
            "[KO]\n"
        )
        return self.error

    def main(self) -> int:
        """ Force k3s to use docker """
        self.print_on_tty(self.tty.info_colour, "")
        self.disp.sub_title("Configuring k3s to use docker")
        self.print_on_tty(self.tty.info_colour, "Instead of containerd")
        status = self._is_docker_installed()
        if status is False:
            self.print_on_tty(
                self.tty.error_colour,
                "Could not configure k3s to use docker because it is not installed\n"
            )
            self.print_on_tty(
                self.tty.error_colour,
                "Please install docker and try again\n"
            )
            self._configuration_failed_message()
            return self.error
        self.print_on_tty(
            self.tty.info_colour,
            "Configuring k3s to use docker:\n"
        )
        status = self._create_backup(self.k3s_service_file)
        status2 = self._create_backup(self.k3s_config_file)
        if status != self.success or status2 != self.success:
            self.print_on_tty(
                self.tty.error_colour,
                "Could not configure k3s to use docker because the backup could not be created\n"
            )
            self._configuration_failed_message()
            return self.error
        status = self._start_docker_on_k3s_boot()
