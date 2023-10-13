"""
File in charge of installing Docker on all 3 systems
"""

import platform
from tty_ov import TTY
from display_tty import IDISP
from .install import InstallDockerInit


class InstallDocker():
    """ Install the Docker library on the host system """

    def __init__(self, tty: TTY, success: int = 0, err: int = 84, error: int = 84) -> None:
        # ---- System Codes ----
        self.success = success
        self.err = err
        self.error = error
        # ---- System info ----
        self.current_system = platform.system()
        # ---- Parent classes ----
        self.tty = tty
        self.disp = IDISP
        # ---- TTY rebinds ----
        self.print_on_tty = self.tty.print_on_tty
        # ---- Disp re-configuration ----
        self.disp.toml_content["PRETTIFY_OUTPUT"] = False
        self.disp.toml_content["PRETTY_OUTPUT_IN_BLOCS"] = False
        # ---- Child classes ----
        self.install = InstallDockerInit(tty, success, err, error)
        # ---- System install ----
        self.windows = self.install.install_docker_windows
        self.linux = self.install.install_docker_linux
        self.raspberrypi = self.install.install_docker_raspberrypi
        self.mac = self.install.install_docker_mac
        # ---- command management ----
        self.options = []

    def install_docker(self, args: list) -> int:
        """ Install docker on the host system """
        function_name = "install_docker"
        if self.tty.help_function_child_name == function_name:
            help_description = f"""
Install docker on the host system
Usage Example:
Input:
    {function_name}
Output:
    Install process of docker for the current system
"""
            self.tty.function_help(function_name, help_description)
            self.tty.current_tty_status = self.tty.success
            return self.success
        if self.current_system == "Windows":
            return self.windows.main()
        if self.current_system == "Linux":
            if self.raspberrypi.is_raspberrypi() is True:
                return self.raspberrypi.main()
            return self.linux.main()
        if self.current_system == "Darwin" or self.current_system == "Java":
            return self.mac.main()
        self.print_on_tty(
            self.tty.error_colour,
            f"System {self.current_system} not supported\n"
        )
        return self.error

    def is_docker_installed(self, args: list) -> int:
        """ Returns true if Docker is installed """
        function_name = "is_docker_installed"
        if self.tty.help_function_child_name == function_name:
            help_description = f"""
Returns true if Docker is installed
Usage Example:
Input:
    {function_name}
Output:
    [OK] if Docker is installed
"""
            self.tty.function_help(function_name, help_description)
            self.tty.current_tty_status = self.tty.success
            return self.tty.success
        if self.current_system == "Windows":
            status = self.windows.is_docker_installed()
        if self.current_system == "Linux":
            if self.raspberrypi.is_raspberrypi() is True:
                status = self.raspberrypi.is_docker_installed()
            else:
                status = self.linux.is_docker_installed()
        if self.current_system == "Darwin" or self.current_system == "Java":
            status = self.mac.is_docker_installed()
        if status is False:
            self.tty.current_tty_status = self.tty.error
            return self.tty.error
        self.tty.current_tty_status = self.tty.success
        return self.tty.success

    def test_install_docker(self, args: list) -> int:
        """ Test the Docker installation """
        function_name = "test_install_docker"
        if self.tty.help_function_child_name == function_name:
            help_description = f"""
Make sure the install Docker classes are loaded
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
            "This message prooves that the install Docker has loaded correctly.\n"
        )
        self.windows.test_class_install_docker_windows()
        self.linux.test_class_install_docker_linux()
        self.mac.test_class_install_docker_mac()
        return self.success

    def save_commands(self) -> list:
        """ The function in charge of saving the commands to the options list """
        self.options = [
            {
                "install_docker": self.install_docker,
                "desc": "Install Docker on the host system"
            },
            {
                "is_docker_installed": self.is_docker_installed,
                "desc": "Returns true if Docker is installed"
            },
            {
                "test_install_Docker": self.test_install_docker,
                "desc": "Test the Docker installation classes"
            }
        ]
        return self.options
