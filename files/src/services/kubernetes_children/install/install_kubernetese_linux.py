"""
File in charge of containing the class that will install kubernetes for linux distributions.
"""

from tty_ov import TTY
import disp


class InstallKubernetesLinux:
    """ The class in charge of installing kubernetes for linux """

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
            "winget": False  # ,
            # "manual":False
        }
        # ---- The Disp option ----
        self.disp = disp.IDISP
        self.disp.toml_content["PRETTIFY_OUTPUT"] = False
        self.disp.toml_content["PRETTY_OUTPUT_IN_BLOCS"] = False
        # ---- links for manual installation ----
        self.release_file = "https://cdn.dl.k8s.io/release/stable.txt"
        self.install_file_link_chunk1 = "https://dl.k8s.io/release/"
        self.install_file_link_chunk2 = "/bin/windows/amd64/kubectl.exe"
        self.installer_name = "kubectl.exe"
        self.installer_folder = ".kubectl"
        self.home = ""
        self.full_path = ""
        # ---- Testing installation ----
        self.kube_folder = ".kube"
        self.config_file = "config"

    def main(self) -> None:
        """ Install kubernetes for linux """
        print("Install kubernetes for linux - Not created yet")

    def test_class_install_kubernetes_linux(self) -> int:
        """ Test the class install kubernetes linux """
        print("This is a test message from the install kubernetes linux class")
        return 0
