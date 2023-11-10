import datetime
import json
import pathlib
from concurrent.futures import ThreadPoolExecutor
from dataclasses import dataclass
from typing import Any

from jinja2 import Environment, FileSystemLoader
from loguru import logger
from rich.progress import Progress, SpinnerColumn, TextColumn

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

    def get_report(self, format: str = "html") -> str:
        env = Environment(loader=FileSystemLoader("html_templates" if format == "html" else "markdown_templates"))
        template = env.get_template("main_template.html" if format == "html" else "main_template.md")

        reports = {}

        def generate_report(task_id, report_class: type[Report], format: str) -> None:
            report_name = pascal_case_to_snake_case(report_class.__name__)
            try:
                report = report_class(str(self.project_path))
                if not report.is_available:
                    progress.update(task_id, completed=100, status="[yellow]Unavailable[/yellow]")
                else:
                    report_content = report.to_html() if format == "html" else report.to_markdown()
                    reports[report_name] = report_content
                    progress.update(task_id, completed=100, status="[green]Finished[/green]")
            except Exception as e:
                logger.exception(f"Got an exception on module {report_name}, skipping this one")
                progress.update(task_id, completed=100, status="[red]Error[/red]")

        with Progress(
            "[progress.description]{task.description}",
            SpinnerColumn(),
            TextColumn("[progress.remaining]{task.fields[status]}"),
        ) as progress, ThreadPoolExecutor() as executor:
            futures = []
            for report_class in self.report_list:
                report_name = pascal_case_to_snake_case(report_class.__name__)
                task_id = progress.add_task(f"Generating {report_name}...", status="In progress...", total=100)
                futures.append(executor.submit(generate_report, task_id, report_class, format))

            # wait for everything to finish
            for future in futures:
                future.result()

        now = datetime.datetime.now()
        formatted_now = now.strftime("%B %d, %Y %H:%M:%S")
        project_name = self.project_path.name

        return template.render(reports=reports, audit_date=formatted_now, project_name=project_name)

    def get_html(self) -> str:
        return self.get_report(format="html")

    def get_markdown(self) -> str:
        return self.get_report(format="markdown")
