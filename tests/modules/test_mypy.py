from tests.conftest import ROOT_DIR
from unella.modules.mypy.main import MypyReport


def test_mypy_report():
    report = MypyReport(ROOT_DIR)
    report.perform_analysis()
    results = report.get_results()

    assert len(results["most_messages"]) >= 1
    assert len(results["most_messages_categories"]) >= 1
    assert len(results["files_most_messages"]) >= 1

    # check the format of the first message for each
    for result in [results["most_messages"], results["most_messages_categories"], results["files_most_messages"]]:
        msg, occurence = result[0]
        assert isinstance(msg, str)
        assert isinstance(occurence, int)
