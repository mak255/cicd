"""Builder package: core types and plugin registry.
Import builders.{core,docker,bake,...} for specific implementations.
Re-exports core types for backward compatibility."""

from .core import (  # noqa: F401
    BuilderType,
    Builder,
    BuilderFactory,
    register_builder,
)

import pkgutil
from importlib import import_module

__all__ = []
for finder, name, ispkg in pkgutil.iter_modules(__path__):
    if name != "core":  # core already imported above
        import_module(f"{__name__}.{name}")
        __all__.append(name)
