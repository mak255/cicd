from .core import Builder, BuilderType, register_builder


class HelmBuilder(Builder):
    """Helm builder example."""

    def build(self) -> None:
        print("setting the helm builder")


register_builder(BuilderType.HELM, HelmBuilder)
