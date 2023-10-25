import json
import pathlib
from dataclasses import dataclass
from typing import Any

from unella.modules.generic import Report
from unella.modules.mypy.main import MypyReport
from unella.modules.ruff.main import RuffReport
from unella.modules.structure.main import StructureReport
from unella.modules.vulture.main import VultureReport
from unella.utils import pascal_case_to_snake_case


@dataclass
class AuditGenerator:
    def __init__(self, project_to_audit: str) -> None:
        self.project_path = pathlib.Path(project_to_audit)

    @property
    def report_list(self) -> list[type[Report]]:
        return [
            RuffReport,
            MypyReport,
            StructureReport,
            VultureReport,
        ]

    def get_data(self) -> dict[str, Any]:
        results = {}
        for report_class in self.report_list:
            report = report_class(str(self.project_path))
            report.perform_analysis()
            report_name = pascal_case_to_snake_case(report_class.__name__)
            results[report_name] = report.get_results()

        return results

    def get_json(self) -> str:
        return json.dumps(self.get_data())
