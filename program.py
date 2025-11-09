"""Small program that reads service definitions and wires builders/deployers.

This script reads `services.json` (a dict of service definitions) and
constructs `Service` objects populated with builder and deployer
configurations. It demonstrates how the `Service`, builder and deployer
datatypes are used in the repository.
"""

from typing import Any
from builders import BuilderType
from deployers import DeployerType, DeployerEnv
import json
from service import Service, KustomizeConfig, CloudfunctionConfig, ArgoCDConfig


with open("services.json") as f:
    services: dict[str, Any] = json.load(f)


def get_builder_type(builder_type: str) -> BuilderType:
    """Return the `BuilderType` for the given user-facing string.

    Accepts case-insensitive names: 'dockerfile', 'bake', 'helm', 'gcloud'.
    Raises ValueError for unknown values.
    """
    builder_map: dict[str, BuilderType] = {
        "dockerfile": BuilderType.DOCKER,
        "bake": BuilderType.BAKE,
        "helm": BuilderType.HELM,
        "gcloud": BuilderType.GCloudBuild,
    }

    key = builder_type.lower()
    if key not in builder_map:
        raise ValueError(f"{builder_type} is not a valid type")

    return builder_map[key]


def get_deployer_type(deployer_type: str) -> DeployerType:
    """Return the `DeployerType` for the given user-facing string.

    Accepts case-insensitive names: 'kustomize', 'helm', 'argocd',
    'gcloudbuild', 'cloudfunction'.
    """
    deployer_map: dict[str, DeployerType] = {
        "kustomize": DeployerType.KUSTOMIZE,
        "helm": DeployerType.HELM,
        "argocd": DeployerType.ARGOCD,
        "gcloudbuild": DeployerType.CLOUDBUILD,
        "cloudfunction": DeployerType.CLOUDFUNCTION,
    }

    key = deployer_type.lower()
    if key not in deployer_map:
        raise ValueError(f"{deployer_type} is not a valid type")

    return deployer_map[key]


def _env_from_str(env: str) -> DeployerEnv:
    """Helper to map a lowercase environment name to a DeployerEnv.

    Raises KeyError if the environment name is unknown.
    """
    mapping = {"dev": DeployerEnv.DEV, "stage": DeployerEnv.STAGE, "prod": DeployerEnv.PROD}
    return mapping[env.lower()]


def set_kustomize(svc: Service, kustomize_conf: dict[str, Any]) -> None:
    """Populate the service's kustomize property from a dict loaded from JSON.

    The input is expected to be a mapping of environment name to a list of
    kustomize overlay definitions.
    """
    kustomize: dict[DeployerEnv, list[KustomizeConfig]] = {}
    for env, env_confs in kustomize_conf.items():
        deploy_env = _env_from_str(env)
        kustomize_configs: list[KustomizeConfig] = []
        for env_conf in env_confs:
            kustomize_configs.append(
                KustomizeConfig(name=env_conf["name"], dir=env_conf["dir"], config_files=env_conf["cm_source"])
            )
        kustomize[deploy_env] = kustomize_configs
    svc.kustomize = kustomize


def set_cloudfunction_property(svc: Service, cloudfunction_conf: dict[str, Any]) -> None:
    """Populate the service's cloudfunction property from a JSON-derived dict."""
    cloudfunction: dict[DeployerEnv, list[CloudfunctionConfig]] = {}
    for env, env_confs in cloudfunction_conf.items():
        deploy_env = _env_from_str(env)
        cloudfunction_configs: list[CloudfunctionConfig] = []
        for env_conf in env_confs:
            cloudfunction_configs.append(
                CloudfunctionConfig(name=env_conf["name"], deploy_file=env_conf["deploy_file"])
            )
        cloudfunction[deploy_env] = cloudfunction_configs
    svc.cloudfunction = cloudfunction


def set_argocd_property(svc: Service, argocd_conf: dict[str, Any]) -> None:
    """Populate the service's argocd property from a JSON-derived dict."""
    argocd: dict[DeployerEnv, list[ArgoCDConfig]] = {}
    for env, env_confs in argocd_conf.items():
        deploy_env = _env_from_str(env)
        argocd_configs: list[ArgoCDConfig] = []
        for env_conf in env_confs:
            argocd_configs.append(
                ArgoCDConfig(app_file=env_conf["argo_app_file"], image_parameters=env_conf["image_parameters"])
            )
        argocd[deploy_env] = argocd_configs
    svc.argocd = argocd


for svc, svc_def in services.items():
    name = svc

    builders: list[BuilderType] = []
    build_types: list[str] = svc_def["builders"]
    for build_type in build_types:
        builders.append(get_builder_type(build_type))

    deployers: list[DeployerType] = []
    deploy_types: list[str] = svc_def["deployers"]
    for deploy_type in deploy_types:
        deployers.append(get_deployer_type(deploy_type))

    service = Service(name=name, builders=builders, deployers=deployers)
    print(service)

    if DeployerType.KUSTOMIZE in service.deployers:
        set_kustomize(service, svc_def["kubernetes"])
    if DeployerType.CLOUDFUNCTION in service.deployers:
        set_cloudfunction_property(service, svc_def["cloudfunction"])
    if DeployerType.ARGOCD in service.deployers:
        set_argocd_property(service, svc_def["argocd"])

    print(f"argocd: {service.argocd}")
    print(f"kustomize: {service.kustomize}")
    if service.kustomize is not None:
        print(f"{service.kustomize[DeployerEnv.DEV][0].name} kustomize dir is {service.kustomize[DeployerEnv.DEV][0].dir}")
    print(f"helm: {service.helm}")
    print(f"cloudfunction: {service.cloudfunction}")
    if service.cloudfunction is not None:
        print(f"{service.cloudfunction[DeployerEnv.DEV][0].name} deploy file is {service.cloudfunction[DeployerEnv.DEV][0].deploy_file}")