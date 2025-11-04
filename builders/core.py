"""Builder types and plugin registry.
See sibling modules for concrete implementations."""

from enum import Enum, auto
from abc import ABC, abstractmethod
from typing import Type, Dict
import importlib

class BuilderType(Enum):
    DOCKER = auto()
    BAKE = auto()
    GCloudBuild = auto()
    HELM = auto()

class Builder(ABC):
    @abstractmethod
    def build(self) -> None: ...

_BUILDER_DISPATCH: Dict[BuilderType, Type[Builder]] = {}

def register_builder(builder_type: BuilderType, cls: Type[Builder]) -> None:
    _BUILDER_DISPATCH[builder_type] = cls

class BuilderFactory:
    @classmethod
    def get_builder(cls, builder_type: BuilderType) -> Builder:
        try:
            importlib.import_module("cicd.builders")
        except ModuleNotFoundError:
            pass  # no builders registered
        if builder_type not in _BUILDER_DISPATCH:
            raise KeyError(f"No builder registered for {builder_type}")
        return _BUILDER_DISPATCH[builder_type]()