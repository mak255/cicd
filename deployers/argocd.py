from typing import Literal

from .deployer import Deployer, DeployerType, register_deployer
from ..repo import Repo


class ARGOCDDeployer(Deployer):
    """Deployer that creates/updates ArgoCD applications."""

    image_tag: str
    app_type: Literal["kustomize", "helm"]
    app_manifest: str
    app_manifest_dir: str
    app_manifest_repo: Repo

    def deploy(self) -> None:
        print("is deployed using ArgoCD application")


register_deployer(DeployerType.ARGOCD, ARGOCDDeployer)
