from enum import Enum, auto
from abc import ABC, abstractmethod
from typing import Type

class DeployerType(Enum):
    KUSTOMIZE = auto()
    ARGOCD = auto()
    CLOUDFUNCTION = auto()
    CLOUDBUILD = auto()
    Helm = auto()

class DeployerEnv(Enum):
    DEV = auto()
    STAGE = auto()
    PROD =  auto()

class Deployer(ABC):
    def __init__(self, env: DeployerEnv, tag: str):
        self._env = env
        self._tag = tag
    @abstractmethod
    def deploy(self):
        pass

class KustomizeDeployer(Deployer):  
    def deploy(self):
        print(f"is deployed using kustomize")
        print(f"in environement: {self._env}")
        print(f"image_tag : {self._tag}")

class ARGOCDDeployer(Deployer):
    def deploy(self):
        print(f"is deployed using Argocd application")

class CloudFunctionDeployer(Deployer):
    def deploy(self):
        print(f"is deployed using clousrunfunction application")

class HelmDeployer(Deployer):
    def deploy(self):
        print(f"is update to the latest helm chart version")

class CloudBuildDeployer(Deployer):
    def deploy(self):
        print(f"is deployed using the cloud build")

class DeployerFactory:
    @classmethod
    def get_deployer(cls,deployer_type: DeployerType, env: DeployerEnv, tag: str) -> Deployer:
        DEPOLOYER_DISPATCH: dict[DeployerType, Type[Deployer]] = {
        DeployerType.KUSTOMIZE: KustomizeDeployer,
        DeployerType.ARGOCD: ARGOCDDeployer,
        DeployerType.CLOUDFUNCTION: CloudFunctionDeployer,
        DeployerType.Helm: HelmDeployer,
        DeployerType.CLOUDBUILD: CloudBuildDeployer
        }
        return DEPOLOYER_DISPATCH[deployer_type](env, tag)