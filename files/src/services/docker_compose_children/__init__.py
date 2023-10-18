"""
File in charge of gathering the sub-classes for managing docker-compose
"""
from tty_ov import TTY
from .install_manager import InstallDockerCompose
from .up import DockerComposeUp
from .down import DockerComposeDown


class DockerComposeChildren:
    """ The dependencies used by the Docker class """

    def __init__(self, tty: TTY, success: int, err: int, error: int) -> None:
        # ---- Status codes ----
        self.success = success
        self.err = err
        self.error = error
        # ---- Inherited classes ----
        self.tty = tty
        # ---- Child classes ----
        self.install_docker_compose = InstallDockerCompose(
            tty,
            success,
            err,
            error
        )
        self.up = DockerComposeUp(tty, success, err, error)
        self.down = DockerComposeDown(tty, success, err, error)

    def test_children(self) -> int:
        """ The function in charge of testing the children """
        self.tty.print_on_tty(
            self.tty.info_colour,
            "This is a test message from the DockerChildren class\n"
        )
        self.install_docker_compose.test_install_docker_compose([])
        self.up.test_docker_compose_up([])
        self.down.test_docker_compose_down([])
        return self.success

    def inject_child_ressources(self, parent_options: list[dict]) -> int:
        """ Injects all child ressources into the parent ressource list """
        content = self.install_docker_compose.save_commands()
        parent_options.extend(content)
        content = self.up.save_commands()
        parent_options.extend(content)
        content = self.down.save_commands()
        parent_options.extend(content)
