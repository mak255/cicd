from .core import Builder, BuilderType, register_builder


class GCloudBuilder(Builder):
    """Google Cloud Build builder example."""

    def build(self) -> None:
        print("setting the gcloud builder")


register_builder(BuilderType.GCloudBuild, GCloudBuilder)
