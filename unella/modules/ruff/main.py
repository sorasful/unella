import json
import subprocess
from dataclasses import dataclass

from unella.modules.generic import Report


@dataclass
class RuffReport(Report):
    _data: list[dict] | None = None
    _cmd_output: str | None = None

    def perform_analysis(self) -> None:
        cmd = f"ruff check {self.project_path} --select ALL --exit-zero --statistics --output-format json --silent"
        cmd_output = subprocess.check_output(cmd, shell=True)
        json_output = cmd_output.decode()

        data = json.loads(json_output)
        self._data = data
        self._cmd_output = json_output

    def get_results(self) -> list[dict]:
        if self._data is None:
            self.perform_analysis()
        return self._data
