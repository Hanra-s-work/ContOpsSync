"""
File in charge of rebinding kubectl as kube
"""

import os
import platform
from tty_ov import TTY
from display_tty import IDISP


class Kubectl():
    """ Install the kubernetes library on the host system """

    def __init__(self, tty: TTY, success: int = 0, err: int = 84, error: int = 84) -> None:
        # ---- System Codes ----
        self.success = success
        self.err = err
        self.error = error
        # ---- Parent classes ----
        self.tty = tty
        self.disp = IDISP
        # ---- TTY rebinds ----
        self.print_on_tty = self.tty.print_on_tty
        # ---- Disp re-configuration ----
        self.disp.toml_content["PRETTIFY_OUTPUT"] = False
        self.disp.toml_content["PRETTY_OUTPUT_IN_BLOCS"] = False

    def kubectl(self, args: list) -> int:
        """ Run commands using the official kubectl instance """
        function_name = "kubectl"
        if self.tty.help_function_child_name == function_name:
            help_description = f"""
Run the kubectl commands using kubectl
Usage Example:
Input:
    {function_name} get pods
Output:
    A list of the available pods
"""
            self.tty.function_help(function_name, help_description)
            self.tty.current_tty_status = self.tty.success
            return self.success
        if platform.system() != "Windows":
            args.insert(0, "sudo kubectl")
        else:
            args.insert(0, "kubectl")
        return self.tty.run_command(args)

    def kube(self, args: list) -> int:
        """ Rebind kubectl as kube and run commands via the rebind """
        function_name = "kubectl"
        if self.tty.help_function_child_name == function_name:
            help_description = f"""
Run the kubectl commands using kube
Usage Example:
Input:
    {function_name} get pods
Output:
    A list of the available pods
"""
            self.tty.function_help(function_name, help_description)
            self.tty.current_tty_status = self.tty.success
            return self.success
        if 'kube' not in os.environ:
            if platform.system() != "Windows":
                os.environ["kube"] = "sudo kubectl"
            else:
                os.environ["kube"] = "kubectl"
        args.insert(0, "kube")
        return self.tty.run_command(args)

    def rebind_kubectl_as_kube(self, args: list) -> int:
        """ Rebind kubectl as kube """
        function_name = "rebind_kubectl_as_kube"
        if self.tty.help_function_child_name == function_name:
            help_description = f"""
Rebind kubectl as kube
Usage Example:
Input:
    {function_name}
Output:
    kubectl rebound as kube (the kubectl will still remain available)
"""
            self.tty.function_help(function_name, help_description)
            self.tty.current_tty_status = self.tty.success
            return self.success
        if 'kube' not in os.environ:
            if platform.system() != "Windows":
                os.environ["kube"] = "sudo kubectl"
            else:
                os.environ["kube"] = "kubectl"
            self.print_on_tty(
                self.tty.success_colour,
                "kubectl rebound as kube (the kubectl will still remain available)\n"
            )
        return self.success

    def _create_rebind_command(self, command: dict[str], rebind_item: str, new_name: str) -> dict:
        """ Create the rebind command """
        data = dict()
        for i in command:
            if rebind_item in i:
                tmp = i.replace(f"{rebind_item}", f"{new_name}")
                data[f"{tmp}"] = command[i]
                data["desc"] = command["desc"]
                break
        return data

    def rebind_kube_commands_as_kubectl(self, args: list) -> int:
        """ Rebind kube commands as kubectl """
        function_name = "rebind_kube_commands_as_kubectl"
        if self.tty.help_function_child_name == function_name:
            help_description = f"""
Rebind kube commands as kubectl
Usage Example:
Input:
    {function_name}
Output:
    kube commands rebound as kubectl (the kube commands will still remain available)
"""
            self.tty.function_help(function_name, help_description)
            self.tty.current_tty_status = self.tty.success
            return self.success
        if 'kubectl' not in os.environ:
            if platform.system() != "Windows":
                os.environ["kubectl"] = "sudo kubectl"
            else:
                os.environ["kubectl"] = "kubectl"
            self.print_on_tty(
                self.tty.success_colour,
                "kube commands rebound as kubectl (the kube commands will still remain available)\n"
            )
        option_length = len(self.tty.options)
        option_tracker = 0
        for i in self.tty.options:
            for b in i:
                if b in "desc":
                    continue
                if "kube" in b:
                    self.tty.options.append(
                        self._create_rebind_command(i, b, "kubectl")
                    )
                    self.print_on_tty(
                        self.tty.success_colour,
                        f"Command '{b}' rebound to {b.replace('kube', 'kubectl')}, the originale command is still available.\n"
                    )
                break
            option_tracker += 1
            if option_tracker >= option_length:
                break
        print(self.tty.options)
        return self.success

    def test_class_kubectl(self, args: list) -> int:
        """ Test kubectl """
        function_name = "test_class_kubectl"
        if self.tty.help_function_child_name == function_name:
            help_description = f"""
Make sure the install kubectl class is initialised
Usage Example:
Input:
    {function_name}
Output:
    A message from the class informing that it has been loaded
"""
            self.tty.function_help(function_name, help_description)
            self.tty.current_tty_status = self.tty.success
            return self.success
        self.print_on_tty(
            self.tty.info_colour,
            "This message prooves that the install kubectl class has loaded correctly.\n"
        )
        return self.success

    def save_commands(self) -> list:
        """ The function in charge of saving commands to the options list """
        options = [
            {
                "kubectl": self.kubectl,
                "desc": "Call the kubectl binary (if installed) that is located on your system."
            },
            {
                "kube": self.kube,
                "desc": "Call the kubectl binary (if installed) that is located on your system."
            },
            {
                "rebind_kubectl_as_kube": self.rebind_kubectl_as_kube,
                "desc": "Rebind kubectl as kube."
            },
            {
                "rebind_kube_commands_as_kubectl": self.rebind_kube_commands_as_kubectl,
                "desc": "Rebind kube commands to contain the kubectl keyword."
            },
            {
                "test_class_kubectl": self.test_class_kubectl,
                "desc": "Test the kubectl class."
            }
        ]
        return options
