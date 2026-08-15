from pathlib import Path
from ..common.archive import DashNitroArchive


def unpack_all(base_dir: Path):
    """
    Logic for unpacking archives or decompressing files before extracting assets (if necessary).
    """
    print("Unpacking files...")
    arc = DashNitroArchive(base_dir / "archive.archive")
    arc.extract_all(base_dir / "_archive")
    pass


def extract_all_images(base_dir: Path, assets_dir: Path):
    """
    Logic for images extraction.
    """
    print("Exporting images...")
    pass


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

    unpack_all(files_dir)
    extract_all_images(files_dir, assets_dir)
    extract_all_models(files_dir, assets_dir)
    extract_all_texts(files_dir, assets_dir)
    extract_all_sounds(files_dir, assets_dir)
    extract_all_animations(files_dir, assets_dir)
