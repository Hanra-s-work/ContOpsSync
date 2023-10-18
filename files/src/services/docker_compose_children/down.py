"""
File in charge of helping the user to bring a docker-compose image down
"""

import os
from platform import system
from tty_ov import TTY
import display_tty


class DockerComposeDown:
    """ Class in charge of helping the user into the task of building a docker-compose file """

    def __init__(self, tty: TTY, success: int = 0, err: int = 84, error: int = 84) -> None:
        self.success = success
        self.err = err
        self.error = error
        self.options = []
        self.system_name = system()
        # ---- The TTY options ----
        self.tty = tty
        self.print_on_tty = self.tty.print_on_tty
        self.sdowner_run = self.tty.run_as_admin
        self.run = self.tty.run_command
        # ---- The Disp option ----
        self.disp = display_tty.IDISP
        self.disp.toml_content["PRETTIFY_OUTPUT"] = False
        self.disp.toml_content["PRETTY_OUTPUT_IN_BLOCS"] = False

    def _run_docker_compose_command(self, command: list, hide_output: bool = False) -> int:
        """ Run a docker-compose command """
        compiled_command = []
        if self.system_name == "Windows":
            compiled_command.append("docker-compose")
            compiled_command.extend(command)
            if hide_output is True:
                compiled_command.extend(
                    [
                        ">/dev/null",
                        "2>/dev/null"
                    ]
                )
        else:
            compiled_command.extend(
                [
                    "sudo",
                    "docker-compose"
                ]
            )
            compiled_command.extend(command)
            if hide_output is True:
                compiled_command.extend(
                    [
                        ">nul",
                        "2>nul"
                    ]
                )
        status = self.run(compiled_command)
        return status

    def docker_compose_down(self, args: list) -> int:
        """ Run the docker-compose down command """
        function_name = "docker_compose_down"
        if self.tty.help_function_child_name == function_name:
            help_description = f"""
Stop/Remove a docker-compose image
Usage Example:
Input:
    {function_name} (<docker_compose_file_path> or <service_name>) [background] [remove] [usual_docker_compose_args]
Output:
    Stop the docker-compose image (if specified, remove the image)
Example:
Input (Stopping a docker-compose image based on the file_path):
    {function_name} ./docker-compose.yml
Output:
    The start process of the docker-compose

Input (Stopping a docker-compose image based on the service_name):
    {function_name} my_service
Output:
    The start process of the docker-compose

Input (Stopping and removing a docker-compose image):
    {function_name} ./docker-compose.yml remove
Output:
    The ending process of the current docker-compose
    The removal process of the docker-compose
"""
            self.tty.function_help(function_name, help_description)
            self.tty.current_tty_status = self.tty.success
            return self.success
        docker_compose_file_path = ""
        stop_in_the_background = False
        # Check if there is at least one argument (docker_compose_file).
        if len(args) < 1:
            self.print_on_tty(
                self.tty.info_colour,
                "Assuming that the file path is '.'\n"
            )
            docker_compose_file_path = "."
        else:
            # The first argument is the docker_compose_file_path.
            docker_compose_file_path = args[0]
            args = args[:1]

        if len(args) >= 1 and "background" in args[0].lower():
            stop_in_the_background = True
            args = args[1:]

        if len(args) >= 1 and args[0].lower() == "rebuild":
            # If the second argument is "rebuild", remove it from the list of arguments.
            args = args[1:]

            # Remove the current docker-compose image.
            status = self._run_docker_compose_command(
                [
                    "-f",
                    docker_compose_file_path,
                    "down",
                    "--rmi",
                    "all",
                ],
                hide_output=stop_in_the_background
            )
            self.print_on_tty(
                self.tty.info_colour,
                "Docker-compose down status:"
            )
            if status != self.success:
                self.print_on_tty(
                    self.tty.info_colour,
                    "Docker-compose down status:"
                )
                self.print_on_tty(self.tty.error_colour, "[KO]\n")
                self.print_on_tty(
                    self.tty.error_colour,
                    "Error while removing the current docker-compose image\n"
                )
                self.tty.current_tty_status = self.err
                return self.err
            self.print_on_tty(self.tty.success_colour, "[OK]\n")
            return self.tty.current_tty_status

        docker_compose_args = []

        for arg in args:
            if arg[0] == "-":
                docker_compose_args.append(arg)
            else:
                self.print_on_tty(
                    self.tty.error_colour,
                    f"Error: Invalid argument '{arg}'."
                )
                self.print_on_tty(
                    self.tty.info_colour,
                    "Docker-compose down status:"
                )
                self.print_on_tty(self.tty.error_colour, "[KO]\n")
                return self.error
        compose_commands = ["down", docker_compose_file_path]
        compose_commands.extend(docker_compose_args)
        self._run_docker_compose_command(
            compose_commands,
            hide_output=stop_in_the_background
        )
        self.print_on_tty(
            self.tty.info_colour,
            "Docker-compose down status:"
        )
        if self.tty.current_tty_status != self.success:
            self.print_on_tty(self.tty.error_colour, "[KO]\n")
        self.print_on_tty(self.tty.success_colour, "[OK]\n")
        return self.tty.current_tty_status

    def save_commands(self) -> list:
        """ The function in charge of saving the commands to the options list """
        options = [
            {
                "docker_compose_down":  self.docker_compose_down,
                "desc": "Build/Run a docker-compose image"
            },
            {
                "test_docker_compose_down":  self.test_docker_compose_down,
                "desc": "Test the docker-compose down class"
            }
        ]
        return options

    def main(self, args: list) -> int:
        """ The main function of the program """
        return self.docker_compose_down(args)

    def test_docker_compose_down(self, args: list) -> int:
        """ Test the docker-compose class """
        self.print_on_tty(
            self.tty.info_colour,
            "This is a test message from the DockerComposeDown class\n"
        )
        return self.success
