from service import RepoDict, BuilderData, Service, DeployerData


def main() -> None:
    repo_info: RepoDict = {
        "url": "https://github.com/user/repo.git",
        "branch": "main",
        "commit": "abcdef1234567890",
    }
    builders_data: list[BuilderData] = [
        {
            "type": "docker",
            "config": {
                "dockerfile": "Dockerfile",
                "dockerfile_path": "path/to/Dockerfile",
                "context_path": "path/to/context",
                "registry": "my-registry",
                "tags": ["latest"],
                "push": True,
            },
        },
        {
            "type": "helm",
            "config": {
                "chart_directory": "charts/my-app",
                "app_version": "1.0.0",
                "chart_version": "1.0.0",
                "registry": "my-helm-registry",
                "push": True,
            },
        },
    ]
    deployers: list[DeployerData] = [
        {
            "type": "helm",
            "config": {
                "kubernetes_namespace": "default",
                "release_name": "my-app-release",
                "chart_path": "charts/my-app",
                "values_file": "charts/my-app/values.yaml",
                "image_tag": "latest",
                "image_key": ["image", "tag"],
            },
        }
    ]
    service = Service.construct(repo_info, builders_data, deployers)
    print(f"Service constructed with repo: {service.repo}")
    print(f"Service constructed with builders: {service.builders}")
    print(f"Service constructed with deployers: {service.deployers}")

    for builder in service.builders:
        builder.build()

    for deployer in service.deployers:
        deployer.deploy()


if __name__ == "__main__":
    main()
