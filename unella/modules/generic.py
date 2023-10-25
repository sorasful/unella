import abc
import pathlib
from dataclasses import dataclass, field


@dataclass
class Report(abc.ABC):
    project_to_audit: str
    project_path: pathlib.Path = field(init=False)

    def __post_init__(self) -> None:
        self.project_path = pathlib.Path(self.project_to_audit)

    @abc.abstractmethod
    def perform_analysis(self) -> None:
        raise NotImplementedError

    @abc.abstractmethod
    def get_results(self):
        raise NotImplementedError
