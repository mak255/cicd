"""Builder types and plugin registry.
See sibling modules for concrete implementations."""

from enum import Enum, auto
from dataclasses import dataclass
from abc import abstractmethod

# DockerBuilder will be imported dynamically to avoid circular dependency


class BuilderType(Enum):
    DOCKER = auto()
    BAKE = auto()
    GCLOUD = auto()
    HELM = auto()


@dataclass
class Builder:
    type: BuilderType

    @abstractmethod
    def build(self) -> None: ...
