import os
import shutil
import subprocess
import sys
from pathlib import Path

def run_test(plugin_name: str):
    print(f"Starting E2E test for plugin: {plugin_name}")
    
    # Define paths
    test_plugin_package_path = Path(f"test-{plugin_name}-package.difypkg")
    test_plugin_folder_path = Path(f"test-{plugin_name}-package")
    
    # Ensure clean state
    if test_plugin_package_path.exists():
        test_plugin_package_path.unlink()
    if test_plugin_folder_path.exists():
        if test_plugin_folder_path.is_dir():
            shutil.rmtree(test_plugin_folder_path)
        else:
            test_plugin_folder_path.unlink()

    try:
        # 1. Package the plugin
        print(f"Packaging plugin '{plugin_name}'...")
        subprocess.run(
            args=["dify", "plugin", "package", plugin_name, "--output_path", str(test_plugin_package_path)],
            check=True,
        )

        # 2. Run script.py (which handles extraction, venv initialization, and pytest)
        print(f"Executing test script for {test_plugin_package_path}...")
        subprocess.run(
            args=["python", "script.py"],
            check=True,
            env={
                **os.environ,
                "PLUGIN_FILE_PATH": str(test_plugin_package_path)
            }
        )
        print(f"Successfully completed tests for {plugin_name}")
        
    except subprocess.CalledProcessError as e:
        print(f"Test failed for plugin {plugin_name} with exit code {e.returncode}")
        sys.exit(e.returncode)
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        sys.exit(1)
    finally:
        # Cleanup
        if test_plugin_package_path.exists():
            test_plugin_package_path.unlink()
        if test_plugin_folder_path.exists():
            shutil.rmtree(test_plugin_folder_path, ignore_errors=True)

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python test_runner.py <plugin_name>")
        sys.exit(1)
    
    plugin_name_arg = sys.argv[1]
    run_test(plugin_name_arg)
