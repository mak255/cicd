"""Deployer types and plugin registry.
See sibling modules for concrete implementations."""

from enum import Enum, auto
from abc import ABC, abstractmethod
from typing import Type, Dict
import importlib

class DeployerType(Enum):
    KUSTOMIZE = auto()
    ARGOCD = auto()
    CLOUDFUNCTION = auto()
    CLOUDBUILD = auto()
    HELM = auto()

class DeployerEnv(Enum):
    DEV = auto()
    STAGE = auto()
    PROD = auto()

class Deployer(ABC):
    def __init__(self, env: DeployerEnv, tag: str):
        self._env = env
        self._tag = tag

    @abstractmethod
    def deploy(self) -> None: ...

_DEPLOYER_DISPATCH: Dict[DeployerType, Type[Deployer]] = {}

def register_deployer(deployer_type: DeployerType, cls: Type[Deployer]) -> None:
    _DEPLOYER_DISPATCH[deployer_type] = cls

class DeployerFactory:
    @classmethod
    def get_deployer(cls, deployer_type: DeployerType, env: DeployerEnv, tag: str) -> Deployer:
        try:
            importlib.import_module("cicd.deployers")
        except ModuleNotFoundError:
            pass  # no deployers registered
        if deployer_type not in _DEPLOYER_DISPATCH:
            raise KeyError(f"No deployer registered for {deployer_type}")
        return _DEPLOYER_DISPATCH[deployer_type](env, tag)