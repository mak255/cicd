from enum import Enum, auto
from abc import ABC, abstractmethod
from typing import Type

class BuilderType(Enum):
    DOCKER = auto()
    BAKE = auto()
    GCloudBuild = auto()
    HELM = auto()

        
class Builder(ABC):
    @abstractmethod
    def build(self):
        pass

class DocekrBuilder(Builder):
    def build(self):
        print(f"setting the docker builder")

class BakeBuilder(Builder):
    def build(self):
        print(f"setting the bake builder")
    
class GCloudBuilder(Builder):
    def build(self):
        print(f" setting the gcloud builder")

class HelmBuilder(Builder):
    def build(self):
        print(f" setting the helm builder") 

class BuilderFactory():
    @classmethod
    def get_builder(cls,builder_type: BuilderType) -> Builder:
        BUILDER_DISPATCH: dict[BuilderType, Type[Builder]] = {
        BuilderType.DOCKER: DocekrBuilder,
        BuilderType.BAKE: BakeBuilder,
        BuilderType.GCloudBuild: GCloudBuilder,
        BuilderType.HELM: HelmBuilder,
        }
        return BUILDER_DISPATCH[builder_type]()
        
