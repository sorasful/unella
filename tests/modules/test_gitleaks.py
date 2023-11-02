from unittest.mock import Mock, patch

from tests.conftest import ROOT_DIR
from unella.modules.gitleaks.main import GitleaksReport

POTENTIAL_LEAK_JSON_OUTPUT = """
[
 {
  "Description": "Generic API Key",
  "StartLine": 8,
  "EndLine": 8,
  "StartColumn": 9,
  "EndColumn": 56,
  "Match": "key : SOMESECRET ",
  "Secret": "SOMESECRET",
  "File": "some/random/file/data.json",
  "SymlinkFile": "",
  "Commit": "2940aca397aadb67c26c5daca583079d0a7f6ea3",
  "Entropy": 3.5582948,
  "Author": "Sorasful",
  "Email": "myemail@example.com",
  "Date": "2023-07-23T11:54:49Z",
  "Message": "Some commit message",
  "Tags": [],
  "RuleID": "generic-api-key",
  "Fingerprint": "2940aca397c26c5daca58307990a7f6ea3:some/random/file/data.json:generic-api-key:8"
 }]"""


@patch("unella.modules.gitleaks.main.subprocess.run")
def test_gitleaks_report(gitleaks_potential_leaks_mock) -> None:
    def mock_subprocess_run(*args, **kwargs):
        with open("gitleaks_results.json", "w") as f:
            f.write(POTENTIAL_LEAK_JSON_OUTPUT)
        return Mock(returncode=0)

    gitleaks_potential_leaks_mock.side_effect = mock_subprocess_run

    report = GitleaksReport(ROOT_DIR)
    report.perform_analysis()
    results = report.get_results()

    assert len(results["leaks"]) == 1
