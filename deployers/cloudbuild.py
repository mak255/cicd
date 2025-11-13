from .deployer import Deployer, DeployerType, register_deployer


class GCloudBuildDeployer(Deployer):
    """Deployer that triggers Cloud Build pipelines."""

    def deploy(self) -> None:
        print("is deployed using cloud build")


register_deployer(DeployerType.GCLOUDBUILD, GCloudBuildDeployer)
