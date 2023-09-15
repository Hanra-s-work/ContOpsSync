"""
Fle in charge of displaying the "auth" (get the kubectl help)
"""

from tty_ov import TTY


class AuthAppInfoKubernetes:
    """ The class in charge of displaying the "auth" """

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

    def auth(self, args: list) -> int:
        """ Display the kubectl help """
        func_name = "kube_auth"
        if self.tty.help_function_child_name == func_name:
            help_description = f"""
Display the kubectl help
Input:
    {func_name}
Output:
    Display the kubectl help
"""
            self.function_help(func_name, help_description)
            self.tty.current_tty_status = self.tty.success
            return self.success
        self.print_on_tty(
            self.tty.help_title_colour,
            "Displaying kubectl help\n"
        )
        if len(args) > 0:
            self.__no_args(func_name, True)
            return self.err
        return self.run(["kubectl", "auth", "--help"])

    def can_i(self, args: list) -> int:
        """ Check if the user has enough authorisations """
        func_name = "kube_can_i"
        function_prototype = f"{func_name} <verb> <ressource>"
        if self.tty.help_function_child_name == func_name:
            help_description = f"""
Check if the user has enough authorisations
Input:
    {function_prototype}
Output:
    Check if the user has enough authorisations
"""
            self.function_help(func_name, help_description)
            self.tty.current_tty_status = self.tty.success
            return self.success
        self.print_on_tty(
            self.tty.help_title_colour,
            "Checking if the user has enough authorisations\n"
        )
        if len(args) != 2:
            self.__no_args(function_prototype)
            return self.err
        return self.run(["kubectl", "auth", "can-i", args[0], args[1]])

    def reconcile(self, args: list) -> int:
        """ Reconcile the current state of the cluster against the state that the cluster would be in if the manifest was applied """
        func_name = "kube_reconcile"
        function_prototype = f"{func_name} <manifest>"
        if self.tty.help_function_child_name == func_name:
            help_description = f"""
Reconcile the current state of the cluster against the state that the cluster would be in if the manifest was applied
Input:
    {function_prototype}
Output:
    Reconcile the current state of the cluster against the state that the cluster would be in if the manifest was applied
"""
            self.function_help(func_name, help_description)
            self.tty.current_tty_status = self.tty.success
            return self.success
        self.print_on_tty(
            self.tty.help_title_colour,
            "Reconciling the current state of the cluster against the state that the cluster would be in if the manifest was applied\n"
        )
        if len(args) != 1:
            self.__no_args(function_prototype)
            return self.err
        return self.run(["kubectl", "auth", "reconcile", args[0]])

    def whoami(self, args: list) -> int:
        """ Display information about the current user """
        func_name = "kube_whoami"
        if self.tty.help_function_child_name == func_name:
            help_description = f"""
Display information about the current user
Input:
    {func_name}
Output:
    Display information about the current user
"""
            self.function_help(func_name, help_description)
            self.tty.current_tty_status = self.tty.success
            return self.success
        self.print_on_tty(
            self.tty.help_title_colour,
            "Displaying information about the current user\n"
        )
        if len(args) > 0:
            self.__no_args(func_name, True)
            return self.err
        return self.run(["kubectl", "auth", "whoami"])

    def inject_child_functions_into_shell(self, parent_options: list) -> int:
        """ Injects all child functions into the parent function list """
        parent_options.extend(
            [
                {
                    "kube_auth": self.auth,
                    "desc": "Display the auths (not tested !)"
                },
                {
                    "kube_can_i": self.can_i,
                    "desc": "Check if the user has enough authorisations"
                },
                {
                    "kube_whoami": self.whoami,
                    "desc": "Display information about the current user"
                }
            ]
        )
        return self.success
