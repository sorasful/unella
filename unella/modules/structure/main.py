import json
import pathlib
import subprocess
import typing as t

from unella.modules.generic import Report


class StructureReportData(t.TypedDict, total=False):
    is_git_repository: bool
    git_repository_hash: str | None
    structure: list[dict]
    has_precommit_file: bool
    has_tests: bool
    uses_pytest: bool
    dependencies: dict


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

    def get_dependencies(self) -> dict:
        project = pathlib.Path(self.project_path)
        dependencies = {
            "requirements.txt": False,
            "pipenv": False,
            "poetry": False,
            "setuptools": False,
            "pip-tools": False,
        }

        # Vérifier requirements.txt
        if (project / "requirements.txt").exists():
            dependencies["requirements.txt"] = True

        # Vérifier Pipfile
        if (project / "Pipfile").exists():
            dependencies["pipenv"] = True

        # Vérifier pyproject.toml pour poetry
        pyproject = project / "pyproject.toml"
        if pyproject.exists():
            with pyproject.open("r") as f:
                content = f.read()
                if "[tool.poetry]" in content:
                    dependencies["poetry"] = True

        # Vérifier setup.py
        if (project / "setup.py").exists():
            dependencies["setuptools"] = True

        # Vérifier pip-tools
        in_files = [f for f in project.iterdir() if f.name.endswith(".in")]
        if in_files:
            dependencies["pip-tools"] = True

        return dependencies

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

        return {
            "has_tests": bool(test_files),
            "uses_pytest": uses_pytest,
        }

    def get_results(self) -> StructureReportData:
        if self._data is None:
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
