from unittest.mock import patch

from tests.conftest import ROOT_DIR
from unella.modules.structure.main import StructureReport


@patch("unella.modules.structure.main.StructureReport.get_coverage")
def test_structure_report(get_coverage_mock) -> None:
    get_coverage_mock.return_value = {
        "totals": {
            "covered_lines": 311,
            "num_statements": 318,
            "percent_covered": 97.79874213836477,
            "percent_covered_display": 98,
            "missing_lines": 7,
            "excluded_lines": 3,
        }
    }
    report = StructureReport(ROOT_DIR)
    report.perform_analysis()
    results = report.get_results()

    assert results["has_tests"] is True
    assert results["uses_pytest"] is True
    assert results["coverage"]["totals"]["percent_covered_display"] == 98
    assert results["is_git_repository"] is True
    assert results["has_precommit_file"] is False
    assert results["structure"] is not None
    dependencies = results["dependencies"]
    assert dependencies["requirements.txt"] is False
    assert dependencies["pipenv"] is False
    assert dependencies["poetry"] is False
    assert dependencies["pip-tools"] is False
    assert dependencies["setuptools"] is True
