from __future__ import annotations

from unella.modules.audit_generator import AuditGenerator

PROJECT_TO_AUDIT = "/home/tevak/dev/jwt_tool"


def main() -> None:
    audit_generator = AuditGenerator(project_to_audit=PROJECT_TO_AUDIT)
    data = audit_generator.get_data()
    print(data)


if __name__ == "__main__":
    main()
