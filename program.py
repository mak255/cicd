from builder import BuilderType
from deployment import DeployerType, DeployerEnv
from typing import Any
import json
from service import Service, KustomizeConfig, CloudfunctionConfig, ArgoCDConfig


with open("services.json") as f:
    services: dict[str,Any] = json.load(f)

def get_builder_type(builder_type: str) -> BuilderType: 
    buider_map: dict[str,BuilderType]= {
        "dockerfile": BuilderType.DOCKER,
        "bake": BuilderType.BAKE,
        "helm": BuilderType.HELM,
        "gcloud": BuilderType.GCloudBuild
    }
    if builder_type.lower() not in ["dockerfile", "bake", "helm", "gcloud"]:
        raise ValueError(f"{builder_type} is not a valid type")
    
    return buider_map[builder_type.lower()]

def get_deployer_type(deployer_type: str) -> DeployerType: 
    deployer_map: dict[str,DeployerType]= {
        "kustomize": DeployerType.KUSTOMIZE,
        "helm": DeployerType.Helm,
        "argocd": DeployerType.ARGOCD,
        "gcloudbuild": DeployerType.CLOUDBUILD,
        "cloudfunction": DeployerType.CLOUDFUNCTION
    }
    if deployer_type.lower() not in ["kustomize", "helm", "argocd", "gcloudbuild","cloudfunction"]:
        raise ValueError(f"{deployer_type} is not a valid type")
    
    return deployer_map[deployer_type.lower()]
    
def set_kustomize(svc: Service,kustmize_conf : dict[str, Any]) -> None:
    kustomize : dict[DeployerEnv,list[KustomizeConfig]] = {}
    for env, env_confs in kustmize_conf.items():
        if env == "dev":
            deploy_env = DeployerEnv.DEV
        if env == "stage":
            deploy_env = DeployerEnv.STAGE
        if env == "prod":
            deploy_env = DeployerEnv.PROD
        kustomize_configs: list[KustomizeConfig] = []
        for env_conf in env_confs:
            kustomize_configs.append(KustomizeConfig(name= env_conf["name"],dir=env_conf["dir"], config_files=env_conf["cm_source"]))
        kustomize[deploy_env] = kustomize_configs
    svc.kustomize = kustomize

def set_cloudfunction_property(svc: Service, cloudfunctino_conf: dict[str,Any]) -> None:
    cloudfunction : dict[DeployerEnv,list[CloudfunctionConfig]] = {}
    for env, env_confs in cloudfunctino_conf.items():
        if env == "dev":
            deploy_env = DeployerEnv.DEV
        if env == "stage":
            deploy_env = DeployerEnv.STAGE
        if env == "prod":
            deploy_env = DeployerEnv.PROD
        cloudfunction_configs: list[CloudfunctionConfig] = []
        for env_conf in env_confs:
            cloudfunction_configs.append(CloudfunctionConfig(name= env_conf["name"],deploy_file=env_conf["deploy_file"]))
        cloudfunction[deploy_env] = cloudfunction_configs
    svc.cloudfunction = cloudfunction

def set_argocd_property(svc: Service, argocd_conf: dict[str,Any]) -> None:
    argocd : dict[DeployerEnv,list[ArgoCDConfig]] = {}
    for env, env_confs in argocd_conf.items():
        if env == "dev":
            deploy_env = DeployerEnv.DEV
        if env == "stage":
            deploy_env = DeployerEnv.STAGE
        if env == "prod":
            deploy_env = DeployerEnv.PROD
        argocd_configs: list[ArgoCDConfig] = []
        for env_conf in env_confs:
            argocd_configs.append(ArgoCDConfig(app_file=env_conf["argo_app_file"], image_parameters=env_conf["image_parameters"]))
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
        set_kustomize(service,svc_def["kubernetes"])
    if DeployerType.CLOUDFUNCTION in service.deployers:
        set_cloudfunction_property(service,svc_def["cloudfunction"])
    if DeployerType.ARGOCD in service.deployers:
        set_argocd_property(service,svc_def["argocd"])
    print(f"argocd: {service.argocd}")
    print(f"kustomize: {service.kustomize}")
    if service.kustomize is not None:
        print(f"{service.kustomize[DeployerEnv.DEV][0].name} kustomize dir is {service.kustomize[DeployerEnv.DEV][0].dir}")
    print(f"helm: {service.helm}")
    print(f"cloudfunction: {service.cloudfunction}") 
    if service.cloudfunction is not None:
        print(f"{service.cloudfunction[DeployerEnv.DEV][0].name} deploy file is {service.cloudfunction[DeployerEnv.DEV][0].deploy_file}")