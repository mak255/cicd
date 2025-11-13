from dataclasses import dataclass

from .builder import Builder


@dataclass
class DockerBuilder(Builder):
    """Dockerfile-based builder example."""

    dockerfile: str
    dockerfile_path: str
    context_path: str
    registry: str
    tags: list[str]
    push: bool

    def build(self) -> None:
        print("setting the docker builder")
