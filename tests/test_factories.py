"""
Thoughts:
- quick unit tests for factories: ensure mapping->concrete class
- keep tests fast, no external side effects
- import resilience: pytest may run from project root or as package
    so adjust sys.path to make local imports reliable in CI and local runs
- assert by class name to avoid importing concrete class symbols (looser
    coupling). not testing runtime deploy/build logic here, just wiring.
"""

import pytest
import sys
import os

# Ensure project root is on sys.path so imports like 'builder' work when
# pytest's CWD is the project directory.
ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if ROOT not in sys.path:
        sys.path.insert(0, ROOT)

from builders import BuilderFactory, BuilderType, Builder
from deployers import DeployerFactory, DeployerType, DeployerEnv


def test_builder_factory_returns_builder_instance():
    b = BuilderFactory.get_builder(BuilderType.DOCKER)
    assert isinstance(b, Builder)
    assert b.__class__.__name__ == "DockerBuilder"


def test_deployer_factory_returns_correct_type():
    d = DeployerFactory.get_deployer(DeployerType.KUSTOMIZE, DeployerEnv.DEV, "v1.0.0")
    # Check by class name to avoid importing concrete class directly
    assert d.__class__.__name__ == "KustomizeDeployer"
    assert hasattr(d, "deploy")
