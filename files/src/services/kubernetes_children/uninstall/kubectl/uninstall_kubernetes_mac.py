"""
File in charge of containing the code that will uninstall kubernetes on a mac.
"""

from tty_ov import TTY
import display_tty


class UninstallKubectlMac:
    """ Install the kubernetes on Mac """

    def __init__(self, tty: TTY, success: int = 0, err: int = 84, error: int = 84) -> None:
        # ---- System Codes ----
        self.success = success
        self.err = err
        self.error = error
        # ---- Parent classes ----
        self.tty = tty
        # ---- TTY rebinds ----
        self.print_on_tty = self.tty.print_on_tty
        # ---- Download options ----
        self.download_options = {
            "choco": False,
            "scoop": False,
            "winget": False
        }
        # ---- The Disp option ----
        self.disp = display_tty.IDISP
        self.disp.toml_content["PRETTIFY_OUTPUT"] = False
        self.disp.toml_content["PRETTY_OUTPUT_IN_BLOCS"] = False
        # ---- links for manual uninstallation ----
        self.release_file = "https://cdn.dl.k8s.io/release/stable.txt"
        self.uninstall_file_link_chunk1 = "https://dl.k8s.io/release/"
        self.uninstall_file_link_chunk2 = "/bin/windows/amd64/kubectl.exe"
        self.uninstaller_name = "kubectl.exe"
        self.uninstaller_folder = ".kubectl"
        self.home = ""
        self.full_path = ""
        # ---- Testing uninstallation ----
        self.kube_folder = ".kube"
        self.config_file = "config"

    def uninstall_kubectl(self) -> int:
        """ uninstall the kubectl software """
        print("Install kubernetes on Mac - Not created yet")
        return self.success

    def main(self) -> int:
        """ Install kubernetes on Mac """
        return self.uninstall_kubectl()

    def test_class_uninstall_kubectl_mac(self) -> int:
        """ Test the class uninstall kubectl mac """
        self.print_on_tty(
            self.tty.info_colour,
            "This is a test message from the uninstall kubectl mac class\n"
        )
        return self.success
