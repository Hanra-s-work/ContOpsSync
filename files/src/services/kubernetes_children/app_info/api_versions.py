"""
File in charge of displaying the api-versions of kubectl
"""

from tty_ov import TTY


class ApiVersionsAppInfoKubernetes:
    """ The class in charge of displaying the api-ressources of kubectl """

    def __init__(self, tty: TTY, success: int = 0, err: int = 84, error: int = 84) -> None:
        # ---- System Codes ----
        self.success = success
        self.err = err
        self.error = error
        # ---- Parent classes ----
        self.tty = tty
        # ---- TTY rebinds ----
        self.print_on_tty = self.tty.print_on_tty
        self.run = self.tty.run_command
        self.function_help = self.tty.function_help

    def api_versions(self, args: list) -> int:
        """ Display the api-versions of kubectl """
        func_name = "kube_api_versions"
        if self.tty.help_function_child_name == func_name:
            help_description = f"""
Display the api-versions of kubectl
Input:
    {func_name}
Output:
    Display the api-versions of kubectl
"""
            self.function_help(func_name, help_description)
            self.tty.current_tty_status = self.tty.success
            return self.success
        return self.run(["kubectl", "api-versions"])

    def inject_child_functions_into_shell(self, parent_options: list) -> int:
        """ Injects all child functions into the parent function list """
        parent_options.extend(
            [
                {
                    "api-versions": self.api_versions,
                    "desc": "Display the versions of the api's"
                }
            ]
        )
        return self.success
