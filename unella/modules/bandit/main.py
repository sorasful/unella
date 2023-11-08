import json
import shutil
import subprocess
import typing as t
from dataclasses import dataclass

from unella.modules.generic import Report


class BanditReportData(t.TypedDict):
    vulnerabilities: "VulnerabilitiesReport"


class VulnerabilitiesReport(t.TypedDict):
    errors: list
    generated_at: str
    metrics: dict[str, "MetricDetail"]
    results: list["ResultDetail"]


class CWEDetail(t.TypedDict):
    id: int
    link: str


class ResultDetail(t.TypedDict):
    code: str
    col_offset: int
    end_col_offset: int
    filename: str
    issue_confidence: str
    issue_cwe: CWEDetail
    issue_severity: str
    issue_text: str
    line_number: int
    line_range: list[int]
    more_info: str
    test_id: str
    test_name: str


class MetricDetail(t.TypedDict):
    CONFIDENCE_HIGH: int
    CONFIDENCE_LOW: int
    CONFIDENCE_MEDIUM: int
    CONFIDENCE_UNDEFINED: int
    SEVERITY_HIGH: int
    SEVERITY_LOW: int
    SEVERITY_MEDIUM: int
    SEVERITY_UNDEFINED: int
    loc: int
    nosec: int
    skipped_tests: int


@dataclass
class BanditReport(Report):
    _data: BanditReportData | None = None

    @property
    def is_available(self) -> bool:
        return bool(shutil.which("bandit"))

    def perform_analysis(self) -> None:
        self._data = {}
        self._data["vulnerabilities"] = self.get_project_vulnerabilities()

    def get_results(self) -> BanditReportData:
        if self._data is None:
            self.perform_analysis()
        return self._data

    def get_project_vulnerabilities(self) -> VulnerabilitiesReport:
        """
        Used to retrieve information about vulnerabilities
        """
        cmd = f"bandit -r {self.project_path} -x {self.project_path / 'venv' } -f json --exit-zero --quiet"
        cmd_output = subprocess.check_output(cmd, shell=True, stderr=subprocess.DEVNULL)

        json_output = cmd_output.decode()

        data = json.loads(json_output)

        return data


if __name__ == "__main__":
    r = BanditReport("/home/tevak/dev/unella")
    r.perform_analysis()
