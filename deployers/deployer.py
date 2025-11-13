"""Deployer types and plugin registry.
See sibling modules for concrete implementations."""

from enum import Enum, auto
from abc import ABC, abstractmethod
from typing import Type, Dict


class DeployerType(Enum):
    KUSTOMIZE = auto()
    ARGOCD = auto()
    CLOUDFUNCTION = auto()
    GCLOUDBUILD = auto()
    HELM = auto()


class Deployer(ABC):
    deployer_type: DeployerType

    @abstractmethod
    def deploy(self) -> None: ...


_DEPLOYER_DISPATCH: Dict[DeployerType, Type[Deployer]] = {}


def register_deployer(deployer_type: DeployerType, cls: Type[Deployer]) -> None:
    _DEPLOYER_DISPATCH[deployer_type] = cls
