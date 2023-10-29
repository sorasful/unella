import datetime
import json
import pathlib
from dataclasses import dataclass
from typing import Any

from jinja2 import Environment, FileSystemLoader
from markdownify import markdownify as md

from unella.cli import ProgressBar
from unella.modules.generic import Report
from unella.modules.mypy.main import MypyReport
from unella.modules.radon.main import RadonReport
from unella.modules.ruff.main import RuffReport
from unella.modules.structure.main import StructureReport
from unella.modules.vulture.main import VultureReport
from unella.utils import pascal_case_to_snake_case


@dataclass
class AuditGenerator:
    def __init__(self, project_to_audit: str | pathlib.Path) -> None:
        self.project_path = pathlib.Path(project_to_audit)

    @property
    def report_list(self) -> list[type[Report]]:
        return [
            StructureReport,
            RuffReport,
            MypyReport,
            VultureReport,
            RadonReport,
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

    def get_html(self) -> str:
        env = Environment(loader=FileSystemLoader("templates"))
        template = env.get_template("main_template.html")

        reports_html = {}
        progress_bar = ProgressBar(len(self.report_list))
        for step, report_class in zip(progress_bar.start(), self.report_list):
            report_name = pascal_case_to_snake_case(report_class.__name__)
            reports_html[report_name] = report_class(str(self.project_path)).to_html()

        now = datetime.datetime.now()
        formatted_now = now.strftime("%B %d, %Y %H:%M:%S")
        project_name = self.project_path.name

        return template.render(reports=reports_html, audit_date=formatted_now, project_name=project_name)

    def get_markdown(self) -> str:
        html = self.get_html()
        return md(html)
