"""
Thoughts:
- smoke test: ensure `program.py` runs with the example config
- create services.json from example to avoid modifying repo permanently
- run as subprocess to keep test isolated from test runner state
- assert on exit code only (fast, avoids brittle stdout checks)
- cleanup after test to leave workspace unchanged
"""

import os
import shutil
import subprocess


def test_program_runs_with_example_services(tmp_path):
    root = os.getcwd()
    src = os.path.join(root, "services.json.example")
    dst = os.path.join(root, "services.json")
    shutil.copy(src, dst)
    try:
        python_path = os.path.join(root, ".venv", "bin", "python")
        env = os.environ.copy()
        env["PYTHONPATH"] = root
        res = subprocess.run([python_path, "program.py"], env=env, capture_output=True, text=True)
        assert res.returncode == 0, f"program failed: stdout={res.stdout} stderr={res.stderr}"
    finally:
        if os.path.exists(dst):
            os.remove(dst)
