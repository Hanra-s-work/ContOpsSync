"""
File in charge of installing kubernetes on all 3 systems
"""

import platform
from tty_ov import TTY
from display_tty import IDISP
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
        self.disp = IDISP
        # ---- TTY rebinds ----
        self.print_on_tty = self.tty.print_on_tty
        # ---- Disp re-configuration ----
        self.disp.toml_content["PRETTIFY_OUTPUT"] = False
        self.disp.toml_content["PRETTY_OUTPUT_IN_BLOCS"] = False
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
            return self.windows.install_kubectl()
        if self.current_system == "Linux":
            return self.linux.install_kubectl()
        if self.current_system == "Darwin" or self.current_system == "Java":
            return self.mac.install_kubectl()
        self.print_on_tty(
            self.tty.error_colour,
            f"System {self.current_system} not supported\n"
        )
        return self.error

    def install_minikube(self, args: list) -> int:
        """ Install kubectl on the host system """
        function_name = "install_minikube"
        if self.tty.help_function_child_name == function_name:
            help_description = f"""
Install minikube on the host system
Usage Example:
Input:
    {function_name}
Output:
    Install process of minikube for the current system
"""
            self.tty.function_help(function_name, help_description)
            self.tty.current_tty_status = self.tty.success
            return self.success
        self.print_on_tty(
            self.tty.info_colour,
            ""
        )
        self.disp.inform_message(
            "Installing kubectl (required for using minikube)"
        )
        status = self.install_kubectl([])
        if status != self.success:
            self.print_on_tty(
                self.tty.error_colour,
                "Error installing kubectl\n"
            )
            return self.tty.error
        if self.current_system == "Windows":
            return self.windows.install_minikube()
        if self.current_system == "Linux":
            return self.linux.install_minikube()
        if self.current_system == "Darwin" or self.current_system == "Java":
            return self.mac.install_minikube()
        self.print_on_tty(
            self.tty.error_colour,
            f"System {self.current_system} not supported\n"
        )
        return self.error

    def install_kind(self, args: list) -> int:
        """ Install kubectl on the host system """
        function_name = "install_kind"
        if self.tty.help_function_child_name == function_name:
            help_description = f"""
Install kind on the host system
Usage Example:
Input:
    {function_name}
Output:
    Install process of kind for the current system
"""
            self.tty.function_help(function_name, help_description)
            self.tty.current_tty_status = self.tty.success
            return self.success
        if self.current_system == "Windows":
            return self.windows.install_kind()
        if self.current_system == "Linux":
            return self.linux.install_kind()
        if self.current_system == "Darwin" or self.current_system == "Java":
            return self.mac.install_kind()
        self.print_on_tty(
            self.tty.error_colour,
            f"System {self.current_system} not supported\n"
        )
        return self.error

    def install_k3s(self, args: list) -> int:
        """ Install kubectl on the host system """
        function_name = "install_k3s"
        if self.tty.help_function_child_name == function_name:
            help_description = f"""
Install k3s on the host system
Usage Example:
Input:
    {function_name}
Output:
    Install process of k3s for the current system
"""
            self.tty.function_help(function_name, help_description)
            self.tty.current_tty_status = self.tty.success
            return self.success
        if self.current_system == "Windows":
            return self.windows.install_k3s()
        if self.current_system == "Linux":
            return self.linux.install_k3s()
        if self.current_system == "Darwin" or self.current_system == "Java":
            return self.mac.install_k3s()
        self.print_on_tty(
            self.tty.error_colour,
            f"System {self.current_system} not supported\n"
        )
        return self.error

    def install_k3d(self, args: list) -> int:
        """ Install kubectl on the host system """
        function_name = "install_k3d"
        if self.tty.help_function_child_name == function_name:
            help_description = f"""
Install k3d on the host system
Usage Example:
Input:
    {function_name}
Output:
    Install process of k3d for the current system
"""
            self.tty.function_help(function_name, help_description)
            self.tty.current_tty_status = self.tty.success
            return self.success
        if self.current_system == "Windows":
            return self.windows.install_k3d()
        if self.current_system == "Linux":
            return self.linux.install_k3d()
        if self.current_system == "Darwin" or self.current_system == "Java":
            return self.mac.install_k3d()
        self.print_on_tty(
            self.tty.error_colour,
            f"System {self.current_system} not supported\n"
        )
        return self.error

    def install_microk8s(self, args: list) -> int:
        """ Install kubectl on the host system """
        function_name = "install_microk8s"
        if self.tty.help_function_child_name == function_name:
            help_description = f"""
Install microk8s on the host system
Usage Example:
Input:
    {function_name}
Output:
    Install process of microk8s for the current system
"""
            self.tty.function_help(function_name, help_description)
            self.tty.current_tty_status = self.tty.success
            return self.success
        if self.current_system == "Windows":
            return self.windows.install_microk8s()
        if self.current_system == "Linux":
            return self.linux.install_microk8s()
        if self.current_system == "Darwin" or self.current_system == "Java":
            return self.mac.install_microk8s()
        self.print_on_tty(
            self.tty.error_colour,
            f"System {self.current_system} not supported\n"
        )
        return self.error

    def install_k8s(self, args: list) -> int:
        """ Install kubectl on the host system """
        function_name = "install_k8s"
        if self.tty.help_function_child_name == function_name:
            help_description = f"""
Install k8s on the host system
Usage Example:
Input:
    {function_name}
Output:
    Install process of k8s for the current system
"""
            self.tty.function_help(function_name, help_description)
            self.tty.current_tty_status = self.tty.success
            return self.success
        if self.current_system == "Windows":
            return self.windows.install_k8s()
        if self.current_system == "Linux":
            return self.linux.install_k8s()
        if self.current_system == "Darwin" or self.current_system == "Java":
            return self.mac.install_k8s()
        self.print_on_tty(
            self.tty.error_colour,
            f"System {self.current_system} not supported\n"
        )
        return self.error

    def install_kubernetes(self, args: list) -> int:
        """ Install k8s because this is the other name of kubernetes """
        self.print_on_tty(self.tty.info_colour, "")
        info_message = "Info: Kubernetes is also known as k8s, thus, this function will run the k8s installation."
        self.disp.inform_message(info_message)
        return self.install_k8s(args)

    def install_kubeadm(self, args: list) -> int:
        """ Install kubectl on the host system """
        function_name = "install_kubeadm"
        if self.tty.help_function_child_name == function_name:
            help_description = f"""
Install kubeadm on the host system
Usage Example:
Input:
    {function_name}
Output:
    Install process of kubeadm for the current system
"""
            self.tty.function_help(function_name, help_description)
            self.tty.current_tty_status = self.tty.success
            return self.success
        if self.current_system == "Windows":
            return self.windows.install_kubeadm()
        if self.current_system == "Linux":
            return self.linux.install_kubeadm()
        if self.current_system == "Darwin" or self.current_system == "Java":
            return self.mac.install_kubeadm()
        self.print_on_tty(
            self.tty.error_colour,
            f"System {self.current_system} not supported\n"
        )
        return self.error

    def _install_options_windows(self) -> int:
        """ Install kubectl on the host system """

    def _install_options_linux(self) -> int:
        """ Install kubectl on the host system """

    def _install_options_mac(self) -> int:
        """ Install kubectl on the host system """

    def install_options(self, args: list) -> int:
        """ Install kubectl on the host system """
        function_name = "install_options"
        if self.tty.help_function_child_name == function_name:
            help_description = f"""
View the installation options for the host system
Usage Example:
Input:
    {function_name}
Output:
    A list of program options that can be installed
"""
            self.tty.function_help(function_name, help_description)
            self.tty.current_tty_status = self.tty.success
            return self.success
        if self.current_system == "Windows":
            return self._install_options_windows()
        if self.current_system == "Linux":
            return self._install_options_linux()
        if self.current_system == "Darwin" or self.current_system == "Java":
            return self._install_options_mac()
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
                "install_kubernetes": self.install_kubernetes,
                "desc": "Install Kubernetes (k8s) on the host system"
            },
            {
                "install_kubectl":  self.install_kubectl,
                "desc": "Install kubectl on the host system"
            },
            {
                "install_minikube": self.install_minikube,
                "desc": "Install minikube on the host system"
            },
            {
                "install_kind": self.install_kind,
                "desc": "Install kind on the host system"
            },
            {
                "install_k3s": self.install_k3s,
                "desc": "Install k3s on the host system"
            },
            {
                "install_k3d": self.install_k3d,
                "desc": "Install k3d on the host system"
            },
            {
                "install_microk8s": self.install_microk8s,
                "desc": "Install microk8s on the host system"
            },
            {
                "install_k8s": self.install_k8s,
                "desc": "Install k8s on the host system"
            },
            # {
            #     "install_kubeadm": self.install_kubeadm,
            #     "desc": "Install kubeadm on the host system"
            # },
            {
                "install_options": self.install_options,
                "desc": "View the installation options for the host system"
            },
            {
                "test_install_kubernetes": self.test_install_kubernetes,
                "desc": "Test the kubernetes installation classes"
            }
        ]
        return self.options
