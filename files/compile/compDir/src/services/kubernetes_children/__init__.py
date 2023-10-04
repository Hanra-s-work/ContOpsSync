"""
File containing the Kubernetes class in charge of managin kubenetes service
"""

import os
from tty_ov import TTY
from .install import Install
from .install_kubernetes import InstallKubernetes
from .app_info import AppInfoKubernetes


class KubeChildren:
    """ The dependencies used by the kubernetes class """

    def __init__(self, tty: TTY, success: int, err: int, error: int) -> None:
        # ---- Status codes ----
        self.success = success
        self.err = err
        self.error = error
        # ---- Inherited classes ----
        self.tty = tty
        # ---- Child classes ----
        self.install_kubernetes = InstallKubernetes(tty, success, err, error)
        self.app_info = AppInfoKubernetes(tty, success, err, error)
        self.install = Install()

    def test_children(self) -> int:
        """ The function in charge of testing the children """
        self.tty.print_on_tty(
            self.tty.info_colour,
            "This is a test message from the KubChildren class\n"
        )
        self.install.test_class_install()
        self.install_kubernetes.test_install_kubernetes([])
        return self.success

    def inject_child_ressources(self, parent_options: list[dict]) -> int:
        """ Injects all child ressources into the parent ressource list """
        content = self.install_kubernetes.save_commands()
        parent_options.extend(content)
        self.app_info.inject_child_functions_into_shell(parent_options)
