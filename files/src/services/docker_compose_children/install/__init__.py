"""
File in charge of linking the docker installation scripts
"""

from tty_ov import TTY
from .install_docker_compose_linux import InstallDockerComposeLinux
from .install_docker_compose_mac import InstallDockerComposeMac
from .install_docker_compose_raspberry_pi import InstallDockerComposeRaspberryPi
from .install_docker_compose_windows import InstallDockerComposeWindows


class InstallDockerComposeInit:
    """ Install docker on your system """

    def __init__(self, tty: TTY, success: int = 0, err: int = 84, error: int = 84) -> None:
        self.install_docker_windows = InstallDockerComposeWindows(
            tty,
            success,
            err,
            error
        )
        self.install_docker_mac = InstallDockerComposeMac(
            tty,
            success,
            err,
            error
        )
        self.install_docker_linux = InstallDockerComposeLinux(
            tty,
            success,
            err,
            error
        )
        self.install_docker_raspberrypi = InstallDockerComposeRaspberryPi(
            tty,
            success,
            err,
            error
        )

    def test_class_install_docker_compose(self, args: list) -> None:
        """ Test the class InstallDocker """
        self.install_docker_windows.test_class_install_docker_compose_windows()
        self.install_docker_mac.test_class_install_docker_compose_mac()
        self.install_docker_linux.test_class_install_docker_compose_linux()
        self.install_docker_raspberrypi.test_class_install_docker_compose_raspberry_pi()
