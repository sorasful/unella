import json

from tests.conftest import ROOT_DIR
from unella.audit_generator import AuditGenerator


def test_get_json() -> None:
    audit_generator = AuditGenerator(project_to_audit=ROOT_DIR)
    report_json = audit_generator.get_json()

    loaded_data = json.loads(report_json)
    assert loaded_data is not None


def test_get_html() -> None:
    audit_generator = AuditGenerator(project_to_audit=ROOT_DIR)
    report_html = audit_generator.get_html()

    assert "<h1>Audit Report</h1>" in report_html
