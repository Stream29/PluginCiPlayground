import os
import shutil
import subprocess
from pathlib import Path
from typing import Final

plugin_file_path: Final[str | None] = os.getenv("PLUGIN_FILE_PATH")
if not plugin_file_path:
    raise Exception("PLUGIN_FILE_PATH is not set")
if not plugin_file_path.endswith(".difypkg"):
    raise Exception("PLUGIN_FILE_PATH must end with .difypkg")

plugin_folder_path: Final[Path] = Path(plugin_file_path.removesuffix(".difypkg"))
if plugin_folder_path.exists():
    if plugin_folder_path.is_dir():
        shutil.rmtree(plugin_folder_path)
    else:
        plugin_folder_path.unlink()

try:
    print(f"Processing plugin: {plugin_file_path}")
    shutil.unpack_archive(
        filename=plugin_file_path,
        extract_dir=plugin_folder_path,
        format="zip",
    )
    print(f"Plugin {plugin_file_path} unzipped to {plugin_folder_path}")

    tests_folder_path: Final[Path] = plugin_folder_path / "tests"
    has_tests: Final[bool] = tests_folder_path.exists() and tests_folder_path.is_dir()
    if not has_tests:
        raise Exception("No tests found in plugin")


    def init_venv() -> None:
        pyproject_path: Final[Path] = plugin_folder_path / "pyproject.toml"
        if pyproject_path.exists():
            subprocess.run(
                args=["uv", "sync", "--all-groups", "--python", "3.12"],
                cwd=plugin_folder_path,
                check=True,
            )
            print("Virtual environment initialized successfully with `pyproject.toml`")
            return None
        requirement_path: Final[Path] = plugin_folder_path / "requirements.txt"
        if requirement_path.exists():
            subprocess.run(
                args=["uv", "venv", "--python", "3.12"],
                cwd=plugin_folder_path,
                check=True,
            )
            subprocess.run(
                args=["uv", "install", "-r", "requirements.txt"],
                cwd=plugin_folder_path,
                check=True,
            )
            print("Virtual environment initialized successfully with `requirements.txt`")
            return None
        raise Exception("Cannot find `pyproject.toml` or `requirements.txt` in plugin folder")


    init_venv()

    print("Dependencies installed successfully. Running tests...")

    subprocess.run(
        args=["uv", "run", "--with", "pytest", "pytest"],
        cwd=plugin_folder_path,
        check=True,
        env={
            **os.environ,
            "PLUGIN_FILE_PATH": str(Path(plugin_file_path).resolve()),
        }
    )

    print("Tests passed successfully")
finally:
    shutil.rmtree(plugin_folder_path)
