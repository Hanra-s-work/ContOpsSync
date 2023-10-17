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
Install k3s on the host system (kubernetes combined with containerd  [or docker if specified])
Usage Example:
Input:
    {function_name} as_slave:boolean force_docker:boolean<default: False> master_token:string master_ip:string
Output:
    Installation process of k3s for the current system
Example 1 (Installing as master node):
    {function_name} true
Example 2 (Installing as slave node):
    {function_name} false <your_master_token> <your_master_ip>
Example 3 (Installing as master node with docker set as default):
    {function_name} true true
Example 2 (Installing as slave node with docker set as default):
    {function_name} false true <your_master_token> <your_master_ip>
"""
            self.tty.function_help(function_name, help_description)
            self.tty.current_tty_status = self.tty.success
            return self.success
        arg_length = len(args)
        as_slave = False
        force_docker = False
        master_token = ""
        master_ip = ""
        if arg_length >= 1:
            if args[0].lower() == "true":
                as_slave = False
            else:
                as_slave = True
        if arg_length >= 2:
            if args[1].lower() == "true":
                force_docker = True
            else:
                force_docker = False
        if arg_length >= 3:
            master_token = args[2]
        if arg_length >= 4:
            master_ip = args[3]
        if self.current_system == "Windows":
            return self.windows.install_k3s()
        if self.current_system == "Linux":
            return self.linux.install_k3s(as_slave, force_docker, master_token, master_ip)
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
Install k3d on the host system (kubernetes combined with docker)
Usage Example:
Input:
    {function_name} as_slave:boolean master_token:string master_ip:string
Output:
    Installation process of k3d for the current system
Example 1 (Installing as master node):
    {function_name} true
Example 2 (Installing as slave node):
    {function_name} false <your_master_token> <your_master_ip>
"""
            self.tty.function_help(function_name, help_description)
            self.tty.current_tty_status = self.tty.success
            return self.success
        arg_length = len(args)
        as_master = True
        master_token = ""
        master_ip = ""
        if arg_length >= 1:
            if args[0].lower() == "true":
                as_master = False
            else:
                as_master = True
        if arg_length >= 2:
            master_token = args[1]
        if arg_length >= 3:
            master_ip = args[2]
        if self.current_system == "Windows":
            return self.windows.install_k3d()
        if self.current_system == "Linux":
            return self.linux.install_k3d(as_master, master_token, master_ip)
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

    def is_k3s_installed(self, args: list) -> int:
        """ Returns true if k3s is installed """
        function_name = "is_k3s_installed"
        if self.tty.help_function_child_name == function_name:
            help_description = f"""
Returns true if k3s is installed
Usage Example:
Input:
    {function_name}
Output:
    [OK] if k3s is installed
"""
            self.tty.function_help(function_name, help_description)
            self.tty.current_tty_status = self.tty.success
            return self.tty.success
        if self.current_system == "Windows":
            status = self.windows.is_k3s_installed()
        if self.current_system == "Linux":
            status = self.linux.is_k3s_installed()
        if self.current_system == "Darwin" or self.current_system == "Java":
            status = self.mac.is_k3s_installed()
        if status is False:
            self.tty.current_tty_status = self.tty.error
            return self.tty.error
        self.tty.current_tty_status = self.tty.success
        return self.tty.success

    def is_k3d_installed(self, args: list) -> int:
        """ Returns true if k3d is installed """
        function_name = "is_k3d_installed"
        if self.tty.help_function_child_name == function_name:
            help_description = f"""
Returns true if k3d is installed
Usage Example:
Input:
    {function_name}
Output:
    [OK] if k3d is installed
"""
            self.tty.function_help(function_name, help_description)
            self.tty.current_tty_status = self.tty.success
            return self.tty.success
        if self.current_system == "Windows":
            status = self.windows.is_k3d_installed()
        if self.current_system == "Linux":
            status = self.linux.is_k3d_installed()
        if self.current_system == "Darwin" or self.current_system == "Java":
            status = self.mac.is_k3d_installed()
        if status is False:
            self.tty.current_tty_status = self.tty.error
            return self.tty.error
        self.tty.current_tty_status = self.tty.success
        return self.tty.success

    def get_master_token(self, args: list) -> int:
        """ Get the token of the master node """
        function_name = "get_master_token"
        if self.tty.help_function_child_name == function_name:
            help_description = f"""
Get the token of the master node
Usage Example:
Input:
    {function_name}
Output:
    The token of the master node
"""
            self.tty.function_help(function_name, help_description)
            self.tty.current_tty_status = self.tty.success
            return self.tty.success
        if self.current_system == "Windows":
            return self.windows.get_master_token()
        if self.current_system == "Linux":
            return self.linux.get_master_token()
        if self.current_system == "Darwin" or self.current_system == "Java":
            return self.mac.get_master_token()
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
Make sure the install kubernetes classes are initialised
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
            {
                "install_options": self.install_options,
                "desc": "View the installation options for the host system"
            },
            {
                "is_k3s_installed": self.is_k3s_installed,
                "desc": "Check if k3s is installed on your system"
            },
            {
                "is_k3d_installed": self.is_k3d_installed,
                "desc": "Check if k3d is installed on your system"
            },
            {
                "get_master_token": self.get_master_token,
                "desc": "Get the token of the master node"
            },
            {
                "test_install_kubernetes": self.test_install_kubernetes,
                "desc": "Test the kubernetes installation classes"
            }
        ]
        return self.options
