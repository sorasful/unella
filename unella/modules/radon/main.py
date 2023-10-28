import json
import re
import subprocess
from dataclasses import dataclass
import typing as t

from unella.modules.generic import Report


class ComplexityDict(t.TypedDict):
    col_offset: int
    complexity: float
    endline: int
    lineno: int
    name: str
    rank: str
    type: str


class RadonReportData(t.TypedDict):
    average_complexity: float
    complexity: dict[str, list[ComplexityDict]]


@dataclass
class RadonReport(Report):
    _data: RadonReportData | None = None

    def perform_analysis(self) -> None:
        self._data = {}
        self._data["average_complexity"] = self.get_project_average_complexity()
        self._data["complexity"] = self.get_project_parts_complexity()

    def get_results(self) -> RadonReportData:
        if self._data is None:
            self.perform_analysis()
        return self._data

    def get_project_average_complexity(self) -> float:
        """
        Used to return the averaged complexity of the whole project.
        """
        cmd = f'radon cc {self.project_path} -a -e "**/venv/*"'
        cmd_output = subprocess.check_output(cmd, shell=True)
        output = cmd_output.decode()

        average_complexity_re = re.search(r"Average complexity:.*\((?P<complexity>[\d\.]+)\)", output)
        average_complexity = average_complexity_re.group("complexity")

        return float(average_complexity)

    def get_project_parts_complexity(self, min_grade: str = "a") -> dict[str, ComplexityDict]:
        """
        Use to return information about items in our code like Classes, Function, Methods ...
        min_grade: parameter will only return information that are equal or worst to this.
        It can go from A to F.
        """
        cmd = f'radon cc {self.project_path} --json -n{min_grade.lower()} -e "**/venv/*"'
        cmd_output = subprocess.check_output(cmd, shell=True)

        json_output = cmd_output.decode()
        # remove some chars linked to the color and breaking the json
        clean_output = re.sub(r"\x1b\[[0-9;]*[a-zA-Z]", "", json_output)

        data = json.loads(clean_output)

        return data
