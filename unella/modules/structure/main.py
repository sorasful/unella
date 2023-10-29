from __future__ import annotations

import json
import pathlib
import subprocess
import typing as t
import venv

from unella.modules.generic import Report


class StructureReportData(t.TypedDict, total=False):
    is_git_repository: bool
    git_repository_hash: str | None
    structure: list[dict]
    has_precommit_file: bool
    has_tests: bool
    uses_pytest: bool
    coverage: "CoverageData" | None
    dependencies: "DependenciesDict"


DependenciesDict = t.TypedDict(
    "DependenciesDict",
    {"requirements.txt": bool, "pipenv": bool, "poetry": bool, "setuptools": bool, "pip-tools": bool},
)


class CoverageSummary(t.TypedDict):
    covered_lines: int
    num_statements: int
    percent_covered: float
    percent_covered_display: str
    missing_lines: int
    excluded_lines: int


class FileCoverage(t.TypedDict):
    executed_lines: list[int]
    summary: CoverageSummary
    missing_lines: list[int]
    excluded_lines: list[int]


class CoverageMeta(t.TypedDict):
    version: str
    timestamp: str
    branch_coverage: bool
    show_contexts: bool


class CoverageTotals(t.TypedDict):
    covered_lines: int
    num_statements: int
    percent_covered: float
    percent_covered_display: str
    missing_lines: int
    excluded_lines: int


class CoverageData(t.TypedDict):
    meta: CoverageMeta
    files: dict[str, FileCoverage]
    totals: CoverageTotals


class StructureReport(Report):
    def __init__(self, project_to_audit: str | pathlib.Path) -> None:
        self._cmd_output = None
        self.project_path = pathlib.Path(project_to_audit)
        self._data: StructureReportData = {}

    def perform_analysis(self) -> None:
        self._data["is_git_repository"] = self.check_is_git_repository()
        if self._data["is_git_repository"]:
            self._data["git_repository_hash"] = self.get_git_repository_hash()
        else:
            self._data["git_repository_hash"] = None

        self._data["structure"] = self.get_tree_structure()
        self._data["has_precommit_file"] = self.check_precommit_file_exists()

        test_information = self.get_tests_information()
        self._data["has_tests"] = test_information["has_tests"]
        self._data["uses_pytest"] = test_information["uses_pytest"]
        self._data["coverage"] = test_information["coverage"]
        self._data["dependencies"] = self.get_dependencies()

    def check_is_git_repository(self) -> bool:
        git_path = self.project_path / ".git"
        return git_path.exists()

    def get_git_repository_hash(self) -> str:
        git_path = self.project_path / ".git"

        cmd = f"git --git-dir={git_path} rev-parse HEAD"
        cmd_output = subprocess.check_output(cmd, shell=True)
        output = cmd_output.decode()

        return output.strip()

    def get_tree_structure(self) -> list[dict]:
        gitignore_path = self.project_path / ".gitignore"
        cmd = f'tree -J -I "{get_tree_ignores(gitignore_path)}" {self.project_path}'
        cmd_output = subprocess.check_output(cmd, shell=True)
        output = cmd_output.decode()

        return json.loads(output)

    def get_python_version(self):
        raise NotImplementedError

    def get_dependencies(self) -> DependenciesDict:
        project = pathlib.Path(self.project_path)
        dependencies = {
            "requirements.txt": False,
            "pipenv": False,
            "poetry": False,
            "setuptools": False,
            "pip-tools": False,
        }

        if (project / "requirements.txt").exists():
            dependencies["requirements.txt"] = True

        if (project / "Pipfile").exists():
            dependencies["pipenv"] = True

        pyproject = project / "pyproject.toml"
        if pyproject.exists():
            with pyproject.open("r") as f:
                content = f.read()
                if "[tool.poetry]" in content:
                    dependencies["poetry"] = True

        if (project / "setup.py").exists():
            dependencies["setuptools"] = True

        in_files = [f for f in project.iterdir() if f.name.endswith(".in")]
        if in_files:
            dependencies["pip-tools"] = True

        return dependencies

    def get_coverage(self) -> dict | None:
        # if we run on this project we'll get an infinite loop
        if self.project_path.name == "unella":
            return None

        # we need to install project dependencies to be able to run the tests
        env_dir = pathlib.Path("test_venv")
        venv.create(env_dir, with_pip=True)

        def run_command(cmd):
            subprocess.run(
                cmd,
                shell=True,
                check=True,
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
            )

        # activate virtualenv and install test dependencies
        python_venv = env_dir / "bin" / "python"
        run_command(f"{python_venv.absolute()} -m pip install pytest pytest-cov coverage covdefaults")

        # install project dependencies
        run_command(f"{python_venv.absolute()} -m pip install {self.project_path}")

        # run the tests
        run_command(f"cd {self.project_path} && {python_venv.absolute()} -m pytest --cov={self.project_path} || true")

        # generate coverage.json file
        run_command(f"cd {self.project_path} && {python_venv.absolute()} -m coverage json")

        # disable and delete virtualenv
        subprocess.run(f"rm -rf {env_dir}", shell=True)

        coverage_file = self.project_path / "coverage.json"

        with open(coverage_file, "r") as f:
            data = json.load(f)

        coverage_file.unlink()

        return data

    def check_precommit_file_exists(self) -> bool:
        precommit_file_paths = [
            self.project_path / ".pre-commit-config.yaml",
            self.project_path / ".pre-commit-config.yml",
        ]
        return any(x.exists() for x in precommit_file_paths)

    def get_tests_information(self) -> dict:
        # check if there are test folders or files
        test_files = self.project_path.rglob("**/test_*.py")
        uses_pytest = False
        coverage = None
        if test_files:
            # check if uses pytest
            gitignore_path = self.project_path / ".gitignore"
            excludes = get_grep_excludes(gitignore_path)
            grep_command = " ".join(["grep", "-r", "pytest", str(self.project_path), *excludes])
            try:
                subprocess.check_output(grep_command, shell=True)
                uses_pytest = True
            except subprocess.CalledProcessError:
                uses_pytest = False

            # get the coverage
            if uses_pytest:
                coverage = self.get_coverage()

        return {
            "has_tests": bool(test_files),
            "uses_pytest": uses_pytest,
            "coverage": coverage,
        }

    def get_results(self) -> StructureReportData:
        if not self._data:
            self.perform_analysis()

        return self._data


def get_tree_ignores(gitignore_path: pathlib.Path) -> str:
    """Ignore some files + all the files contained in .gitignore when performing "tree" command."""
    ignores = ["venv", "__pycache__", "*.pyc"]

    if gitignore_path.exists():
        with gitignore_path.open("r") as f:
            lines = f.readlines()
            git_ignores = [line.strip() for line in lines if not line.startswith("#") and line.strip()]
            ignores.extend(git_ignores)

    return "|".join(ignores)


def get_grep_excludes(gitignore_path: pathlib.Path) -> list:
    ignores = ["venv", "__pycache__", "*.pyc"]

    if gitignore_path.exists():
        with gitignore_path.open("r") as f:
            lines = f.readlines()
            git_ignores = [line.strip() for line in lines if not line.startswith("#") and line.strip()]
            ignores.extend(git_ignores)

    grep_excludes = []
    for ignore in ignores:
        if ("*" in ignore or "?" in ignore) and not ignore.endswith("/"):
            grep_excludes.append(f"--exclude={ignore}")
        else:
            grep_excludes.append(f"--exclude-dir={ignore}")

    return grep_excludes
