import re
import subprocess
from dataclasses import dataclass

from unella.modules.generic import Report

VULTURE_LINE_REGEX = r"(?P<file_path>.*):(?P<line>\d+): (?P<msg>.*)\((?P<confidence>\d+).*\)"


@dataclass
class VultureReport(Report):
    _cmd_output: str | None = None
    _data: list[dict] | None = None

    def perform_analysis(self) -> None:
        cmd = f"vulture {self.project_path} --exclude venv "
        try:
            cmd_output = subprocess.check_output(cmd, shell=True)
        except subprocess.CalledProcessError as e:
            # mypy does not provide an option to return 0 status code
            cmd_output = e.output

        output = cmd_output.decode()

        results = []
        for match in re.finditer(VULTURE_LINE_REGEX, output):
            file_path = match.group("file_path")
            line = match.group("line")
            msg = match.group("msg")
            confidence = match.group("confidence")

            results.append(
                {
                    "file_path": file_path,
                    "line": line,
                    "msg": msg,
                    "confidence": confidence,
                }
            )

        self._data = results
        self._cmd_output = output

    def get_results(self) -> list[dict]:
        if self._data is None:
            self.perform_analysis()
        return self._data
