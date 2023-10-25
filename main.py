from __future__ import annotations

from loguru import logger

from unella.modules.audit_generator import AuditGenerator

PROJECT_TO_AUDIT = "/home/tevak/dev/jwt_tool"


def main() -> None:
    audit_generator = AuditGenerator(project_to_audit=PROJECT_TO_AUDIT)
    logger.info(f"{audit_generator.get_json()}")


if __name__ == "__main__":
    main()
