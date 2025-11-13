from dataclasses import dataclass


@dataclass
class Repo:
    url: str
    branch: str
    commit: str
