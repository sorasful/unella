import pytest
from unella.utils import pascal_case_to_snake_case


@pytest.mark.parametrize(
    "text, expected", [("VultureReport", "vulture_report"), ("SomeOtherPackageX", "some_other_package_x")]
)
def test_pascal_case_to_snake_case(text: str, expected: str) -> None:
    assert pascal_case_to_snake_case(text) == expected
