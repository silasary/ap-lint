import os
from typing import NamedTuple
import json
import zipfile
import glob

class WorldInfo(NamedTuple):
    game: str
    stub: str
    manifest: dict

def setup_world():
    os.makedirs("/worlds", exist_ok=True)
    os.makedirs("/out", exist_ok=True)

    worlds = glob.glob("/worlds/*.apworld")
    if len(worlds) == 0:
        raise RuntimeError("No worlds found in /worlds")
    elif len(worlds) > 1:
        raise RuntimeError("Multiple worlds found in /worlds")

    world = os.path.basename(worlds[0])
    stub = os.path.splitext(world)[0]
    with zipfile.ZipFile(f"/worlds/{world}", 'r') as zip_ref:
        zip_ref.extractall("/Archipelago/worlds")
        if 'archipelago.json' in zip_ref.namelist():
            manifest = zip_ref.read('archipelago.json')
        elif (manifest_path := f'{stub}/archipelago.json') in zip_ref.namelist():
            manifest = zip_ref.read(manifest_path)
        else:
            raise RuntimeError("archipelago.json not found in the world zip")
    print(f"Extracted world {world} to /Archipelago/worlds")

    parsed_manifest = json.loads(manifest)

    stat = WorldInfo(game=parsed_manifest["game"], stub=stub, manifest=parsed_manifest)
    with open("/out/stat.json", 'w') as f:
        json.dump(stat._asdict(), f, indent=4)
    return stat
