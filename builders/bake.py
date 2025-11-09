from .core import Builder, BuilderType, register_builder


class BakeBuilder(Builder):
    """Bake (Buildx Bake) builder example."""

    def build(self) -> None:
        print("setting the bake builder")


register_builder(BuilderType.BAKE, BakeBuilder)
