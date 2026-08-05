import json
import sys
import shutil
from pathlib import Path
from ndstools.formats import NDSRom

from utils.region import get_region
from utils.maker import get_maker


def get_unique_names(names: dict):
    return list(set(names.values()))


def add_game(filepath: str):
    rom = NDSRom(filepath)
    games: dict = json.load(open("games.json", "r", encoding="utf-8"))
    data = {
        "title": rom.name,
        "code": rom.game_code,
        "region": get_region(rom.game_code),
        "maker": get_maker(rom.maker_code),
        "names": get_unique_names(rom.banner.get_names()),
    }
    global_game_code = rom.game_code[:-1]
    if not games.get(global_game_code):
        games[global_game_code] = {}
        print(f"Registered game {global_game_code}.")
    if games[global_game_code].get(rom.game_code):
        raise Exception(f"Game {rom.game_code} is already registered.")
    games[global_game_code][rom.game_code] = data
    print(f"Registered game region {rom.game_code}.")
    games[global_game_code] = dict(sorted(games[global_game_code].items()))
    games = dict(sorted(games.items()))
    json.dump(
        games, open("games.json", "w", encoding="utf-8"), indent=4, ensure_ascii=False
    )

    script_path = Path("extractors", global_game_code, rom.game_code)
    script_path.mkdir(exist_ok=True, parents=True)
    readme_path = Path("extractors", global_game_code, "README.md")
    if not readme_path.exists():
        readme_path.write_text(rom.banner.japanese.replace("\n", " "), encoding="utf-8")

    shutil.copy(Path("extractors", "_template", "main.py"), script_path / "main.py")
    print(f"Copied extractor template into {script_path}.")


if __name__ == "__main__":
    add_game(sys.argv[1])
