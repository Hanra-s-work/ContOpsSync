"""
File in charge of uninstalling kubernetes on all 3 systems
"""

import platform
from tty_ov import TTY
from display_tty import IDISP
from .uninstall import Uninstall


class UninstallKubernetes():
    """ Uninstall the kubernetes library on the host system """

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
        self.uninstall = Uninstall()
        # ---- System uninstall ----
        self.windows = self.uninstall.uninstall_kubernetes_windows(
            self.tty,
            self.success,
            self.err,
            self.error
        )
        self.linux = self.uninstall.uninstall_kubernetes_linux(
            self.tty,
            self.success,
            self.err,
            self.error
        )
        self.mac = self.uninstall.uninstall_kubernetes_mac(
            self.tty,
            self.success,
            self.err,
            self.error
        )
        # ---- command management ----
        self.options = []

    def uninstall_kubectl(self, args: list) -> int:
        """ Uninstall kubectl on the host system """
        function_name = "uninstall_kubectl"
        if self.tty.help_function_child_name == function_name:
            help_description = f"""
Uninstall kubectl on the host system
Usage Example:
Input:
    {function_name}
Output:
    Uninstall process of kubectl for the current system
"""
            self.tty.function_help(function_name, help_description)
            self.tty.current_tty_status = self.tty.success
            return self.success
        if self.current_system == "Windows":
            return self.windows.uninstall_kubectl()
        if self.current_system == "Linux":
            return self.linux.uninstall_kubectl()
        if self.current_system == "Darwin" or self.current_system == "Java":
            return self.mac.uninstall_kubectl()
        self.print_on_tty(
            self.tty.error_colour,
            f"System {self.current_system} not supported\n"
        )
        return self.error

    def uninstall_minikube(self, args: list) -> int:
        """ Uninstall kubectl on the host system """
        function_name = "uninstall_minikube"
        if self.tty.help_function_child_name == function_name:
            help_description = f"""
Install minikube on the host system
Usage Example:
Input:
    {function_name}
Output:
    Uninstall process of minikube for the current system
"""
            self.tty.function_help(function_name, help_description)
            self.tty.current_tty_status = self.tty.success
            return self.success
        self.print_on_tty(
            self.tty.info_colour,
            ""
        )
        self.disp.inform_message(
            "Uninstalling kubectl (required for using minikube)"
        )
        status = self.uninstall_kubectl([])
        if status != self.success:
            self.print_on_tty(
                self.tty.error_colour,
                "Error uninstalling kubectl\n"
            )
            return self.tty.error
        if self.current_system == "Windows":
            return self.windows.uninstall_minikube()
        if self.current_system == "Linux":
            return self.linux.uninstall_minikube()
        if self.current_system == "Darwin" or self.current_system == "Java":
            return self.mac.uninstall_minikube()
        self.print_on_tty(
            self.tty.error_colour,
            f"System {self.current_system} not supported\n"
        )
        return self.error

    def uninstall_kind(self, args: list) -> int:
        """ Uninstall kubectl on the host system """
        function_name = "uninstall_kind"
        if self.tty.help_function_child_name == function_name:
            help_description = f"""
Uninstall kind on the host system
Usage Example:
Input:
    {function_name}
Output:
    Uninstall process of kind for the current system
"""
            self.tty.function_help(function_name, help_description)
            self.tty.current_tty_status = self.tty.success
            return self.success
        if self.current_system == "Windows":
            return self.windows.uninstall_kind()
        if self.current_system == "Linux":
            return self.linux.uninstall_kind()
        if self.current_system == "Darwin" or self.current_system == "Java":
            return self.mac.uninstall_kind()
        self.print_on_tty(
            self.tty.error_colour,
            f"System {self.current_system} not supported\n"
        )
        return self.error

    def uninstall_k3s(self, args: list) -> int:
        """ Uninstall kubectl on the host system """
        function_name = "uninstall_k3s"
        if self.tty.help_function_child_name == function_name:
            help_description = f"""
Uninstall k3s on the host system (kubernetes combined with containerd [or docker if specified])
Usage Example:
Input:
    {function_name}
Output:
    Uninstallation process of k3s for the current system
"""
            self.tty.function_help(function_name, help_description)
            self.tty.current_tty_status = self.tty.success
            return self.success
        if self.current_system == "Windows":
            return self.windows.uninstall_k3s()
        if self.current_system == "Linux":
            return self.linux.uninstall_k3s()
        if self.current_system == "Darwin" or self.current_system == "Java":
            return self.mac.uninstall_k3s()
        self.print_on_tty(
            self.tty.error_colour,
            f"System {self.current_system} not supported\n"
        )
        return self.error

    def uninstall_k3d(self, args: list) -> int:
        """ Uninstall kubectl on the host system """
        function_name = "uninstall_k3d"
        if self.tty.help_function_child_name == function_name:
            help_description = f"""
Uninstall k3d on the host system (kubernetes combined with docker)
Usage Example:
Input:
    {function_name}
Output:
    Uninstallation process of k3d for the current system
"""
            self.tty.function_help(function_name, help_description)
            self.tty.current_tty_status = self.tty.success
            return self.success
        if self.current_system == "Windows":
            return self.windows.uninstall_k3d()
        if self.current_system == "Linux":
            return self.linux.uninstall_k3d()
        if self.current_system == "Darwin" or self.current_system == "Java":
            return self.mac.uninstall_k3d()
        self.print_on_tty(
            self.tty.error_colour,
            f"System {self.current_system} not supported\n"
        )
        return self.error

    def uninstall_microk8s(self, args: list) -> int:
        """ Uninstall kubectl on the host system """
        function_name = "uninstall_microk8s"
        if self.tty.help_function_child_name == function_name:
            help_description = f"""
Uninstall microk8s on the host system
Usage Example:
Input:
    {function_name}
Output:
    Uninstall process of microk8s for the current system
"""
            self.tty.function_help(function_name, help_description)
            self.tty.current_tty_status = self.tty.success
            return self.success
        if self.current_system == "Windows":
            return self.windows.uninstall_microk8s()
        if self.current_system == "Linux":
            return self.linux.uninstall_microk8s()
        if self.current_system == "Darwin" or self.current_system == "Java":
            return self.mac.uninstall_microk8s()
        self.print_on_tty(
            self.tty.error_colour,
            f"System {self.current_system} not supported\n"
        )
        return self.error

    def uninstall_k8s(self, args: list) -> int:
        """ Uninstall kubectl on the host system """
        function_name = "uninstall_k8s"
        if self.tty.help_function_child_name == function_name:
            help_description = f"""
Uninstall k8s on the host system
Usage Example:
Input:
    {function_name}
Output:
    Uninstall process of k8s for the current system
"""
            self.tty.function_help(function_name, help_description)
            self.tty.current_tty_status = self.tty.success
            return self.success
        if self.current_system == "Windows":
            return self.windows.uninstall_k8s()
        if self.current_system == "Linux":
            return self.linux.uninstall_k8s()
        if self.current_system == "Darwin" or self.current_system == "Java":
            return self.mac.uninstall_k8s()
        self.print_on_tty(
            self.tty.error_colour,
            f"System {self.current_system} not supported\n"
        )
        return self.error

    def uninstall_kubernetes(self, args: list) -> int:
        """ Uninstall k8s because this is the other name of kubernetes """
        self.print_on_tty(self.tty.info_colour, "")
        info_message = "Info: Kubernetes is also known as k8s, thus, this function will run the k8s uninstallation."
        self.disp.inform_message(info_message)
        return self.uninstall_k8s(args)

    def uninstall_kubeadm(self, args: list) -> int:
        """ Uninstall kubectl on the host system """
        function_name = "uninstall_kubeadm"
        if self.tty.help_function_child_name == function_name:
            help_description = f"""
Uninstall kubeadm on the host system
Usage Example:
Input:
    {function_name}
Output:
    Uninstall process of kubeadm for the current system
"""
            self.tty.function_help(function_name, help_description)
            self.tty.current_tty_status = self.tty.success
            return self.success
        if self.current_system == "Windows":
            return self.windows.uninstall_kubeadm()
        if self.current_system == "Linux":
            return self.linux.uninstall_kubeadm()
        if self.current_system == "Darwin" or self.current_system == "Java":
            return self.mac.uninstall_kubeadm()
        self.print_on_tty(
            self.tty.error_colour,
            f"System {self.current_system} not supported\n"
        )
        return self.error

    def _uninstall_options_windows(self) -> int:
        """ Uninstall kubectl on the host system """

    def _uninstall_options_linux(self) -> int:
        """ Uninstall kubectl on the host system """

    def _uninstall_options_mac(self) -> int:
        """ Uninstall kubectl on the host system """

    def uninstall_options(self, args: list) -> int:
        """ Uninstall kubectl on the host system """
        function_name = "uninstall_options"
        if self.tty.help_function_child_name == function_name:
            help_description = f"""
View the uninstallation options for the host system
Usage Example:
Input:
    {function_name}
Output:
    A list of program options that can be uninstalled
"""
            self.tty.function_help(function_name, help_description)
            self.tty.current_tty_status = self.tty.success
            return self.success
        if self.current_system == "Windows":
            return self._uninstall_options_windows()
        if self.current_system == "Linux":
            return self._uninstall_options_linux()
        if self.current_system == "Darwin" or self.current_system == "Java":
            return self._uninstall_options_mac()
        self.print_on_tty(
            self.tty.error_colour,
            f"System {self.current_system} not supported\n"
        )
        return self.error

    def test_uninstall_kubernetes(self, args: list) -> int:
        """ Test the kubernetes installation """
        function_name = "test_uninstall_kubernetes"
        if self.tty.help_function_child_name == function_name:
            help_description = f"""
Make sure the uninstall kubernetes classes are initialised
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
            "This message prooves that the uninstall kubernetes has loaded correctly.\n"
        )
        self.windows.test_class_uninstall_kubernetes_windows()
        self.linux.test_class_uninstall_kubernetes_linux()
        self.mac.test_class_uninstall_kubernetes_mac()
        return self.success

    def save_commands(self) -> list:
        """ The function in charge of saving the commands to the options list """
        self.options = [
            {
                "uninstall_kubernetes": self.uninstall_kubernetes,
                "desc": "Install Kubernetes (k8s) on the host system"
            },
            {
                "uninstall_kubectl":  self.uninstall_kubectl,
                "desc": "Install kubectl on the host system"
            },
            {
                "uninstall_minikube": self.uninstall_minikube,
                "desc": "Install minikube on the host system"
            },
            {
                "uninstall_kind": self.uninstall_kind,
                "desc": "Install kind on the host system"
            },
            {
                "uninstall_k3s": self.uninstall_k3s,
                "desc": "Install k3s on the host system"
            },
            {
                "uninstall_k3d": self.uninstall_k3d,
                "desc": "Install k3d on the host system"
            },
            {
                "uninstall_microk8s": self.uninstall_microk8s,
                "desc": "Install microk8s on the host system"
            },
            {
                "uninstall_k8s": self.uninstall_k8s,
                "desc": "Install k8s on the host system"
            },
            {
                "uninstall_options": self.uninstall_options,
                "desc": "View the installation options for the host system"
            },
            {
                "test_uninstall_kubernetes": self.test_uninstall_kubernetes,
                "desc": "Test the kubernetes installation classes"
            }
        ]
        return self.options
