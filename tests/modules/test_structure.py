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
        },
    }
    report = StructureReport(ROOT_DIR)
    report.perform_analysis()
    results = report.get_results()

    assert results["has_tests"] is True
    assert results["uses_pytest"] is True
    assert results["coverage"]["totals"]["percent_covered_display"] == 98
    assert results["is_git_repository"] is True
    assert results["has_precommit_file"] is True
    assert results["precommit_config"] == {
        "repos": [
            {
                "repo": "https://github.com/pre-commit/pre-commit-hooks",
                "rev": "v2.4.0",
                "hooks": [
                    {"id": "check-ast"},
                    {"id": "trailing-whitespace"},
                    {"id": "check-toml"},
                    {"id": "end-of-file-fixer"},
                ],
            },
            {
                "repo": "https://github.com/pycqa/isort",
                "rev": "5.12.0",
                "hooks": [{"id": "isort", "name": "isort (python)"}],
            },
            {
                "repo": "https://github.com/asottile/add-trailing-comma",
                "rev": "v2.1.0",
                "hooks": [{"id": "add-trailing-comma"}],
            },
            {
                "repo": "https://github.com/macisamuele/language-formatters-pre-commit-hooks",
                "rev": "v2.1.0",
                "hooks": [{"id": "pretty-format-yaml", "args": ["--autofix", "--preserve-quotes", "--indent=2"]}],
            },
            {
                "repo": "https://github.com/psf/black-pre-commit-mirror",
                "rev": "23.10.1",
                "hooks": [{"id": "black", "language_version": "python3.10"}],
            },
        ],
    }
    assert results["structure"] is not None
    dependencies = results["dependencies"]
    assert dependencies["requirements.txt"] is False
    assert dependencies["pipenv"] is False
    assert dependencies["poetry"] is False
    assert dependencies["pip-tools"] is False
    assert dependencies["setuptools"] is True
