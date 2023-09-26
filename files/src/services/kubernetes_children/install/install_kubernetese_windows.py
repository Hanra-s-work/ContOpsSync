"""
File in charge of downloading kubernetes for windows
"""

import os
import requests
import display_tty
from tqdm import tqdm
from tty_ov import TTY


class InstallKubernetesWindows:
    """ The script in charge of installing the kubernetes interpreter for windows """

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
        self.disp = display_tty.IDISP
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

    def download_file(self, url: str, filepath: str) -> int:
        """ Download a file from a url """
        self.print_on_tty(
            self.tty.info_colour,
            f"Downloading file from url: {url}\n"
        )
        try:
            request = requests.get(
                url,
                allow_redirects=True,
                timeout=10,
                stream=True
            )
            with open(filepath, "wb") as file:
                total_length = int(request.headers.get('content-length'))
                chunk_size = 1024
                for chunk in tqdm(
                    request.iter_content(chunk_size=chunk_size),
                    total=(total_length // chunk_size)+1,
                    unit='KB'
                ):
                    if chunk:
                        file.write(chunk)
                        file.flush()
            self.print_on_tty(
                self.tty.success_colour,
                f"File downloaded to: {filepath}\n"
            )
            self.tty.current_tty_status = self.tty.success
            return self.tty.current_tty_status
        except requests.RequestException as err:
            self.print_on_tty(
                self.tty.error_colour,
                f"Error downloading file: {err}\n"
            )
            self.tty.current_tty_status = self.tty.error
            return self.tty.current_tty_status

    def save_environement_variable(self, variable_name: str, variable_value: str) -> int:
        """ Permanently add or update an environment variable """
        try:
            with os.popen(f'setx {variable_name} "{variable_value}"') as pointer:
                result = pointer.close()
                if result is not None:
                    self.print_on_tty(
                        self.tty.error_colour,
                        f"Failed to set environment variable '{variable_name}'\n"
                    )
                    return self.tty.error
                else:
                    self.print_on_tty(
                        self.tty.success_colour,
                        f"Successfully set environment variable '{variable_name}'\n"
                    )
                    return self.tty.success
        except OSError as err:
            self.print_on_tty(
                self.tty.error_colour,
                f"Error: {str(err)}\n"
            )
            return self.tty.error

    def save_permanently_to_path(self, path: str) -> int:
        """ Permanently add a variable to the path of the user """
        variable_name = "PATH"
        if variable_name not in os.environ:
            self.print_on_tty(
                self.tty.error_colour,
                "Error saving path: PATH not found in environment variables\n"
            )
            self.tty.current_tty_status = self.tty.error
            return self.tty.current_tty_status
        old_path = os.environ[variable_name]
        if "/" in path:
            path = path.replace("/", "\\")
        if path in old_path:
            self.print_on_tty(
                self.tty.success_colour,
                f"'{path}' is already present in the 'PATH' environement."
            )
            return self.tty.success
        if path[-1] != ";":
            path += ";"
        if old_path[-1] != ";":
            old_path += ";"
        new_path = f"{path};{old_path}"
        status = self.save_environement_variable(variable_name, new_path)
        if status != self.tty.success:
            self.print_on_tty(
                self.tty.error_colour,
                "Error saving path: PATH not found in environment variables\n"
            )
            self.tty.current_tty_status = self.tty.error
            return self.tty.error
        status = self.tty.setenv([variable_name, new_path])
        os.environ[variable_name] = new_path
        if status != self.tty.success:
            self.print_on_tty(
                self.tty.error_colour,
                "Error saving path: PATH not found in environment variables\n"
            )
            self.tty.current_tty_status = self.tty.error
            return self.tty.error
        return self.tty.success

    def compile_new_path(self) -> int:
        """ Create the new path in which the kubectl.exe will be found """
        self.full_path = ""
        if "HOMEDRIVE" in os.environ:
            self.full_path += os.environ['HOMEDRIVE']
        if "HOMEPATH" in os.environ:
            self.full_path += os.environ['HOMEPATH']
            self.home = f"{self.full_path}"
        if self.installer_folder != "":
            self.full_path += f"\\{self.installer_folder}"
            self.tty.create_directories(self.full_path, False)
        if self.full_path == "":
            self.full_path = os.getcwd()
        return self.save_permanently_to_path(self.full_path)

    def get_file_content(self, file_path: str) -> str or int:
        """ Get the content of a file """
        if os.path.isfile(file_path) is False:
            self.print_on_tty(
                self.tty.error_colour,
                f"Error getting file content: {file_path} is not a file\n"
            )
            self.tty.current_tty_status = self.tty.error
            return self.tty.current_tty_status
        try:
            with open(file_path, "r", encoding="utf-8", newline="\n") as file:
                content = file.read()
            self.tty.current_tty_status = self.tty.success
            return content
        except OSError as err:
            self.print_on_tty(
                self.tty.error_colour,
                f"Error getting file content: {err}\n"
            )
            self.tty.current_tty_status = self.tty.error
            return self.tty.current_tty_status

    def run_command(self, command: str) -> int:
        """ Run a command on the host system """
        self.tty.current_tty_status = self.tty.run_external_command(
            command
        )
        if self.tty.current_tty_status != self.tty.success:
            self.print_on_tty(
                self.tty.error_colour,
                f"Error running command: {command}\n"
            )
        return self.tty.current_tty_status

    def update_extension_availability(self) -> None:
        """ Check if the file has an extension """
        for i in self.download_options:
            self.print_on_tty(self.tty.info_colour, f"{i}: ")
            if self.run_command(f"{i} --version  >nul 2>nul") == self.success:
                self.download_options[i] = True
                self.print_on_tty(self.tty.success_colour, "[OK]\n")
            else:
                self.download_options[i] = False
                self.print_on_tty(self.tty.error_colour, "[KO]\n")

    def install_via_chocolatey(self) -> int:
        """ Install Kubectl using the chocolatey package manager """
        self.print_on_tty(
            self.tty.info_colour,
            "Installing Kubernetes for Windows via Chocolatey\n"
        )
        self.tty.current_tty_status = self.run_command(
            "choco install kubernetes-cli"
        )
        if self.tty.current_tty_status != self.tty.success:
            self.print_on_tty(
                self.tty.error_colour,
                "Error installing Kubernetes for Windows via Chocolatey\n"
            )
            return self.tty.current_tty_status
        self.tty.current_tty_status = self.tty.success
        return self.tty.current_tty_status

    def install_via_scoop(self) -> int:
        """ Install Kubectl using the scoop package manager """
        self.print_on_tty(
            self.tty.info_colour,
            "Installing Kubernetes for Windows via Scoop\n"
        )
        self.tty.current_tty_status = self.run_command(
            "scoop install kubernetes"
        )
        if self.tty.current_tty_status != self.tty.success:
            self.print_on_tty(
                self.tty.error_colour,
                "Error installing Kubernetes for Windows via Scoop\n"
            )
            return self.tty.current_tty_status
        self.tty.current_tty_status = self.tty.success
        return self.tty.current_tty_status

    def temporary_path(self) -> int:
        """ Update the path of the loaded path """
        error_message = """
Failed to update the path.\n
Please make sure the package was correctly installed:
- please close the window in which this program was launched (this might involve exiting your ssh session)
- please open a new window and try again
"""
        path_updater = ""
        if "LOCALAPPDATA" in os.environ:
            path_updater = os.environ['LOCALAPPDATA']
        else:
            if "HOMEDRIVE" in os.environ:
                path_updater += os.environ['HOMEDRIVE']
            if "HOMEPATH" in os.environ:
                path_updater += os.environ['HOMEPATH']
                self.home = f"{path_updater}"
            if os.path.isdir(f"{path_updater}\\AppData\\Local") is True:
                path_updater += "\\AppData\\Local"
            else:
                self.print_on_tty(
                    self.tty.error_colour,
                    error_message
                )
                return self.tty.err
        if os.path.isdir(f"{path_updater}\\Microsoft\\WinGet\\Packages") is False:
            self.print_on_tty(
                self.tty.error_colour,
                error_message
            )
            return self.tty.err
        path_updater = f"{path_updater}\\Microsoft\\WinGet\\Packages"
        dir_content = os.listdir(path_updater)
        for i in dir_content:
            if "kubectl" in i:
                path_updater += f"\\{i}"
                break
        path_updater += ";"
        self.save_permanently_to_path(path_updater)
        return self.success

    def install_via_winget(self) -> int:
        """ Install Kubectl using the winget package manager """
        self.print_on_tty(
            self.tty.info_colour,
            "Installing Kubernetes for Windows via winget\n"
        )
        self.tty.current_tty_status = self.run_command(
            "winget install -e --id Kubernetes.kubectl"
        )
        if self.tty.current_tty_status != self.tty.success:
            self.print_on_tty(
                self.tty.error_colour,
                "Error installing Kubernetes for Windows via winget\n"
            )
            return self.tty.current_tty_status
        self.temporary_path()
        self.tty.current_tty_status = self.tty.success
        return self.tty.current_tty_status

    def get_latest_version(self) -> int:
        """ Get the latest version of the program """
        self.tty.current_tty_status = self.tty.success
        self.print_on_tty(
            self.tty.info_colour,
            "Getting the latest version of Kubernetes for Windows\n"
        )
        version_name = "version.useless"
        status = self.download_file(
            self.release_file,
            version_name
        )
        if status != self.tty.success:
            self.print_on_tty(
                self.tty.error_colour,
                "Error getting the latest release of Kubernetes for Windows\n"
            )
            self.tty.current_tty_status = status
            return self.tty.current_tty_status
        file_content = self.get_file_content(version_name)
        if file_content == self.tty.error:
            self.print_on_tty(
                self.tty.error_colour,
                "Error getting the latest release of Kubernetes for Windows\n"
            )
            self.tty.current_tty_status = self.tty.error
            return self.tty.current_tty_status
        download_link = f"{self.install_file_link_chunk1}{file_content}{self.install_file_link_chunk2}"
        status = self.download_file(
            download_link,
            f"{self.full_path}\\{self.installer_name}"
        )
        if self.tty.current_tty_status != self.tty.success:
            self.print_on_tty(
                self.tty.error_colour,
                "Error downloading the latest release of Kubernetes for Windows\n"
            )
            return self.tty.current_tty_status
        self.print_on_tty(
            self.tty.success_colour,
            "Downloaded Kubernetes for Windows\n"
        )
        self.tty.current_tty_status = self.tty.success
        return self.tty.current_tty_status

    def install_manually(self) -> int:
        """ Install kubernetes manually """
        self.print_on_tty(
            self.tty.info_colour,
            ""
        )
        self.disp.sub_sub_title("Installing Kubernetes for Windows manually\n")
        self.compile_new_path()
        self.tty.current_tty_status = self.get_latest_version()
        if self.tty.current_tty_status != self.tty.success:
            self.print_on_tty(
                self.tty.error_colour,
                "Error installing Kubernetes for Windows manually\n"
            )
            return self.tty.current_tty_status

        self.tty.current_tty_status = self.tty.success
        return self.tty.current_tty_status

    def use_available_method(self) -> int:
        """ Check which extension is installed """
        if self.download_options["winget"] is True:
            self.print_on_tty(
                self.tty.info_colour,
                "Using Winget to install Kubernetes for Windows\n"
            )
            return self.install_via_winget()
        if self.download_options["choco"] is True:
            self.print_on_tty(
                self.tty.info_colour,
                "Using Chocolatey to install Kubernetes for Windows\n"
            )
            return self.install_via_chocolatey()
        if self.download_options["scoop"] is True:
            self.print_on_tty(
                self.tty.info_colour,
                "Using Scoop to install Kubernetes for Windows\n"
            )
            return self.install_via_scoop()
        self.print_on_tty(
            self.tty.error_colour,
            "No package manager found to install Kubernetes for Windows\n"
        )
        self.print_on_tty(
            self.tty.info_colour,
            "Reverting to manual installation ..."
        )
        return self.install_manually()

    def create_kube_folder(self) -> int:
        """ create the required .kube folder """
        self.print_on_tty(
            self.tty.info_colour,
            f"Creating required {self.kube_folder} in {self.home}"
        )
        status = self.tty.change_directory([self.home])
        if status != self.tty.success:
            self.print_on_tty(
                self.tty.error_colour,
                f"Error accessing {self.home}"
            )
            return self.tty.error
        status = self.tty.create_directories(self.kube_folder, True)
        if status != self.tty.success:
            self.print_on_tty(
                self.tty.error_colour,
                f"Error creating {self.kube_folder} in {self.home}"
            )
            return self.tty.error
        self.tty.current_tty_status = self.tty.success
        return self.tty.current_tty_status

    def set_kube_folder_up(self) -> int:
        """ Do the required steps to set the .kube folder up """
        status = self.create_kube_folder()
        if status != self.tty.success:
            self.print_on_tty(
                self.tty.error_colour,
                "Error creating the .kube folder\n"
            )
            return self.tty.error
        status = self.tty.change_directory([self.kube_folder])
        if status != self.tty.success:
            self.print_on_tty(
                self.tty.error_colour,
                "Error accessing the .kube folder\n"
            )
            return self.tty.error
        status = self.tty.touch([self.config_file])
        if status != self.tty.success:
            self.print_on_tty(
                self.tty.error_colour,
                f"Error creating '{self.config_file}' file\n"
            )
            return self.tty.error
        return self.tty.success

    def test_installation(self) -> int:
        """ Make sure that the kubectl is installed and operational """
        self.print_on_tty(
            self.tty.info_colour,
            "Testing the installation of Kubernetes for Windows\n"
        )
        self.tty.current_tty_status = self.run_command(
            "kubectl version --output=yaml"
        )
        if self.tty.current_tty_status != self.tty.success:
            self.print_on_tty(
                self.tty.error_colour,
                "Error testing the installation of Kubernetes for Windows\n"
            )
            return self.tty.current_tty_status
        self.tty.current_tty_status = self.tty.success
        return self.tty.current_tty_status

    def main(self) -> int:
        """ The main function in charge of installing kubernetes on windows """
        self.print_on_tty(self.tty.help_title_colour, "")
        self.disp.title("Downloading Kubernetes for Windows")
        self.print_on_tty(
            self.tty.default_colour,
            "Checking pre-installed package managers:\n"
        )
        self.update_extension_availability()
        status = self.use_available_method()
        if status != self.tty.success:
            self.print_on_tty(
                self.tty.error_colour,
                "Error installing Kubernetes for Windows\n"
            )
            self.tty.current_tty_status = self.tty.error
            return self.tty.error
        status = self.test_installation()
        if status != self.tty.success:
            self.print_on_tty(
                self.tty.error_colour,
                "Error installing Kubernetes for Windows\n"
            )
            self.tty.current_tty_status = self.tty.error
            return self.tty.error
        self.print_on_tty(
            self.tty.info_colour,
            """
The Path variable has been modified, it's effect has been applied in this program, and in any new instances that will be started.\n
If you want to use kubectl outside of this instance, please restart all the terminals (this could be your ssh connection).\n
"""
        )
        self.tty.current_tty_status = self.tty.success
        return self.tty.success

    def test_class_install_kubernetes_windows(self) -> int:
        """ Test the class install kubernetes windows """
        self.print_on_tty(
            self.tty.info_colour,
            "This is a test message from the install kubernetes windows class\n"
        )
        return self.tty.success
