"""
File containing the DockerCompose class in charge of managing the Docker-Compose services
"""

import os
from tty_ov import TTY


class DockerCompose:
    """ The class in charge of managing the docker-compose.yml file """

    def __init__(self, success, err, error, tty: TTY) -> None:
        self.success = success
        self.err = err
        self.error = error
        self.tty = tty
        # ---- TTY Docker Compose options ----
        self.options = []

    def docker_compose_class_test(self, args: list) -> int:
        """ This is a test to check that the classe's function has correctly imported """
        self.tty.print_on_tty(
            self.tty.success_colour,
            "This is a test message.\n"
        )
        self.tty.print_on_tty(
            self.tty.success_colour,
            "If you see this message:\n"
        )
        self.tty.print_on_tty(
            self.tty.success_colour,
            "\tThis means that the Docker_compose class has correctly been imported\n"
        )
        self.tty.current_tty_status = self.success
        return self.tty.current_tty_status

    def save_commands(self) -> None:
        """ The function in charge of saving the commands to the options list """
        self.options = [
            {
                "docker_compose_class_test":  self.docker_compose_class_test,
                "desc": "A test function for the Docker Compose class"
            }
        ]

    def injector(self) -> int:
        """ The function in charge of injecting the docker_compose class into the main class """
        self.save_commands()
        return self.tty.import_functions_into_shell(self.options)

    def build(self, path: str, tag: str) -> None:
        """ Build a docker-compose image """
        pass

    def run(self, image: str, port: int) -> None:
        """ Run a docker-compose image """
        pass

    def stop(self, image: str) -> None:
        """ Stop a docker-compose image """
        pass

    def remove(self, image: str) -> None:
        """ Remove a docker-compose image """
        pass

    def rebuild(self, image: str) -> None:
        """ Rebuild a docker-compose container from scratch """
        pass

    def main(self) -> int:
        """ The Prompt for the docker-compose class """
        print("This is the main class")
        return self.success
