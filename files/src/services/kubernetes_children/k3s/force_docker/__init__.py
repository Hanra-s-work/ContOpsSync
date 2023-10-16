"""
File in charge of forcing k3s to use docker when starting up
"""

from tty_ov import TTY
from .force_docker_linux import ForceDockerLinux
from .force_docker_mac import ForceDockerMac
from .force_docker_windows import ForceDockerWindows


class ForceDocker:
    """ The class in charge of forcing docker for the system """

    def __init__(self, tty: TTY, success: int = 0, err: int = 84, error: int = 84) -> None:
        self.linux = ForceDockerLinux(tty, success, err, error)
        self.mac = ForceDockerMac(tty, success, err, error)
        self.windows = ForceDockerWindows(tty, success, err, error)
