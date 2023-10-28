from tests.conftest import ROOT_DIR
from unella.modules.radon.main import RadonReport


def test_radon_report() -> None:
    report = RadonReport(ROOT_DIR)
    report.perform_analysis()
    results = report.get_results()

    assert results["average_complexity"] > 0
    assert len(results["complexity"]) > 1

    first_file, file_complexities = next(iter(results["complexity"].items()))

    first_complexity = file_complexities[0]
    assert first_complexity["col_offset"] >= 0
    assert first_complexity["complexity"] >= 0
    assert first_complexity["endline"] >= 0
    assert first_complexity["lineno"] >= 0
    assert first_complexity["rank"] in {"A", "B", "C", "D", "E", "F"}
    assert first_complexity["type"] in {"function", "class", "method"}
    assert first_complexity["name"] is not None
