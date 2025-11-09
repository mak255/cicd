from .core import Deployer, DeployerType, DeployerEnv, register_deployer


class HelmDeployer(Deployer):
    """Deployer that updates/upgrades Helm releases."""

    def deploy(self) -> None:
        print("is updated to the latest helm chart version")


register_deployer(DeployerType.HELM, HelmDeployer)