import os
import shutil
import subprocess
from pathlib import Path

import dotenv

dotenv.load_dotenv()

test_plugin_package_path = Path("test-anthropic-package.difypkg")
plugin_source_folder_path = Path("anthropic")

try:
    subprocess.run(
        args=[
            "dify",
            "plugin",
            "package",
            "anthropic",
            "--output_path",
            test_plugin_package_path.as_posix()
        ],
        check=True,
    )

    subprocess.run(
        args=["python", "script.py"],
        check=True,
        env={
            **os.environ,
            "PLUGIN_FILE_PATH": test_plugin_package_path.as_posix(),
        }
    )
finally:
    test_plugin_package_path.unlink()
