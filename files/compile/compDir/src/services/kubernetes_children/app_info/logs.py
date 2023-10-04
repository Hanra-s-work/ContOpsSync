"""
File in containing the class in charge of displaying the logs of kubernetes
"""

from tty_ov import TTY


class LogsAppInfoKubernetes:
    """ The class in charge of displaying the logs of kubernetes """

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

    def __no_args(self, function_prototype: str) -> None:
        """ Display an error message when there is not enough arguments """
        self.print_on_tty(
            self.tty.error_colour,
            f"Not enough arguments\nRequired arguments: {function_prototype}"
        )
        self.tty.current_tty_status = self.tty.error

    def logs(self, args: list) -> int:
        """ Display the logs of a specific pod """
        func_name = "kube_logs"
        function_prototype = f"{func_name} <pod>"
        if self.tty.help_function_child_name == func_name:
            help_description = f"""
Display logs from pod <nginx> with only one container
Input:
    {function_prototype}
Output:
    Display the logs of the pod
"""
            self.function_help(func_name, help_description)
            self.tty.current_tty_status = self.tty.success
            return self.success
        if len(args) == 0:
            self.__no_args(function_prototype)
            self.tty.current_tty_status = self.tty.err
            return self.err
        usr_input = " ".join(args)
        return self.run(["kubectl", "logs", usr_input])

    def display_all_logs_from_pod(self, args: list) -> int:
        """ Display the logs of a specific pod """
        func_name = "kube_log_all"
        function_prototype = f"{func_name} <pod>"
        if self.tty.help_function_child_name == func_name:
            help_description = f"""
Display all the logs of a specific pod
Input:
    {function_prototype}
Output:
    Display the logs of the pod
"""
            self.function_help(func_name, help_description)
            self.tty.current_tty_status = self.tty.success
            return self.success
        if len(args) == 0:
            self.__no_args(function_prototype)
            self.tty.current_tty_status = self.tty.err
            return self.err
        usr_input = " ".join(args)
        return self.run(["kubectl", "logs", usr_input, "--all-containers=true"])

    def log_all_containers_by_name(self, args: list) -> int:
        """ Display the logs of a specific pod """
        func_name = "kube_log_all_by_name"
        function_prototype = f"{func_name} <label>"
        if self.tty.help_function_child_name == func_name:
            help_description = f"""
Display all the logs of a specific label
Input:
    {function_prototype}
Output:
    Display the logs of the label
"""
            self.function_help(func_name, help_description)
            self.tty.current_tty_status = self.tty.success
            return self.success
        if len(args) == 0:
            self.__no_args(function_prototype)
            self.tty.current_tty_status = self.tty.err
            return self.err
        usr_input = " ".join(args)
        return self.run(["kubectl", "logs", "-l", usr_input, "--all-containers=true"])

    def log_all_containers_by_name_and_since(self, args: list) -> int:
        """ Display the logs of a specific pod """
        func_name = "kube_log_all_by_name_and_since"
        function_prototype = f"{func_name} <label> <time>"
        if self.tty.help_function_child_name == func_name:
            help_description = f"""
Display all the logs of a specific label since a specific time
Input:
    {function_prototype}
Output:
    Display the logs of the label since a specific time
"""
            self.function_help(func_name, help_description)
            self.tty.current_tty_status = self.tty.success
            return self.success
        if len(args) < 2:
            self.__no_args(function_prototype)
            self.tty.current_tty_status = self.tty.err
            return self.err
        return self.run(["kubectl", "logs", "-l", args[0], "--all-containers=true", f"--since={args[1]}"])

    def logs_dead_container_from_pod(self, args: list) -> int:
        """ Display the logs of a specific pod """
        func_name = "kube_log_dead_container"
        function_prototype = f"{func_name} <pod> <container>"
        if self.tty.help_function_child_name == func_name:
            help_description = f"""
Display the logs of a dead container from a specific pod
Input:
    {function_prototype}
Output:
    Display the logs of the dead container from the pod
"""
            self.function_help(func_name, help_description)
            self.tty.current_tty_status = self.tty.success
            return self.success
        if len(args) < 2:
            self.__no_args(function_prototype)
            self.tty.current_tty_status = self.tty.err
            return self.err
        return self.run(["kubectl", "logs", "-p", "-c", args[1], args[0]])

    def live_logs_from_container(self, args: list) -> int:
        """ Display the logs of a specific pod """
        func_name = "kube_log_live_container"
        function_prototype = f"{func_name} <pod> <container>"
        if self.tty.help_function_child_name == func_name:
            help_description = f"""
Display the logs of a live container from a specific pod
Input:
    {function_prototype}
Output:
    Display the logs of the live container from the pod
"""
            self.function_help(func_name, help_description)
            self.tty.current_tty_status = self.tty.success
            return self.success
        if len(args) < 2:
            self.__no_args(function_prototype)
            self.tty.current_tty_status = self.tty.err
            return self.err
        return self.run(["kubectl", "logs", "-f", "-c", args[1], args[0]])

    def live_logs_from_label(self, args: list) -> int:
        """ Display the logs of a specific pod """
        func_name = "kube_log_live_label"
        function_prototype = f"{func_name} <label>"
        if self.tty.help_function_child_name == func_name:
            help_description = f"""
Display the logs of a live container from a specific label
Input:
    {function_prototype}
Output:
    Display the live logs of the container from the label
"""
            self.function_help(func_name, help_description)
            self.tty.current_tty_status = self.tty.success
            return self.success
        if len(args) == 0:
            self.__no_args(function_prototype)
            self.tty.current_tty_status = self.tty.err
            return self.err
        usr_input = " ".join(args)
        return self.run(["kubectl", "logs", "-f", "-l", usr_input, "--all-containers=true"])

    def short_log(self, args: list) -> int:
        """ Display the logs of a specific pod """
        func_name = "kube_log_short"
        function_prototype = f"{func_name} <pod> <lines>"
        if self.tty.help_function_child_name == func_name:
            help_description = f"""
Display no more than <n> lines of the pod log
Input:
    {function_prototype}
Output:
    Display the last <n> lines of the logs from the pod
"""
            self.function_help(func_name, help_description)
            self.tty.current_tty_status = self.tty.success
            return self.success
        if len(args) < 2:
            self.__no_args(function_prototype)
            self.tty.current_tty_status = self.tty.err
            return self.err
        return self.run(["kubectl", "logs", args[0], f"--tail={args[1]}"])

    def logs_since(self, args: list) -> int:
        """ Display the logs of a specific pod """
        func_name = "kube_log_since"
        function_prototype = f"{func_name} <pod> <time>"
        if self.tty.help_function_child_name == func_name:
            help_description = f"""
Display the logs of a specific pod that has been active for the last <n> amount of time
Input:
    {function_prototype}
Output:
    Display the logs from the pod since a specific time
"""
            self.function_help(func_name, help_description)
            self.tty.current_tty_status = self.tty.success
            return self.success
        if len(args) < 2:
            self.__no_args(function_prototype)
            self.tty.current_tty_status = self.tty.err
            return self.err
        return self.run(["kubectl", "logs", args[0], f"--since={args[1]}"])

    def log_expired_certificate_pod(self, args: list) -> int:
        """ Display the logs of a specific pod """
        func_name = "kube_log_expired_certificate"
        function_prototype = f"{func_name} <pod>"
        if self.tty.help_function_child_name == func_name:
            help_description = f"""
Display the logs of a specific pod whom's certificate is expired
Input:
    {function_prototype}
Output:
    Display the logs from the pod with an expired certificate
"""
            self.function_help(func_name, help_description)
            self.tty.current_tty_status = self.tty.success
            return self.success
        if len(args) == 0:
            self.__no_args(function_prototype)
            self.tty.current_tty_status = self.tty.err
            return self.err
        usr_input = " ".join(args)
        return self.run(["kubectl", "logs", "--insecure-skip-tls-verify-backend", usr_input])

    def log_job(self, args: list) -> int:
        """ Display the logs of a specific pod """
        func_name = "kube_log_job"
        function_prototype = f"{func_name} <job>"
        if self.tty.help_function_child_name == func_name:
            help_description = f"""
Display the logs for the first job matching the provided name
Input:
    {function_prototype}
Output:
    Display the logs from the job
"""
            self.function_help(func_name, help_description)
            self.tty.current_tty_status = self.tty.success
            return self.success
        if len(args) > 1:
            self.__no_args(function_prototype)
            self.tty.current_tty_status = self.tty.err
            return self.err
        return self.run(["kubectl", "logs", f"job/{args[0]}"])

    def log_pod_job(self, args: list) -> int:
        """ Display the logs of a specific pod """
        func_name = "kube_log_pod_job"
        function_prototype = f"{func_name} <pod> <job>"
        if self.tty.help_function_child_name == func_name:
            help_description = f"""
Display the logs of a specific job fro a specified container
Input:
    {function_prototype}
Output:
    Display the logs from the job
"""
            self.function_help(func_name, help_description)
            self.tty.current_tty_status = self.tty.success
            return self.success
        if len(args) == 0:
            self.__no_args(function_prototype)
            self.tty.current_tty_status = self.tty.err
            return self.err
        usr_input = " ".join(args)
        return self.run(["kubectl", "logs", "-f", "-c", usr_input[0], f"job/{usr_input[1]}"])

    def log_deployment(self, args: list) -> int:
        """ Display the logs of a specific pod """
        func_name = "kube_log_deployment"
        function_prototype = f"{func_name} <deployment>"
        if self.tty.help_function_child_name == func_name:
            help_description = f"""
Display the logs of a specific deployment from a specified container
Input:
    {function_prototype}
Output:
    Display the logs from the deployment
"""
            self.function_help(func_name, help_description)
            self.tty.current_tty_status = self.tty.success
            return self.success
        if len(args) > 1:
            self.__no_args(function_prototype)
            self.tty.current_tty_status = self.tty.err
            return self.err
        return self.run(["kubectl", "logs", f"deployment/{args[0]}"])

    def inject_child_functions_into_shell(self, parent_options: list) -> int:
        """ Injects all child functions into the parent function list """
        parent_options.extend(
            [
                {
                    "kube_logs": self.logs,
                    "desc": "Display the logs (not tested !)"
                },
                {
                    "kube_log_all": self.display_all_logs_from_pod,
                    "desc": "Display the logs of a specific pod"
                },
                {
                    "kube_log_all_by_name": self.log_all_containers_by_name,
                    "desc": "Display the logs of a specific label"
                },
                {
                    "kube_log_all_by_name_and_since": self.log_all_containers_by_name_and_since,
                    "desc": "Display the logs of a specific label since a specific time"
                },
                {
                    "kube_log_dead_container": self.logs_dead_container_from_pod,
                    "desc": "Display the logs of a dead container from a specific pod"
                },
                {
                    "kube_log_live_container": self.live_logs_from_container,
                    "desc": "Display the logs of a live container from a specific pod"
                },
                {
                    "kube_log_live_label": self.live_logs_from_label,
                    "desc": "Display the logs of a live container from a specific label"
                },
                {
                    "kube_log_short": self.short_log,
                    "desc": "Display no more than <n> lines of the pod log"
                },
                {
                    "kube_log_since": self.logs_since,
                    "desc": "Display the logs of a specific pod that has been active for the last <n> amount of time"
                },
                {
                    "kube_log_expired_certificate": self.log_expired_certificate_pod,
                    "desc": "Display the logs of a specific pod whom's certificate is expired"
                },
                {
                    "kube_log_job": self.log_job,
                    "desc": "Display the logs for the first job matching the provided name"
                },
                {
                    "kube_log_pod_job": self.log_pod_job,
                    "desc": "Display the logs of a specific job fro a specified container"
                },
                {
                    "kube_log_deployment": self.log_deployment,
                    "desc": "Display the logs of a specific deployment from a specified container"
                }
            ]
        )
        return self.success
