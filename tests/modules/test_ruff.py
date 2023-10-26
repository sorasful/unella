from tests.conftest import ROOT_DIR
from unella.modules.ruff.main import RuffReport


def test_ruff_report():
    report = RuffReport(ROOT_DIR)
    report.perform_analysis()
    first_entry, *entries = report.get_results()

    assert isinstance(first_entry["code"], str)
    assert isinstance(first_entry["count"], int)
    assert isinstance(first_entry["fixable"], bool)
    assert isinstance(first_entry["message"], str)
