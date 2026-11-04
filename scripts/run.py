import os
import sys

import setup_world
import subprocess

from time import sleep

world_info = setup_world.setup_world()

print(f"World info: {world_info}")
stub = world_info.stub

ruff_base =["ruff", "check",
            "--output-format", "json",

            "--config", "/scripts/ruff.toml",
            f"/Archipelago/worlds/{stub}"]

ruff_cmd = ruff_base + [
            "--output-file", "/out/ruff_output.json"]

subprocess.run(ruff_cmd)

ruff_cmd = ruff_base + ["--statistics",
             "--output-file", "/out/ruff_stats.json"]

subprocess.run(ruff_cmd)

pytest_cmd = [sys.executable, "-m", "pytest",
              "-k", "not test_no_container_version",
              "--junitxml=/out/report.xml"]
pytest_env = {"AP_TEST_WORLDS": stub}

subprocess.run(pytest_cmd, env=pytest_env)

if os.environ.get("KEEP_RUNNING"):
    while True:
        sleep(1)
