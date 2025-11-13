from typing import Any, Type
from .deployer import Deployer, DeployerType
from .helm import HelmDeployer

_DEPLOYER_DISPATCH: dict[DeployerType, Type[Deployer]] = {
    DeployerType.HELM: HelmDeployer,
}


class DeployerFactory:
    @staticmethod
    def get_deployer(deployer_type: str, **kwargs: dict[str, Any]) -> Deployer:
        dtype = DeployerType[deployer_type.upper()]
        deployer_cls = _DEPLOYER_DISPATCH.get(dtype)
        if not deployer_cls:
            raise ValueError(f"No deployer registered for type: {deployer_type}")
        return deployer_cls(**kwargs)
