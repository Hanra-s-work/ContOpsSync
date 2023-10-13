"""
File in charge of linking the docker installation scripts
"""

from tty_ov import TTY
from .install_docker_linux import InstallDockerLinux
from .install_docker_mac import InstallDockerMac
from .install_docker_raspberry_pi import InstallDockerRaspberryPi
from .install_docker_windows import InstallDockerWindows


class InstallDockerInit:
    """ Install docker on your system """

    def __init__(self, tty: TTY, success: int = 0, err: int = 84, error: int = 84) -> None:
        self.install_docker_windows = InstallDockerWindows(
            tty,
            success,
            err,
            error
        )
        self.install_docker_mac = InstallDockerMac(tty, success, err, error)
        self.install_docker_linux = InstallDockerLinux(
            tty,
            success,
            err,
            error
        )
        self.install_docker_raspberrypi = InstallDockerRaspberryPi(
            tty,
            success,
            err,
            error
        )

    def test_class_install_docker(self) -> None:
        """ Test the class InstallDocker """
        self.install_docker_windows.test_class_install_docker_windows()
        self.install_docker_mac.test_class_install_docker_mac()
        self.install_docker_linux.test_class_install_docker_linux()
        self.install_docker_raspberrypi.test_class_install_docker_raspberry_pi()
