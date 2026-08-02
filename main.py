import sys
import json
import importlib
from pathlib import Path

from ndstools.formats import NDSRom


def main():
    rom_path = sys.argv[1]
    try:
        rom = NDSRom(rom_path)
    except:
        raise Exception(
            f"Couldn't load ROM from file {rom_path}. Are you sure it's an NDS ROM?"
        )

    global_game_code = rom.game_code[:-1]
    games: dict = json.load(open("games.json", "r", encoding="utf-8"))
    game_data: dict = games.get(global_game_code, {})
    if not game_data:
        raise Exception(f"Game with code {global_game_code} is not supported.")
    game_region_data = game_data.get(rom.game_code)

    if not game_region_data:
        raise Exception(
            f"Game with code {global_game_code} is supported, but not for this region: {rom.game_code}."
        )

    module_name = f"extractors.{global_game_code}.{rom.game_code}.main"
    try:
        module = importlib.import_module(module_name)
    except ImportError as e:
        print(e)
        raise Exception(
            f"Error: couldn't load the {global_game_code}/{rom.game_code} extractor."
        )

    extracted_rom_dir = Path("temp", rom.game_code)
    rom.extract_all(extracted_rom_dir)

    assets_dir = Path(rom.game_code)
    assets_dir.mkdir(exist_ok=True)
    module.extract_all_assets(extracted_rom_dir, assets_dir)


if __name__ == "__main__":
    main()
