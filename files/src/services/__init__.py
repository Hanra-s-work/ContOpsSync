"""
File in charge of grouping the sub-classes that are in charge of managing the different services
"""
from .docker import Docker
from .docker_compose import DockerCompose
from .kubernetes import Kubernetes


class Services:
    """ The class in charge of managing the services """

    def __init__(self) -> None:
        super().__init__()
        self.docker = Docker
        self.docker_compose = DockerCompose
        self.kubernetes = Kubernetes
