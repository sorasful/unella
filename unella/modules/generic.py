import abc
import pathlib
from dataclasses import dataclass, field

from jinja2 import Environment, FileSystemLoader

from unella.utils import pascal_case_to_snake_case


@dataclass
class Report(abc.ABC):
    project_to_audit: str
    project_path: pathlib.Path = field(init=False)

    def __post_init__(self) -> None:
        self.project_path = pathlib.Path(self.project_to_audit)

    @property
    @abc.abstractmethod
    def is_available(self) -> bool:
        """
        A property to test if the report is valid int the current context or not.
        For example if the commands are installed.
        """
        raise NotImplementedError

    @abc.abstractmethod
    def perform_analysis(self) -> None:
        raise NotImplementedError

    @abc.abstractmethod
    def get_results(self):
        raise NotImplementedError

    def to_html(self) -> str:
        env = Environment(loader=FileSystemLoader("html_templates/modules"))
        template_name = f"{pascal_case_to_snake_case(self.__class__.__name__)}_template.html"
        template = env.get_template(template_name)
        return template.render(data=self.get_results())

    def to_markdown(self) -> str:
        env = Environment(loader=FileSystemLoader("markdown_templates/modules"))
        template_name = f"{pascal_case_to_snake_case(self.__class__.__name__)}_template.md"
        template = env.get_template(template_name)
        return template.render(data=self.get_results())
