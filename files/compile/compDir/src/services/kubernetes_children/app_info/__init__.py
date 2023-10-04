"""
File in charge of gathering the different info that the user can choose to display about kubernetes
"""

from tty_ov import TTY
from .describe import DescribeAppInfoKubernetes
from .version import VersionAppInfoKubernetes
from .logs import LogsAppInfoKubernetes
from .auth import AuthAppInfoKubernetes
from .api_ressources import ApiRessourcesAppInfoKubernetes
from .api_versions import ApiVersionsAppInfoKubernetes


class AppInfoKubernetes:
    """ The class in charge of grouping the different description class instances """

    def __init__(self, tty: TTY, success: int = 0, err: int = 84, error: int = 84) -> None:
        # ---- System Codes ----
        self.success = success
        self.err = err
        self.error = error
        # ---- Parent classes ----
        self.tty = tty
        # ---- TTY rebinds ----
        self.print_on_tty = self.tty.print_on_tty
        # ---- Child classes ----
        self.describe = DescribeAppInfoKubernetes(
            self.tty,
            self.success,
            self.err,
            self.error
        )
        self.version = VersionAppInfoKubernetes(
            self.tty,
            self.success,
            self.err,
            self.error
        )
        self.logs_app_info_kubernetes = LogsAppInfoKubernetes(
            self.tty,
            self.success,
            self.err,
            self.error
        )
        self.auth_app_info_kubernetes = AuthAppInfoKubernetes(
            self.tty,
            self.success,
            self.err,
            self.error
        )
        self.api_ressources_app_info_kubernetes = ApiRessourcesAppInfoKubernetes(
            self.tty,
            self.success,
            self.err,
            self.error
        )
        self.api_versions_app_info_kubernetes = ApiVersionsAppInfoKubernetes(
            self.tty,
            self.success,
            self.err,
            self.error
        )
        # ---- command management ----
        self.options = []

    def inject_child_functions_into_shell(self, parent_options: list) -> int:
        """ Injects all child functions into the parent function list """
        status = self.describe.inject_child_functions_into_shell(
            parent_options
        )
        if status != self.success:
            self.print_on_tty(
                self.tty.error_colour,
                "Failed to inject kubernetes describe functions into the shell.\n"
            )
            return status
        status = self.version.inject_child_functions_into_shell(parent_options)
        if status != self.success:
            self.print_on_tty(
                self.tty.error_colour,
                "Failed to inject kubernetes version functions into the shell.\n"
            )
            return status
        status = self.logs_app_info_kubernetes.inject_child_functions_into_shell(
            parent_options
        )
        if status != self.success:
            self.print_on_tty(
                self.tty.error_colour,
                "Failed to inject kubernetes version functions into the shell.\n"
            )
            return status
        status = self.auth_app_info_kubernetes.inject_child_functions_into_shell(
            parent_options
        )
        if status != self.success:
            self.print_on_tty(
                self.tty.error_colour,
                "Failed to inject kubernetes version functions into the shell.\n"
            )
            return status
        status = self.api_ressources_app_info_kubernetes.inject_child_functions_into_shell(
            parent_options
        )
        if status != self.success:
            self.print_on_tty(
                self.tty.error_colour,
                "Failed to inject kubernetes version functions into the shell.\n"
            )
            return status
        status = self.api_versions_app_info_kubernetes.inject_child_functions_into_shell(
            parent_options)
        if status != self.success:
            self.print_on_tty(
                self.tty.error_colour,
                "Failed to inject kubernetes version functions into the shell.\n"
            )
            return status
        return self.success
