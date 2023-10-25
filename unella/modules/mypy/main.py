import json
import pathlib
import re
import subprocess
from collections import Counter
from dataclasses import dataclass

from loguru import logger

from unella.modules.generic import Report

MYPY_LINE_REGEX = r"(?P<file_path>.*):\d+: (?P<msg_type>error|warning):(?P<msg>.*)\[(?P<msg_category>[\w_-]+)\]"


@dataclass
class MypyReport(Report):
    _cmd_output: str | None = None
    _data: str | None = None
    _most_messages_categories: list | None = None
    _most_messages: list | None = None
    _file_most_messages: list | None = None

    def perform_analysis(self) -> None:
        cmd = f"mypy {self.project_path} --strict"
        try:
            cmd_output = subprocess.check_output(cmd, shell=True)
        except subprocess.CalledProcessError as e:
            # mypy does not provide an option to return 0 status code
            cmd_output = e.output

        output = cmd_output.decode()
        matches = re.finditer(MYPY_LINE_REGEX, string=output)

        file_counter: Counter = Counter()
        msg_counter: Counter = Counter()
        msg_category_counter: Counter = Counter()

        for match in matches:
            file_path = match.group("file_path")
            msg = match.group("msg")
            msg_category = match.group("msg_category")

            file_counter[file_path] += 1
            msg_counter[msg] += 1
            msg_category_counter[msg_category] += 1

        self._file_most_messages = file_counter.most_common()
        self._most_messages = msg_counter.most_common()
        self._most_messages_categories = msg_category_counter.most_common()

        self._cmd_output = output

    def get_results(self) -> dict:
        return {
            "files_most_messages": self._file_most_messages,
            "most_messages": self._most_messages,
            "most_messages_categories": self._most_messages_categories,
        }
