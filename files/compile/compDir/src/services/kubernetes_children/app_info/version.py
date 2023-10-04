"""
File in charge of displaying the versions of the server and the client
"""

from tty_ov import TTY


class VersionAppInfoKubernetes:
    """ The class in charge of displaying the versions of the server and the client """

    def __init__(self, tty: TTY, success: int = 0, err: int = 84, error: int = 84) -> None:
        # ---- System Codes ----
        self.success = success
        self.err = err
        self.error = error
        # ---- Parent classes ----
        self.tty = tty
        # ---- TTY rebinds ----
        self.print_on_tty = self.tty.print_on_tty
        self.function_help = self.tty.function_help
        self.run = self.tty.run_command

    def version(self, args: list) -> int:
        """ Display the versions of the server and the client """
        func_name = "kube_version"
        if self.tty.help_function_child_name == func_name:
            help_description = f"""
Display information about a node
Input:
    {func_name} <node>
Output:
    Display information about the node
"""
            self.function_help(func_name, help_description)
            self.tty.current_tty_status = self.tty.success
            return self.success
        self.print_on_tty(
            self.tty.help_title_colour,
            "Displaying overall version view\n"
        )
        return self.run(["kubectl", "version", "--output=yaml"])

    def client_version(self, args: list) -> int:
        """ Display the version of the client """
        func_name = "kube_client_version"
        if self.tty.help_function_child_name == func_name:
            help_description = f"""
Display information about a node
Input:
    {func_name} <node>
Output:
    Display information about the node
"""
            self.function_help(func_name, help_description)
            self.tty.current_tty_status = self.tty.success
            return self.success
        self.print_on_tty(
            self.tty.help_title_colour,
            "Displaying information about the client\n"
        )
        return self.run(["kubectl", "version"])

    def server_version(self, args: list) -> int:
        """ Display the version of the server """
        func_name = "kube_server_version"
        if self.tty.help_function_child_name == func_name:
            help_description = f"""
Display information about a node
Input:
    {func_name} <node>
Output:
    Display information about the node
"""
            self.function_help(func_name, help_description)
            self.tty.current_tty_status = self.tty.success
            return self.success
        self.print_on_tty(
            self.tty.help_title_colour,
            "Displaying information about the server\n"
        )
        return self.run(["kubectl", "version", "--short"])

    def inject_child_functions_into_shell(self, parent_options: list) -> int:
        """ Injects all child functions into the parent function list """
        parent_options.extend(
            [
                {
                    "kube_version": self.version,
                    "desc": "Display the versions of the server and the client"
                },
                {
                    "kube_client_version": self.client_version,
                    "desc": "Display the version of the client"
                },
                {
                    "kube_server_version": self.server_version,
                    "desc": "Display the version of the server"
                }
            ]
        )
        return self.success
