from pathlib import Path
from . import Bg999, Char999


def unpack_all(base_dir: Path):
    """
    Logic for unpacking archives or decompressing files before extracting assets (if necessary).
    """
    print("Unpacking files...")
    pass


def extract_all_images(base_dir: Path, images_dir: Path):
    """
    Logic for images extraction.
    """
    print("Exporting backgrounds...")
    for file in Path(base_dir, "bg").rglob("*"):
        if file.is_file() and file.suffix == ".dat":
            bg = Bg999(file)
            bg.export_image(Path(images_dir, "bg", file.with_suffix(".png").name))

    print("Exporting characters sprites...")
    for file in Path(base_dir, "char").iterdir():
        char = Char999(file)
        char.export_sprite(Path(images_dir, "cha", file.with_suffix(".png").name))


def extract_all_models(base_dir: Path, assets_dir: Path):
    """
    Logic for 3D models and textures extraction.
    """
    print("Exporting models textures...")
    pass


def extract_all_texts(base_dir: Path, assets_dir: Path):
    """
    Logic for text/script extraction.
    """
    print("Exporting text...")
    pass


def extract_all_sounds(base_dir: Path, assets_dir: Path):
    """
    Logic for sound/music extraction.
    """
    print("Exporting sound effects...")
    pass


def extract_all_animations(base_dir: Path, assets_dir: Path):
    """
    Logic for 2D animations extraction.
    """
    print("Exporting animations...")
    pass


def extract_all_assets(extraction_dir: Path, assets_dir: Path):
    """
    Put all the extraction logic here.

    extraction_dir refers to the files extracted from the NDS rom.

    assets_dir refers to the directory were assets will be written.
    """
    files_dir = extraction_dir / "files"
    code_dir = extraction_dir / "code"

    extract_all_images(files_dir, assets_dir / "images")
    extract_all_models(files_dir, assets_dir / "models")
    extract_all_texts(files_dir, assets_dir / "text")
    extract_all_sounds(files_dir, assets_dir / "sound")
    extract_all_animations(files_dir, assets_dir)
