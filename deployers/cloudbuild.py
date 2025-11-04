from .core import Deployer, DeployerType, DeployerEnv, register_deployer


class CloudBuildDeployer(Deployer):
    """Deployer that triggers Cloud Build pipelines."""

    def deploy(self) -> None:
        print("is deployed using cloud build")


register_deployer(DeployerType.CLOUDBUILD, CloudBuildDeployer)