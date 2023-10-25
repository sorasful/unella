import json
import pathlib
import re
import subprocess
from dataclasses import dataclass

from unella.modules.generic import Report


VULTURE_LINE_REGEX = (
    r"(?P<file_path>.*):(?P<line>\d+): (?P<msg>.*)\((?P<confidence>\d+).*\)"
)


def get_tree_ignores(gitignore_path: pathlib.Path) -> str:
    ignores = ["venv", "__pycache__", "*.pyc"]

    if gitignore_path.exists():
        with gitignore_path.open("r") as f:
            lines = f.readlines()
            git_ignores = [
                line.strip()
                for line in lines
                if not line.startswith("#") and line.strip()
            ]
            ignores.extend(git_ignores)

    return "|".join(ignores)


@dataclass
class VultureReport(Report):
    _cmd_output: str | None = None
    _data: list[dict] | None = None

    def perform_analysis(self) -> None:
        # TODO: exclude everything from the gitignore
        gitignore_path = self.project_path / ".gitignore"
        cmd = f"vulture {self.project_path} --exclude 'venv'"
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
        return self._data

    def render_json(self) -> str:
        return json.dumps(self._data)

    def render_html(self) -> str:
        return ""
