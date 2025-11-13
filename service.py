from repo import Repo
from deployers import Deployer, DeployerFactory
from builders import Builder, BuilderFactory
from composed_objects import RepoDict
from typing import TypedDict, Any


class BuilderData(TypedDict):
    type: str
    config: dict[str, Any]


class DeployerData(TypedDict):
    type: str
    config: dict[str, Any]


class Service:
    def __init__(
        self, repo: Repo, builders: list[Builder], deployers: list[Deployer]
    ) -> None:
        self._repo = repo
        self._builders = builders
        self._deployers = deployers

    @property
    def repo(self) -> Repo:
        return self._repo

    @property
    def builders(self) -> list[Builder]:
        return self._builders

    @property
    def deployers(self) -> list[Deployer]:
        return self._deployers

    @classmethod
    def construct(
        cls,
        repo: RepoDict,
        builders_data: list[BuilderData],
        deployers_data: list[DeployerData],
    ) -> "Service":
        repository = Repo(url=repo["url"], branch=repo["branch"], commit=repo["commit"])
        builders: list[Builder] = []
        for b in builders_data:
            builder = BuilderFactory.create_builder(
                builder_type=b["type"], **b["config"]
            )
            builders.append(builder)
        deployers: list[Deployer] = []
        for d in deployers_data:
            deployer = DeployerFactory.get_deployer(
                deployer_type=d["type"], **d["config"]
            )
            deployers.append(deployer)
        return cls(repository, builders, deployers)
