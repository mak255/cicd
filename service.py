from dataclasses import dataclass
from deployment import DeployerType, DeployerEnv
from builder import BuilderType

@dataclass
class KustomizeConfig:
    name: str
    dir: str
    config_files: list[str]

@dataclass
class HelmConfig:
    filename: str

@dataclass
class CloudfunctionConfig:
    name: str
    deploy_file: str

@dataclass
class ArgoCDConfig:
    app_file: str
    image_parameters: list[str]

@dataclass
class Service:
    name: str
    deployers: list[DeployerType]
    builders: list[BuilderType]
    _kustomize: dict[DeployerEnv, list[KustomizeConfig]] | None = None
    _helm: dict[DeployerEnv, list[HelmConfig]] | None = None
    _cloudfunction: dict[DeployerEnv,list[CloudfunctionConfig]] | None = None
    _argocd: dict[DeployerEnv, list[ArgoCDConfig]] | None = None

    def pull(self):
        ...
    @property
    def kustomize(self) -> dict[DeployerEnv, list[KustomizeConfig]] | None:
        return self._kustomize
    
    @kustomize.setter
    def kustomize(self, kustomize: dict[DeployerEnv, list[KustomizeConfig]]) -> None:
        self._kustomize = kustomize

    @property
    def helm(self) -> dict[DeployerEnv, list[HelmConfig]] | None:
        return self._helm
    
    @helm.setter
    def helm(self, helm: dict[DeployerEnv, list[HelmConfig]]) -> None:
        self._helm = helm

    @property
    def cloudfunction(self) -> dict[DeployerEnv,list[CloudfunctionConfig]] | None:
        return self._cloudfunction
    
    @cloudfunction.setter
    def cloudfunction(self, cloudfunction: dict[DeployerEnv,list[CloudfunctionConfig]]) -> None:
        self._cloudfunction = cloudfunction

    @property
    def argocd(self) -> dict[DeployerEnv, list[ArgoCDConfig]] | None:
        return self._argocd
    
    @argocd.setter
    def argocd(self, argocd: dict[DeployerEnv, list[ArgoCDConfig]]) -> None:
        self._argocd = argocd


