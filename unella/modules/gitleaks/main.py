import json
import pathlib
import re
import subprocess
import typing as t
from dataclasses import dataclass

from unella.modules.generic import Report


class GitleakEntry(t.TypedDict):
    description: str
    start_line: int
    end_line: int
    start_column: int
    end_column: int
    match: str
    secret: str
    file: str
    symlink_file: str
    commit: str
    entropy: float
    author: str
    email: str
    date: str
    message: str
    tags: list[str]
    rule_id: str
    fingerprint: str


class GitleaksReportData(t.TypedDict):
    leaks: list[GitleakEntry]


def to_snake_case(string: str) -> str:
    s1 = re.sub("(.)([A-Z][a-z]+)", r"\1_\2", string)
    return re.sub("([a-z0-9])([A-Z])", r"\1_\2", s1).lower()


def convert_keys_to_snake_case(data: dict) -> dict:
    return {
        to_snake_case(key): (convert_keys_to_snake_case(value) if isinstance(value, dict) else value)
        for key, value in data.items()
    }


@dataclass
class GitleaksReport(Report):
    _data: GitleaksReportData | None = None

    def perform_analysis(self) -> None:
        self._data = {}
        self._data["leaks"] = self.get_potential_leaks()

    def get_results(self) -> GitleaksReportData:
        if self._data is None:
            self.perform_analysis()
        return self._data

    def get_potential_leaks(self) -> list[GitleakEntry]:
        """
        Used to return a list of potential leaks in the project.
        """
        gitleaks_result_file = pathlib.Path("gitleaks_results.json")
        cmd = f"gitleaks detect -s {self.project_path} -f json  --exit-code 0 -r {gitleaks_result_file}"
        subprocess.run(cmd, shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

        with open(gitleaks_result_file, "r") as f:
            gitleaks_data = json.load(f)
            gitleaks_data = [convert_keys_to_snake_case(x) for x in gitleaks_data]

        gitleaks_result_file.unlink(missing_ok=True)

        return gitleaks_data
