from pathlib import Path


def unpack_all(base_dir: Path):
    """
    Logic for unpacking archives or decompressing files before extracting assets (if necessary).
    """
    pass


def extract_all_images(base_dir: Path, assets_dir: Path):
    """
    Logic for images extraction.
    """
    pass


def extract_all_models(base_dir: Path, assets_dir: Path):
    """
    Logic for 3D models and textures extraction.
    """
    pass


def extract_all_texts(base_dir: Path, assets_dir: Path):
    """
    Logic for text/script extraction.
    """
    pass


def extract_all_sounds(base_dir: Path, assets_dir: Path):
    """
    Logic for sound/music extraction.
    """
    pass


def extract_all_animations(base_dir: Path, assets_dir: Path):
    """
    Logic for 2D animations extraction.
    """
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
    extract_all_images(extraction_dir, assets_dir)
    extract_all_models(extraction_dir, assets_dir)
    extract_all_texts(extraction_dir, assets_dir)
    extract_all_sounds(extraction_dir, assets_dir)
    extract_all_animations(extraction_dir, assets_dir)
