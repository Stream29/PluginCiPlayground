import os
import shutil
import subprocess
from pathlib import Path

import dotenv

dotenv.load_dotenv()

test_plugin_package_path = Path("test-anthropic-package.difypkg")
plugin_source_folder_path = Path("anthropic")
test_plugin_folder_path = Path("test-anthropic-package")

try:
    subprocess.run(
        args=["dify", "plugin", "package", "anthropic", "--output_path", "test-anthropic-package.difypkg"],
        check=True,
    )

    subprocess.run(
        args=["python", "script.py"],
        check=True,
        env={
            **os.environ,
            "PLUGIN_FILE_PATH": "test-anthropic-package.difypkg"
        }
    )
finally:
    test_plugin_package_path.unlink()
    shutil.rmtree(test_plugin_folder_path)
