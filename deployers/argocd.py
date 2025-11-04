from .core import Deployer, DeployerType, DeployerEnv, register_deployer


class ARGOCDDeployer(Deployer):
    """Deployer that creates/updates ArgoCD applications."""

    def deploy(self) -> None:
        print("is deployed using ArgoCD application")


register_deployer(DeployerType.ARGOCD, ARGOCDDeployer)