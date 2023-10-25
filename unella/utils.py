import re


def pascal_case_to_snake_case(text: str) -> str:
    s = re.sub("(?<=[a-z])(?=[A-Z])", "_", text)
    return s.lower()
