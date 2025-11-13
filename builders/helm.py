from dataclasses import dataclass

from .builder import Builder


@dataclass
class HelmBuilder(Builder):
    chart_directory: str
    app_version: str
    chart_version: str
    registry: str
    push: bool

    def build(self) -> None:
        print("setting the helm builder")
