from .builder import Builder


class GCloudBuilder(Builder):
    """Google Cloud Build builder example."""

    def build(self) -> None:
        print("setting the gcloud builder")
