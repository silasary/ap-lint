import os
import shutil
import sys

import setup_world
import subprocess
import requests

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

subprocess.run(pytest_cmd, env=pytest_env, check=False)

get_fuzzer = requests.get("https://raw.githubusercontent.com/Eijebong/Archipelago-fuzzer/refs/heads/main/fuzz.py")
with open("/Archipelago/fuzz.py", "w") as f:
    f.write(get_fuzzer.text)

fuzz_cmd = [sys.executable, "/Archipelago/fuzz.py",
            "-g", stub,
            "-r", "50"]
subprocess.run(fuzz_cmd, check=False)
shutil.copy("/Archipelago/fuzz_output/report.json", "/out/fuzz_output.json")

get_worldman = requests.get("https://github.com/silasary/Archipelago/releases/download/apworld_manager-0.0.26/apworld_manager.apworld")
with open("/Archipelago/custom_worlds/apworld_manager.apworld", "wb") as f:
    f.write(get_worldman.content)
worldman_cmd = [sys.executable, "/Archipelago/Launcher.py",
                "worldman",
                "--",
                "--nogui",
                "--install", "tracker",
                ]

subprocess.run(worldman_cmd, check=False)

fuzz_ut_cmd = fuzz_cmd + [
    "--hook", "worlds.tracker.fuzzer_hook:Hook"
]
subprocess.run(fuzz_ut_cmd, check=False)
shutil.copy("/Archipelago/fuzz_output/report.json", "/out/fuzz_ut_output.json")

if os.environ.get("KEEP_RUNNING"):
    while True:
        sleep(1)
