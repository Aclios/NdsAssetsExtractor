import shutil
from pathlib import Path
from . import TheresiaPack, TheresiaBgData, TheresiaSpData, TheresiaScript
from ndstools.formats import NFTR, NSBMD, SDAT
from ndstools.compression import decompress


def extract_all_images(base_dir: Path, images_dir: Path):
    nanr_pack = TheresiaPack(base_dir / "nanpack.dat")
    ncer_pack = TheresiaPack(base_dir / "ncepack.dat")
    ncgr_pack = TheresiaPack(base_dir / "ncgpack.dat")
    nclr_pack = TheresiaPack(base_dir / "nclpack.dat")
    nscr_pack = TheresiaPack(base_dir / "nscpack.dat")

    print("Exporting background images...")
    bg_data = TheresiaBgData(base_dir / "bgdata.dat")
    bg_data.export_all(ncgr_pack, nscr_pack, nclr_pack, images_dir / "bg")

    print("Exporting cell images...")
    sp_data = TheresiaSpData(base_dir / "spdata.dat")
    sp_data.export_all(ncgr_pack, ncer_pack, nclr_pack, nanr_pack, images_dir / "sp")

    print("Exporting misc images...")
    ht_data = TheresiaSpData(base_dir / "htdata.dat")
    ht_data.export_all(ncgr_pack, ncer_pack, nclr_pack, nanr_pack, images_dir / "ht")

    print("Exporting font glyphs...")
    font = NFTR(base_dir / "a.NFTR")
    font.export_glyphs(images_dir / "font.png")


def extract_all_models(base_dir: Path, models_dir: Path):
    """
    Logic for 3D models and textures extraction.
    """
    print("Exporting models textures...")
    for file in Path(base_dir / "3d").iterdir():
        if file.is_file() and file.suffix == ".nsbmd":
            model = NSBMD(file)
            model.export_textures(models_dir / file.with_suffix("").name)


def extract_all_texts(base_dir: Path, text_dir: Path, region: str):
    """
    Logic for text/script extraction.
    """

    def _export_text_from_dir(base_dir: Path, text_dir: Path):
        expected_next_offset = 0
        if region == 'jp':
            raw_string, _ = decompress(Path(base_dir, "common.txt").read_bytes())
        Path(text_dir).mkdir(exist_ok=True)
        for file in Path(base_dir).iterdir():
            if file.is_file() and file.suffix == ".adv":
                _expected_next_offset = expected_next_offset if region == "jp" else 0
                # Ugly hack because there is some presumably unused text in the middle of the file
                if region == "jp" and str(base_dir).endswith("sub") and file.name == "scene003_s.txt.adv":
                    next_offset = 0x03_9D_3B
                    missing_text = raw_string[_expected_next_offset:next_offset]
                    _expected_next_offset = next_offset
                    Path(text_dir / "unknown_text.txt").write_bytes(missing_text)
                script = TheresiaScript(file, _expected_next_offset)
                expected_next_offset = script.expected_next_offset
                if region != "jp":
                    raw_string, _ = decompress(file.with_suffix(".txt").read_bytes())
                script.export_to_excel(
                    text_dir / file.with_suffix(".xlsx").name, raw_string
                )

    print("Exporting text...")
    _export_text_from_dir(base_dir / "script", text_dir)
    _export_text_from_dir(base_dir / "script" / "opt", text_dir / "opt")
    _export_text_from_dir(base_dir / "script" / "opt2", text_dir / "opt2")
    _export_text_from_dir(base_dir / "script" / "sub", text_dir / "sub")
    shutil.copy(base_dir / "system.txt", text_dir / "system.txt")


def extract_all_sounds(base_dir: Path, sound_dir: Path):
    """
    Logic for sound/music extraction.
    """
    print("Exporting sound effects...")
    sdat = SDAT(base_dir / "sound" / "sound_data.sdat")
    sdat.unpack(sound_dir)


def extract_all_animations(base_dir: Path, assets_dir: Path):
    """
    Logic for 2D animations extraction.
    """
    pass


def extract_all_assets(extraction_dir: Path, assets_dir: Path, region: str):
    """
    Put all the extraction logic here.

    extraction_dir refers to the files extracted from the NDS rom.

    assets_dir refers to the directory were assets will be written.
    """
    files_dir = extraction_dir / "files" / "data"

    extract_all_images(files_dir, assets_dir / "images")
    extract_all_models(files_dir, assets_dir / "models")
    extract_all_texts(files_dir, assets_dir / "text", region)
    extract_all_sounds(files_dir, assets_dir / "sound")
    extract_all_animations(files_dir, assets_dir)

    print("Successfully exported all supported assets from the game!")
