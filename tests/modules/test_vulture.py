from tests.conftest import ROOT_DIR
from unella.modules.vulture.main import VultureReport


def test_vulture_report():
    report = VultureReport(ROOT_DIR)
    report.perform_analysis()
    first_entry, *entries = report.get_results()

    assert isinstance(first_entry["confidence"], str)
    assert isinstance(first_entry["file_path"], str)
    assert isinstance(first_entry["line"], str)
    assert isinstance(first_entry["msg"], str)
