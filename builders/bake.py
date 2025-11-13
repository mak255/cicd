from .builder import Builder


class BakeBuilder(Builder):
    """Bake (Buildx Bake) builder example."""

    def build(self) -> None:
        print("setting the bake builder")
