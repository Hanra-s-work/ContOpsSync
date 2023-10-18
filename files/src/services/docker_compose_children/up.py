"""
File in charge of helping the user to bring a docker-compose image up
"""

import os
from platform import system
from tty_ov import TTY
import display_tty


class DockerComposeUp:
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
        self.super_run = self.tty.run_as_admin
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
                        "-d"
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
                        "-d"
                    ]
                )
        status = self.run(compiled_command)
        return status

    def docker_compose_up(self, args: list) -> int:
        """ Run the docker-compose up command """
        function_name = "docker_compose_up"
        if self.tty.help_function_child_name == function_name:
            help_description = f"""
Build/Run a docker-compose image
Usage Example:
Input:
    {function_name} (<docker_compose_file_path> or <service_name>) [background] [rebuild] [usual_docker_compose_args]
Output:
    Build (if required) then run the docker-compose image
Example:
Input (Building a docker-compose image based on the file_path):
    {function_name} ./docker-compose.yml
Output:
    (if required): The build process of the docker-compose
    The start process of the docker-compose

Input (Building a docker-compose image based on the service_name):
    {function_name} my_service
Output:
    (if required): The build process of the docker-compose
    The start process of the docker-compose

Input (Rebuilding a docker-compose image):
    {function_name} ./docker-compose.yml rebuild
Output:
    The removal process of the current docker-compose
    The build process of the docker-compose
    The start process of the docker-compose
"""
            self.tty.function_help(function_name, help_description)
            self.tty.current_tty_status = self.tty.success
            return self.success
        docker_compose_file_path = ""
        build_in_the_background = False
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
            build_in_the_background = True
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
                    "all"
                ]
            )
            if status != self.success:
                self.print_on_tty(
                    self.tty.info_colour,
                    "Docker-compose up status:"
                )
                self.print_on_tty(self.tty.error_colour, "[KO]\n")
                self.print_on_tty(
                    self.tty.error_colour,
                    "Error while removing the current docker-compose image\n"
                )
                self.tty.current_tty_status = self.err
                return self.err

            # Build the docker-compose image.
            status = self._run_docker_compose_command(
                [
                    "up",
                    "--build",
                    docker_compose_file_path
                ],
                hide_output=build_in_the_background
            )

            if status != self.success:
                self.print_on_tty(
                    self.tty.info_colour,
                    "Docker-compose up status:"
                )
                self.print_on_tty(self.tty.error_colour, "[KO]\n")
                self.print_on_tty(
                    self.tty.error_colour,
                    "Error while building the docker-compose image\n"
                )
                self.tty.current_tty_status = self.err
                return self.err
            self.print_on_tty(
                self.tty.info_colour,
                "Docker-compose up status:"
            )
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
                    "Docker-compose up status:"
                )
                self.print_on_tty(self.tty.error_colour, "[KO]\n")
                return self.error
        compose_commands = ["up", docker_compose_file_path]
        compose_commands.extend(docker_compose_args)
        self._run_docker_compose_command(
            compose_commands,
            hide_output=build_in_the_background
        )
        self.print_on_tty(
            self.tty.info_colour,
            "Docker-compose up status:"
        )
        if self.tty.current_tty_status != self.success:
            self.print_on_tty(self.tty.error_colour, "[KO]\n")
        self.print_on_tty(self.tty.success_colour, "[OK]\n")
        return self.tty.current_tty_status

    def save_commands(self) -> list:
        """ The function in charge of saving the commands to the options list """
        options = [
            {
                "docker_compose_up":  self.docker_compose_up,
                "desc": "Build/Run a docker-compose image"
            },
            {
                "test_docker_compose_up":  self.test_docker_compose_up,
                "desc": "Test the docker-compose up class"
            }
        ]
        return options

    def main(self, args: list) -> int:
        """ The main function of the program """
        return self.docker_compose_up(args)

    def test_docker_compose_up(self, args: list) -> int:
        """ Test the docker-compose class """
        self.print_on_tty(
            self.tty.info_colour,
            "This is a test message from the DockerComposeUp class\n"
        )
        return self.success
