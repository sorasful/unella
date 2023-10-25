import pathlib
from dataclasses import dataclass
from typing import Any

from unella.modules.generic import Report
from unella.modules.mypy.main import MypyReport
from unella.modules.ruff.main import RuffReport
from unella.modules.structure.main import StructureReport
from unella.modules.vulture.main import VultureReport


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
            report = report_class(self.project_path)
            report.perform_analysis()
            results[report_class.__name__] = report.get_results()

        return results
