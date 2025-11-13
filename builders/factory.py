from typing import Any, Type

from .builder import BuilderType, Builder
from .docker import DockerBuilder
from .helm import HelmBuilder
from .gcloud import GCloudBuilder

_BUILDER_DISPATCH: dict[BuilderType, Type[Builder]] = {
    BuilderType.DOCKER: DockerBuilder,
    BuilderType.HELM: HelmBuilder,
    BuilderType.GCLOUD: GCloudBuilder,
}


class BuilderFactory:
    @staticmethod
    def create_builder(builder_type: str, **kwargs: Any | dict[str, Any]) -> Builder:
        builder_class = _BUILDER_DISPATCH.get(BuilderType[builder_type.upper()])
        if not builder_class:
            raise ValueError(f"Unknown builder type: {builder_type}")
        return builder_class(type=BuilderType[builder_type.upper()], **kwargs)


def main() -> None:
    builder = BuilderFactory.create_builder(
        builder_type="gcloud",
    )

    print(f"Created builder: {builder}")
    builder.build()


if __name__ == "__main__":
    main()
