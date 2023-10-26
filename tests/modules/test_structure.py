from tests.conftest import ROOT_DIR
from unella.modules.structure.main import StructureReport


def test_structure_report() -> None:
    report = StructureReport(ROOT_DIR)
    report.perform_analysis()
    results = report.get_results()

    assert results["has_tests"] is True
    assert results["uses_pytest"] is True
    assert results["is_git_repository"] is True
    assert results["has_precommit_file"] is False
    assert results["structure"] is not None
    dependencies = results["dependencies"]
    assert dependencies["requirements.txt"] is True
    assert dependencies["pipenv"] is False
    assert dependencies["poetry"] is False
    assert dependencies["pip-tools"] is True
    assert dependencies["setuptools"] is False
