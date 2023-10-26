from __future__ import annotations

from loguru import logger

from unella.audit_generator import AuditGenerator

PROJECT_TO_AUDIT = "/home/tevak/dev/jwt_tool"


def main() -> None:
    audit_generator = AuditGenerator(project_to_audit=PROJECT_TO_AUDIT)
    report_html = audit_generator.get_html()

    with open("report.html", "w") as f:
        f.write(report_html)


if __name__ == "__main__":
    main()
