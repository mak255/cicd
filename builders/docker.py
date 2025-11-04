from .core import Builder, BuilderType, register_builder


class DockerBuilder(Builder):
    """Dockerfile-based builder example."""

    def build(self) -> None:
        print("setting the docker builder")


# register on import
register_builder(BuilderType.DOCKER, DockerBuilder)
