import sys
import constants as CONST
from services import Docker, DockerCompose, Kubernetes
from tty_ov import TTY, ColouriseOutput, AskQuestion


class Main:
    """ The main class of the program """

    def __init__(self, colourise_output: bool = True) -> None:
        super().__init__()
        self.err = CONST.ERR
        self.error = CONST.ERROR
        self.success = CONST.SUCCESS
        self.colours = CONST.COLOURS
        # finish the imports
        self.co = ColouriseOutput()
        self.aq = AskQuestion()
        self.tty = TTY(
            self.err,
            self.error,
            self.success,
            self.co,
            self.aq,
            CONST.COLOURS,
            colourise_output
        )
        self.tty.load_basics()
        self.docker = Docker(self.success, self.err, self.error, self.tty)
        self.docker_compose = DockerCompose(
            self.success,
            self.err,
            self.error,
            self.tty
        )
        self.kubernetes = Kubernetes(
            self.success,
            self.err,
            self.error,
            self.tty
        )

    def call_injectors(self) -> None:
        """ The function in charge of calling the injectors of the classes """
        status = self.docker.injector()
        if status != self.success:
            self.tty.print_on_tty(
                self.tty.error_colour,
                "Error while injecting tty with the Docker class\n"
            )
        status = self.docker_compose.injector()
        if status != self.success:
            self.tty.print_on_tty(
                self.tty.error_colour,
                "Error while injecting tty with the Docker Compose class\n"
            )
        status = self.kubernetes.injector()
        if status != self.success:
            self.tty.print_on_tty(
                self.tty.error_colour,
                "Error while injecting tty with the Kubernetes class\n"
            )

    def compile_characters(self, char: str = " ", nb: int = 5) -> str:
        """ Compile a string of characters """
        string = ""
        index = 0
        while index < nb:
            string += char
            index += 1
        return string

    def add_spacing(self) -> None:
        """ Add some spacing between the loading function and the title """
        spacing = self.compile_characters("\n", 2)
        self.tty.print_on_tty(
            self.tty.default_colour,
            spacing
        )

    def run_command(self, args: list) -> int:
        """ Run a command in parent langage """
        help_command = "run"
        if self.tty.help_function_child_name == help_command:
            help_description = f"""
This is a command that allows you to run a command on the parent shell.
Input:
    {help_command} <your command>
Output:
    The result of the command you ran.
Example:
Input:
    {help_command} echo "Hello World"
Output:
    Hello World
"""
            self.tty.function_help(help_command, help_description)
            self.tty.current_tty_status = self.success
            return self.success
        if len(args) < 1:
            self.tty.print_on_tty(
                self.tty.error_colour,
                "You need to specify a command to run\n"
            )
            self.tty.current_tty_status = self.error
            return self.error
        command = " ".join(args)
        self.tty.print_on_tty(
            self.tty.default_colour,
            f"Running command: {command}\n"
        )
        status = self.tty.run_external_command(command)
        if status != self.success:
            self.tty.print_on_tty(
                self.tty.error_colour,
                "Error while running command\n"
            )
            self.tty.current_tty_status = self.error
            return self.error
        self.tty.current_tty_status = self.success
        return self.success

    def main(self) -> None:
        """ The main function of the program """
        self.call_injectors()
        self.add_spacing()
        status = self.tty.mainloop()
        self.tty.unload_basics()
        print()
        sys.exit(status)


if __name__ == "__main__":
    COLOURISE_OUTPUT = True
    if "-nc" in sys.argv or "--no-colour" in sys.argv:
        COLOURISE_OUTPUT = False
    main = Main(COLOURISE_OUTPUT)
    main.main()
