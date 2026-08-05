from ndstools.formats import NDSRom
import json
from pathlib import Path

from .maker import get_maker
from .region import get_region


def dump_game_info(rom: NDSRom, out_path: Path):
    data = {
        "title": rom.name,
        "code": rom.game_code,
        "maker": get_maker(rom.maker_code),
        "region": get_region(rom.game_code),
    }
    if rom.banner:
        data.update(rom.banner.get_names())
    json.dump(data, out_path.open("w", encoding="utf-8"), indent=4, ensure_ascii=False)
