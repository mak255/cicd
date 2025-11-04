
"""Service configuration dataclasses and the `Service` container.

This module contains lightweight dataclasses that represent per-environment
deployment configuration (kustomize manifests, Helm charts, Cloud Function
deploy files, and ArgoCD application descriptors). The `Service` dataclass
collects those per-service mappings and exposes simple properties to read and
set them.

These classes are intentionally small and used by `program.py` to wire
service definitions from `services.json` into the CI/CD scaffolding.
"""

from dataclasses import dataclass
from deployers import DeployerType, DeployerEnv
from builders import BuilderType


@dataclass
class KustomizeConfig:
    """Configuration needed to apply a Kustomize overlay.

    Attributes:
        name: logical name of the overlay
        dir: filesystem directory containing the kustomize overlay
        config_files: list of configmap/secret sources referenced by the overlay
    """

    name: str
    dir: str
    config_files: list[str]


@dataclass
class HelmConfig:
    """Small wrapper for a Helm chart filename or chart reference."""

    filename: str


@dataclass
class CloudfunctionConfig:
    """Information required to deploy a Cloud Function or Cloud Run service."""

    name: str
    deploy_file: str


@dataclass
class ArgoCDConfig:
    """Configuration for an ArgoCD Application descriptor.

    Attributes:
        app_file: path to the ArgoCD app manifest
        image_parameters: list of parameters for injecting image tags
    """

    app_file: str
    image_parameters: list[str]


@dataclass
class Service:
    """Representation of a service and its build/deploy configurations.

    Fields:
        name: service name
        deployers: list of DeployerType values used by this service
        builders: list of BuilderType values used to build this service

    Per-environment configuration fields (kustomize/helm/cloudfunction/argocd)
    are stored internally and exposed via properties.
    """

    name: str
    deployers: list[DeployerType]
    builders: list[BuilderType]
    _kustomize: dict[DeployerEnv, list[KustomizeConfig]] | None = None
    _helm: dict[DeployerEnv, list[HelmConfig]] | None = None
    _cloudfunction: dict[DeployerEnv, list[CloudfunctionConfig]] | None = None
    _argocd: dict[DeployerEnv, list[ArgoCDConfig]] | None = None

    def pull(self) -> None:
        """Placeholder for fetching source artifacts for the service.

        In a real system this might clone a repo or download artifacts. Left
        as a placeholder here.
        """
        ...

    @property
    def kustomize(self) -> dict[DeployerEnv, list[KustomizeConfig]] | None:
        return self._kustomize

    @kustomize.setter
    def kustomize(self, kustomize: dict[DeployerEnv, list[KustomizeConfig]]) -> None:
        """Set per-environment Kustomize configurations."""
        self._kustomize = kustomize

    @property
    def helm(self) -> dict[DeployerEnv, list[HelmConfig]] | None:
        return self._helm

    @helm.setter
    def helm(self, helm: dict[DeployerEnv, list[HelmConfig]]) -> None:
        """Set per-environment Helm chart configurations."""
        self._helm = helm

    @property
    def cloudfunction(self) -> dict[DeployerEnv, list[CloudfunctionConfig]] | None:
        return self._cloudfunction

    @cloudfunction.setter
    def cloudfunction(self, cloudfunction: dict[DeployerEnv, list[CloudfunctionConfig]]) -> None:
        """Set per-environment cloud function deployment info."""
        self._cloudfunction = cloudfunction

    @property
    def argocd(self) -> dict[DeployerEnv, list[ArgoCDConfig]] | None:
        return self._argocd

    @argocd.setter
    def argocd(self, argocd: dict[DeployerEnv, list[ArgoCDConfig]]) -> None:
        """Set per-environment ArgoCD application configurations."""
        self._argocd = argocd


