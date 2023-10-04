"""
File in charge of describing information about a specific ressources or group of ressources
"""

from tty_ov import TTY


class DescribeAppInfoKubernetes:
    """ The class in charge of displaying information about a specific ressources or group of ressources  """

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

    def describe(self, args: list) -> int:
        """ Display information about a service """
        func_name = "kube_describe"
        if self.tty.help_function_child_name == func_name:
            help_description = f"""
Display information about a service
Input:
    {func_name} <service>
Output:
    Display information about the service
Kubernetes description (adapted to this command program):
    Show details of a specific resource or group of resources.

    Print a detailed description of the selected resources, including related resources such as events or controllers. You may select a single object by name, all objects of that type, provide a name prefix, or label selector. For example:

    run kubectl describe TYPE NAME_PREFIX
    
    will first check for an exact match on TYPE and NAME_PREFIX. If no such resource exists, it will output details for every resource that has a name prefixed with NAME_PREFIX.

    Use "k_api-resources" for a complete list of supported resources.

    Examples:
    # Describe a node
    run kubectl describe nodes kubernetes-node-emt8.c.myproject.internal
    
    # Describe a pod
    run kubectl describe pods/nginx
    
    # Describe a pod identified by type and name in "pod.json"
    run kubectl describe -f pod.json
    
    # Describe all pods
    run kubectl describe pods
    
    # Describe pods by label name=myLabel
    run kubectl describe po -l name=myLabel
    
    # Describe all pods managed by the 'frontend' replication controller
    # (rc-created pods get the name of the rc as a prefix in the pod name)
    run kubectl describe pods frontend
"""
            self.function_help(func_name, help_description)
            self.tty.current_tty_status = self.tty.success
            return self.success

        self.print_on_tty(
            self.tty.help_title_colour,
            "Displaying information about the requested service\n"
        )
        usr_input = " ".join(args)
        status = self.run(["kubectl", "describe", usr_input])
        self.tty.current_tty_status = status
        return status

    def describe_a_node(self, args: list) -> int:
        """ Display information about a node """
        func_name = "kube_describe_node"
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
        usr_input = " ".join(args)
        return self.describe(["node", usr_input])

    def describe_a_pod(self, args: list) -> int:
        """ Display information about a pod """
        func_name = "kube_describe_pod"
        if self.tty.help_function_child_name == func_name:
            help_description = f"""
Display information about a pod
Input:
    {func_name} <pod>
Output:
    Display information about the pod
"""
            self.function_help(func_name, help_description)
            self.tty.current_tty_status = self.tty.success
            return self.success
        usr_input = " ".join(args)
        return self.describe([f"pods/{usr_input}"])

    def describe_pod_identified_by_type_and_name(self, args: list) -> int:
        """ Display information about a pod identified by type and name """
        func_name = "kube_describe_pod_identified_by_type_and_name"
        if self.tty.help_function_child_name == func_name:
            help_description = f"""
Display information about a pod identified by type and name
Input:
    {func_name} <pod>
Output:
    Display information about the pod identified by type and name
"""
            self.function_help(func_name, help_description)
            self.tty.current_tty_status = self.tty.success
            return self.success
        usr_input = " ".join(args)
        return self.describe(["-f", usr_input])

    def describe_all_pods(self, args: list) -> int:
        """ Display information about all pods """
        func_name = "kube_describe_all_pods"
        if self.tty.help_function_child_name == func_name:
            help_description = f"""
Display information about all pods
Input:
    {func_name}
Output:
    Display information about all pods
"""
            self.function_help(func_name, help_description)
            self.tty.current_tty_status = self.tty.success
            return self.success
        return self.describe(["pods"])

    def describe_pods_by_label(self, args: list) -> int:
        """ Display information about pods by label """
        func_name = "kube_describe_pods_by_label"
        if self.tty.help_function_child_name == func_name:
            help_description = f"""
Display information about pods by label
Input:
    {func_name} name=<label>
Output:
    Display information about pods by label
"""
            self.function_help(func_name, help_description)
            self.tty.current_tty_status = self.tty.success
            return self.success
        usr_input = " ".join(args)
        return self.describe(["po", "-l", usr_input])

    def describe_all_pods_managed_by_frontend(self, args: list) -> int:
        """ Display information about all pods managed by the 'frontend' replication controller """
        func_name = "kube_describe_all_pods_managed_by_frontend"
        if self.tty.help_function_child_name == func_name:
            help_description = f"""
Display information about all pods managed by the 'frontend' replication controller
Input:
    {func_name}
Output:
    Display information about all pods managed by the 'frontend' replication controller
"""
            self.function_help(func_name, help_description)
            self.tty.current_tty_status = self.tty.success
            return self.success
        return self.describe(["pods", "frontend"])

    def inject_child_functions_into_shell(self, parent_options: list) -> int:
        """ Injects all child functions into the parent function list """
        parent_options.extend(
            [
                {
                    "kube_describe": self.describe,
                    "desc": "Display information about a service"
                },
                {
                    "kube_describe_node": self.describe_a_node,
                    "desc": "Display information about a node"
                },
                {
                    "kube_describe_pod": self.describe_a_pod,
                    "desc": "Display information about a pod"
                },
                {
                    "kube_describe_pod_identified_by_type_and_name": self.describe_pod_identified_by_type_and_name,
                    "desc": "Display information about a pod identified by type and name"
                },
                {
                    "kube_describe_all_pods": self.describe_all_pods,
                    "desc": "Display information about all pods"
                },
                {
                    "kube_describe_pods_by_label": self.describe_pods_by_label,
                    "desc": "Display information about pods by label"
                },
                {
                    "kube_describe_all_pods_managed_by_frontend": self.describe_all_pods_managed_by_frontend,
                    "desc": "Display information about all pods managed by the 'frontend' replication controller"
                }
            ]
        )
        return self.success
