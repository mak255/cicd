from dataclasses import dataclass

from .deployer import Deployer, DeployerType, register_deployer


@dataclass
class KustomizeDeployer(Deployer):
    """Deployer that uses kustomize manifests."""

    manifest_url: str
    dir: str
    image_tag: str
    image_name: str

    def deploy(self) -> None:
        print("is deployed using kustomize")


register_deployer(DeployerType.KUSTOMIZE, KustomizeDeployer)
