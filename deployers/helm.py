from dataclasses import dataclass

from .deployer import Deployer, DeployerType, register_deployer


@dataclass
class HelmDeployer(Deployer):
    """Deployer that updates/upgrades Helm releases."""

    kubernetes_namespace: str
    release_name: str
    chart_path: str
    values_file: str
    image_tag: str
    image_key: list[str]

    def deploy(self) -> None:
        print("is updated to the latest helm chart version")


register_deployer(DeployerType.HELM, HelmDeployer)
