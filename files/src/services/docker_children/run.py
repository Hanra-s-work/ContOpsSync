"""
File in charge of containing the code to build a docker image
"""

import os
from platform import system
from tty_ov import TTY
import display_tty


class RunImage:
    """ Build the docker image for a user """

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

    def _run_docker_command(self, command: list, hide_output: bool = False) -> int:
        """ Run a docker command """
        compiled_command = []
        if self.system_name == "Windows":
            compiled_command.append("docker")
            compiled_command.extend(command)
            if hide_output is True:
                compiled_command.extend(
                    [
                        ">nul",
                        "2>nul"
                    ]
                )
        else:
            compiled_command.extend(
                [
                    "sudo",
                    "docker"
                ]
            )
            compiled_command.extend(command)
            if hide_output is True:
                compiled_command.extend(
                    [
                        ">/dev/null",
                        "2>/dev/null"
                    ]
                )
        status = self.run(compiled_command)
        return status

    def run_image(self, args: list) -> int:
        """ Build a docker image """
        function_name = "run_image"
        if self.tty.help_function_child_name == function_name:
            help_description = f"""
Run a docker image
PS: When an image gets run, it becomes a container
Usage Example:
Input:
    {function_name} <image_name> <container_name_(optional)> <ports_(optional)> <volumes_(optional)> <interactive_[allows_you_to_access_the_content_of_the_container_via_your_terminal]_(optional)> <background_[start_in_the_background]_(optional)> -my<other_arguments_you_wish_to_pass>
Output:
    Build a docker image
PS: This function still needs to be written
"""
            self.tty.function_help(function_name, help_description)
            self.tty.current_tty_status = self.tty.success
            return self.success
        self.print_on_tty(
            self.tty.info_colour,
            "This is a test message from the BuildImage class\n"
        )
        argc = len(args)
        image_name = ""
        dockerfile_path = ""
        version = ""
        default_version = "latest"
        default_path = "."
        if argc == 0:
            self.print_on_tty(
                self.tty.error_colour,
                "No image name provided\n"
            )
            self.tty.current_tty_status = self.err
            return self.err
        if argc == 1:
            image_name = args[0]
            self.print_on_tty(
                self.tty.info_colour,
                f"No build path provided, assuming that it is '{default_path}'\n"
            )
            image_name = default_path
            self.print_on_tty(
                self.tty.info_colour,
                f"No version provided, assuming that it is '{default_version}'\n"
            )
            version = default_version
        if argc == 2:
            image_name = args[0]
            dockerfile_path = args[1]
            self.print_on_tty(
                self.tty.info_colour,
                f"No version provided, assuming that it is '{default_version}'\n"
            )
            version = default_version

        if argc == 3:
            image_name = args[0]
            dockerfile_path = args[1]
            version = args[2]

        if os.path.exists(dockerfile_path) is False:
            self.print_on_tty(
                self.tty.error_colour,
                f"Path '{dockerfile_path}' does not exist\n"
            )
            self.tty.current_tty_status = self.err
            return self.err
        self.print_on_tty(
            self.tty.info_colour,
            f"Building image '{image_name}'\n"
        )
        self.print_on_tty(
            self.tty.info_colour,
            f"Using dockerfile '{dockerfile_path}'\n"
        )
        self.print_on_tty(
            self.tty.info_colour,
            f"Using version '{version}'\n"
        )
        self.print_on_tty(
            self.tty.info_colour,
            f"Building image '{image_name}:{version}'\n"
        )
        status = self._run_docker_command(
            [
                "run",
                f"{image_name}:{version}",
                dockerfile_path
            ]
        )
        self.print_on_tty(
            self.tty.info_colour,
            "Docker build status:"
        )
        if status != self.tty.success:
            self.print_on_tty(self.tty.error_colour, "[KO]\n")
            self.print_on_tty(
                self.tty.error_colour,
                "Build failed, please check the error on top of the problem\n"
            )
            return self.err
        self.print_on_tty(self.tty.success_colour, "[OK]\n")
        self.tty.current_tty_status = self.success
        return self.success

    def is_image_run(self, args: list) -> bool:
        """ Check if the image is built """
        function_name = "is_image_run"
        if self.tty.help_function_child_name == function_name:
            help_description = f"""
Check if the image is built
PS: when an Image gets run, it becomes a container.
Usage Example:
Input:
    {function_name} <container_name>
Output:
    Displays [OK] if the container is present.
    Displays [KO] if the container is not present.
"""
            self.tty.function_help(function_name, help_description)
            self.tty.current_tty_status = self.tty.success
            return self.success
        argc = len(args)
        container_name = ""
        version = ""
        if argc == 0:
            self.print_on_tty(
                self.tty.error_colour,
                "No container name provided\n"
            )
            self.tty.current_tty_status = self.err
            return self.err
        if argc == 1:
            container_name = args[0]
        if argc == 2:
            container_name = args[0]
            version = args[1]
        self.print_on_tty(
            self.tty.info_colour,
            f"Checking if container '{container_name}:{version}' is built\n"
        )
        status = self._run_docker_command(
            [
                "containers",
                "-q",
                f"{container_name}:{version}"
            ]
        )
        self.print_on_tty(
            self.tty.info_colour,
            "Docker container status:"
        )
        if status != self.tty.success:
            self.print_on_tty(self.tty.error_colour, "[KO]\n")
            return False
        self.print_on_tty(self.tty.success_colour, "[OK]\n")
        return True

    def main(self, args: list) -> int:
        """ The main function of the class """
        return self.run_image(args)

    def test_class_run_docker_image(self, args: list) -> None:
        """ Tests the method 'build_docker_image' """
        function_name = "test_class_run_docker_image"
        if self.tty.help_function_child_name == function_name:
            help_description = f"""
Make sure the run Docker classes are loaded
Usage Example:
Input:
    {function_name}
Output:
    A message from each class informing that they are loaded
"""
            self.tty.function_help(function_name, help_description)
            self.tty.current_tty_status = self.tty.success
            return self.success
        self.print_on_tty(
            self.tty.info_colour,
            "This is a test message from the Build Image class from Docker.\n"
        )

    def save_commands(self) -> list[dict]:
        """ The function in charge of saving the commands to the options list """
        self.options = [
            {
                "run_image": self.run_image,
                "desc": "Build a docker image"
            },
            {
                "is_image_run": self.is_image_run,
                "desc": "Check if the image is running"
            },
            {
                "test_class_run_docker_image": self.test_class_run_docker_image,
                "desc": "Test the class"
            }
        ]
        return self.options
