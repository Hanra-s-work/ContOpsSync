"""
File containing the Docker class in charge of managing the Docker services
"""

from tty_ov import TTY
from .docker_children import DockerChildren


class Docker:
    """ The class in charge of managin the docker images """

    def __init__(self, success, err, error, tty: TTY) -> None:
        self.success = success
        self.err = err
        self.error = error
        self.tty = tty
        # ---- Docker child components ----
        self.docker_children = DockerChildren(tty, success, err, error)
        # ---- TTY Docker options ----
        self.options = []

    def docker_class_test(self, args: list) -> int:
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
            "\tThis means that the Docker class has correctly been imported\n"
        )
        self.tty.current_tty_status = self.success
        return self.tty.current_tty_status

    def save_commands(self) -> None:
        """ The function in charge of saving the commands to the options list """
        self.options = [
            {
                "docker_class_test":  self.docker_class_test,
                "desc": "A test function for the Docker class"
            }
        ]
        self.docker_children.inject_child_ressources(self.options)

    def injector(self) -> int:
        """ The function in charge of injecting the kubernetes class into the main class """
        self.save_commands()
        return self.tty.import_functions_into_shell(self.options)

    def run(self, image: str, port: int) -> None:
        """ Run a docker image """
        pass

    def stop(self, image: str) -> None:
        """ Stop a docker image """
        pass

    def remove(self, image: str) -> None:
        """ Remove a docker image """
        pass

    def list_containers(self) -> None:
        """ List the running containers """
        pass

    def list_all_containers(self) -> None:
        """ List all the containers contained in memory """
        pass

    def list_images(self) -> None:
        """ List the images present on the system """
        pass
