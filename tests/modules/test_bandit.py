from tests.conftest import ROOT_DIR
from unella.modules.bandit.main import BanditReport


def test_bandit_report() -> None:
    report = BanditReport(ROOT_DIR)
    report.perform_analysis()
    results = report.get_results()

    first_vulnerability, *vulnerabilities = results["vulnerabilities"]["results"]

    assert isinstance(first_vulnerability.get("code"), str)
    assert isinstance(first_vulnerability.get("col_offset"), int)
    assert isinstance(first_vulnerability.get("end_col_offset"), int)
    assert isinstance(first_vulnerability.get("filename"), str)
    assert isinstance(first_vulnerability.get("issue_confidence"), str)
    assert isinstance(first_vulnerability.get("issue_cwe"), dict)
    assert isinstance(first_vulnerability["issue_cwe"].get("id"), int)
    assert isinstance(first_vulnerability["issue_cwe"].get("link"), str)
    assert isinstance(first_vulnerability.get("issue_severity"), str)
    assert isinstance(first_vulnerability.get("issue_text"), str)
    assert isinstance(first_vulnerability.get("line_number"), int)
    assert isinstance(first_vulnerability.get("line_range"), list)
    assert all(isinstance(item, int) for item in first_vulnerability.get("line_range"))
    assert isinstance(first_vulnerability.get("more_info"), str)
    assert isinstance(first_vulnerability.get("test_id"), str)
    assert isinstance(first_vulnerability.get("test_name"), str)
