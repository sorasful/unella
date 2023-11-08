from tests.conftest import ROOT_DIR
from unella.modules.bandit.main import BanditReport


def test_bandit_report() -> None:
    report = BanditReport(ROOT_DIR)
    report.perform_analysis()
    results = report.get_results()

    first_vulnerability, *vulnerabilities = results["vulnerabilities"]["results"]

    assert first_vulnerability == {
        "code": '7 \n8 response = requests.get("https://pro.pinock.io/features")\n9 \n',
        "col_offset": 11,
        "end_col_offset": 57,
        "filename": "/home/tevak/dev/unella/pan.py",
        "issue_confidence": "LOW",
        "issue_cwe": {"id": 400, "link": "https://cwe.mitre.org/data/definitions/400.html"},
        "issue_severity": "MEDIUM",
        "issue_text": "Requests call without timeout",
        "line_number": 8,
        "line_range": [8],
        "more_info": "https://bandit.readthedocs.io/en/1.7.5/plugins/b113_request_without_timeout.html",
        "test_id": "B113",
        "test_name": "request_without_timeout",
    }
