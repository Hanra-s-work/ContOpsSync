"""
File containing the Kubernetes class in charge of managin kubenetes service
"""

import os
from tty_ov import TTY
from .kubernetes_children import KubeChildren


class Kubernetes:
    """ The class in charge of managing Kubernetes """

    def __init__(self, success, err, error, tty: TTY) -> None:
        self.success = success
        self.err = err
        self.error = error
        self.tty = tty
        # ---- TTY Kubernetes options ----
        self.options = []
        # ---- Child classes ----
        self.kube_children = KubeChildren(
            self.tty,
            self.success,
            self.err,
            self.error
        )

    def kubernetes_class_test(self, args: list) -> int:
        """ This is a test to check that the classe's function has correctly imported """
        self.tty.print_on_tty(
            self.tty.success_colour,
            "This is a test message.\n"
        )
        self.tty.print_on_tty(
            self.tty.success_colour,
            "If you see this message:\n"
        )
        self.tty.print_on_tty(
            self.tty.success_colour,
            "\tThis means that the Kubernetes class has correctly been imported\n"
        )
        self.kube_children.test_children()
        self.tty.current_tty_status = self.success
        return self.tty.current_tty_status

    def save_commands(self) -> None:
        """ The function in charge of saving the commands to the options list """
        self.options.append(
            {
                "kubernetes_class_test":  self.kubernetes_class_test,
                "desc": "A test function for the Kubernetes class"
            }
        )
        self.kube_children.inject_child_ressources(self.options)

    def injector(self) -> int:
        """ The function in charge of injecting the kubernetes class into the main class """
        self.save_commands()
        return self.tty.import_functions_into_shell(self.options)
