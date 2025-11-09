from .core import Deployer, DeployerType, DeployerEnv, register_deployer


class KustomizeDeployer(Deployer):
    """Deployer that uses kustomize manifests."""

    def deploy(self) -> None:
        print("is deployed using kustomize")
        print(f"in environment: {self._env}")
        print(f"image_tag : {self._tag}")


register_deployer(DeployerType.KUSTOMIZE, KustomizeDeployer)