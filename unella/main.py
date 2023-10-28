from __future__ import annotations

import argparse
import datetime
import pathlib
import sys

from loguru import logger

from unella.audit_generator import AuditGenerator


def main() -> None:
    parser = argparse.ArgumentParser(description="Generate an audit report")
    parser.add_argument("--path", help="Path of the folder you want to audit.")
    parser.add_argument(
        "--output-format", choices=["html", "json"], default="html", help="Output format (html or json)."
    )

    args = parser.parse_args()
    project_path_input = args.path
    output_format = args.output_format

    project_path = pathlib.Path(project_path_input)
    if not project_path.exists():
        logger.error("The path specified does not exists")
        sys.exit(1)

    if not project_path.is_dir():
        logger.error("The path specified is not a directory")
        sys.exit(1)

    audit_generator = AuditGenerator(project_to_audit=project_path)

    if output_format == "json":
        report_json = audit_generator.get_json()
        print(report_json)
    elif output_format == "html":
        report_html = audit_generator.get_html()

        now = datetime.datetime.now()
        formatted_now = now.strftime("%Y-%m-%d_%H-%M")
        report_dir_path = pathlib.Path(f"report_{formatted_now}")
        report_dir_path.mkdir(parents=True, exist_ok=True)
        report_file_path = report_dir_path / "index.html"

        with open(report_file_path, "w") as f:
            f.write(report_html)

        logger.info(f"Report written in {report_file_path.absolute()}")


if __name__ == "__main__":
    main()
