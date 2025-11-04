from .core import Deployer, DeployerType, DeployerEnv, register_deployer


class CloudFunctionDeployer(Deployer):
    """Deployer for Cloud Function/Cloud Run services."""

    def deploy(self) -> None:
        print("is deployed using cloud function / cloud run")


register_deployer(DeployerType.CLOUDFUNCTION, CloudFunctionDeployer)