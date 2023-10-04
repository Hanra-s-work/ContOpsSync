"""
File in charge of displaying the api-ressources of kubectl
"""

from tty_ov import TTY


class ApiRessourcesAppInfoKubernetes:
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

    def __no_args(self, function_prototype: str, to_many: bool = False) -> None:
        """ Display an error message when there is not enough arguments """
        message = f"Not enough arguments\nRequired arguments: {function_prototype}"
        if to_many is True:
            message = f"To many arguments\nRequired arguments: {function_prototype}"
        self.print_on_tty(
            self.tty.error_colour,
            message
        )
        self.tty.current_tty_status = self.tty.error

    def api_ressources(self, args: list) -> int:
        """ Display the api-ressources of kubectl """
        func_name = "kube_api_ressources"
        if self.tty.help_function_child_name == func_name:
            help_description = f"""
Display the api-ressources of kubectl
Input:
    {func_name}
Output:
    Display the api-ressources of kubectl
"""
            self.function_help(func_name, help_description)
            self.tty.current_tty_status = self.tty.success
            return self.success
        return self.run(["kubectl", "api-resources"])

    def inject_child_functions_into_shell(self, parent_options: list) -> int:
        """ Injects all child functions into the parent function list """
        parent_options.extend(
            [
                {
                    "kube_api_ressources": self.api_ressources,
                    "desc": "Display the ressources of the api (not tested !)"
                }
            ]
        )
        return self.success
