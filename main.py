from __future__ import annotations

from unella.modules.audit_generator import AuditGenerator

PROJECT_TO_AUDIT = "/home/tevak/dev/jwt_tool"


def main() -> None:
    audit_generator = AuditGenerator(project_to_audit=PROJECT_TO_AUDIT)
    for report_class in audit_generator.report_list:
        print(report_class.__name__)
        report = report_class(PROJECT_TO_AUDIT)
        report.perform_analysis()
        print(report.render_json())


if __name__ == "__main__":
    main()
