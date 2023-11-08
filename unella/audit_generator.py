import datetime
import json
import pathlib
from dataclasses import dataclass
from typing import Any

from jinja2 import Environment, FileSystemLoader
from loguru import logger
from markdownify import markdownify as md

from unella.cli import ProgressBar
from unella.modules.bandit.main import BanditReport
from unella.modules.generic import Report
from unella.modules.gitleaks.main import GitleaksReport
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
            BanditReport,
            GitleaksReport,
        ]

    @property
    def available_report_list(self) -> list[type[Report]]:
        for report_class in [
            StructureReport,
            RuffReport,
            MypyReport,
            VultureReport,
            RadonReport,
            BanditReport,
            GitleaksReport,
        ]:
            if report_class(str(self.project_path)).is_available:
                yield report_class
            else:
                logger.warning(f"{report_class.__name__} is not available, skipping this one.")
                continue

    def get_data(self) -> dict[str, Any]:
        results = {}
        for report_class in self.available_report_list:
            report = report_class(str(self.project_path))
            try:
                report.perform_analysis()
            except Exception as e:
                logger.exception(f"Got an exception on module {report_name}, skipping this one")
                continue
            report_name = pascal_case_to_snake_case(report_class.__name__)
            results[report_name] = report.get_results()

        return results

    def get_json(self) -> str:
        return json.dumps(self.get_data())

    def get_html(self) -> str:
        env = Environment(loader=FileSystemLoader("templates"))
        template = env.get_template("main_template.html")

        reports_html = {}
        available_report_list = list(self.available_report_list)
        progress_bar = ProgressBar(len(available_report_list))
        for step, report_class in zip(progress_bar.start(), available_report_list):
            report_name = pascal_case_to_snake_case(report_class.__name__)
            try:
                reports_html[report_name] = report_class(str(self.project_path)).to_html()
            except Exception as e:
                logger.exception(f"Got an exception on module {report_name}, skipping this one")
                continue
        now = datetime.datetime.now()
        formatted_now = now.strftime("%B %d, %Y %H:%M:%S")
        project_name = self.project_path.name

        return template.render(reports=reports_html, audit_date=formatted_now, project_name=project_name)

    def get_markdown(self) -> str:
        html = self.get_html()
        return md(html)
