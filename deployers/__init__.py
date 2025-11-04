"""Deployer package: core types and plugin registry.
Import deployers.{core,kustomize,argocd,...} for specific implementations.
Re-exports core types for backward compatibility."""

from .core import (  # noqa: F401
    DeployerType,
    DeployerEnv,
    Deployer,
    DeployerFactory,
    register_deployer,
)

import pkgutil
from importlib import import_module

__all__ = []
for finder, name, ispkg in pkgutil.iter_modules(__path__):
    if name != "core":  # core already imported above
        import_module(f"{__name__}.{name}")
        __all__.append(name)