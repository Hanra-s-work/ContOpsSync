"""
File in charge of installing kubernetes on all 3 systems
"""

import platform
from tty_ov import TTY
from .install import Install


class InstallKubernetes():
    """ Install the kubernetes library on the host system """

    def __init__(self, tty: TTY, success: int = 0, err: int = 84, error: int = 84) -> None:
        # ---- System Codes ----
        self.success = success
        self.err = err
        self.error = error
        # ---- System info ----
        self.current_system = platform.system()
        # ---- Parent classes ----
        self.tty = tty
        # ---- TTY rebinds ----
        self.print_on_tty = self.tty.print_on_tty
        # ---- Child classes ----
        self.install = Install()
        # ---- System install ----
        self.windows = self.install.install_kubernetes_windows(
            self.tty,
            self.success,
            self.err,
            self.error
        )
        self.linux = self.install.install_kubernetes_linux(
            self.tty,
            self.success,
            self.err,
            self.error
        )
        self.mac = self.install.install_kubernetes_mac(
            self.tty,
            self.success,
            self.err,
            self.error
        )
        # ---- command management ----
        self.options = []

    def install_kubectl(self, args: list) -> int:
        """ Install kubectl on the host system """
        function_name = "install_kubectl"
        if self.tty.help_function_child_name == function_name:
            help_description = f"""
Install kubectl on the host system
Usage Example:
Input:
    {function_name}
Output:
    Install process of kubectl for the current system
"""
            self.tty.function_help(function_name, help_description)
            self.tty.current_tty_status = self.tty.success
            return self.success
        if self.current_system == "Windows":
            return self.windows.main()
        if self.current_system == "Linux":
            return self.linux.main()
        if self.current_system == "Darwin" or self.current_system == "Java":
            return self.mac.main()
        self.print_on_tty(
            self.tty.error_colour,
            f"System {self.current_system} not supported\n"
        )
        return self.error

    def test_install_kubernetes(self, args: list) -> int:
        """ Test the kubernetes installation """
        function_name = "test_install_kubernetes"
        if self.tty.help_function_child_name == function_name:
            help_description = f"""
Make sure the install kubernetes classes are installed
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
            "This message prooves that the install kubernetes has loaded correctly.\n"
        )
        self.windows.test_class_install_kubernetes_windows()
        self.linux.test_class_install_kubernetes_linux()
        self.mac.test_class_install_kubernetes_mac()
        return self.success

    def save_commands(self) -> list:
        """ The function in charge of saving the commands to the options list """
        self.options = [
            {
                "install_kubectl":  self.install_kubectl,
                "desc": "Install kubectl on the host system"
            },
            {
                "test_install_kubernetes": self.test_install_kubernetes,
                "desc": "Test the kubernetes installation classes"
            }
        ]
        return self.options
