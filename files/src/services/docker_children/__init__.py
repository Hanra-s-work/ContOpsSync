"""
File in charge of gathering the sub-classes for managing docker
"""
from tty_ov import TTY
from .install_manager import InstallDocker
from .build import BuildImage
from .run import RunImage


class DockerChildren:
    """ The dependencies used by the Docker class """

    def __init__(self, tty: TTY, success: int, err: int, error: int) -> None:
        # ---- Status codes ----
        self.success = success
        self.err = err
        self.error = error
        # ---- Inherited classes ----
        self.tty = tty
        # ---- Child classes ----
        self.install_docker = InstallDocker(tty, success, err, error)
        self.build_image = BuildImage(tty, success, err, error)
        self.run_image = RunImage(tty, success, err, error)

    def test_children(self) -> int:
        """ The function in charge of testing the children """
        self.tty.print_on_tty(
            self.tty.info_colour,
            "This is a test message from the DockerChildren class\n"
        )
        self.install_docker.test_install_docker([])
        self.build_image.test_class_build_docker_image()
        self.run_image.test_class_run_docker_image()
        return self.success

    def inject_child_ressources(self, parent_options: list[dict]) -> int:
        """ Injects all child ressources into the parent ressource list """
        content = self.install_docker.save_commands()
        parent_options.extend(content)
        content = self.build_image.save_commands()
        parent_options.extend(content)
        content = self.run_image.save_commands()
        parent_options.extend(content)
