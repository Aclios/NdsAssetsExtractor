from ..common.main import extract_all_assets as _extract_all_assets
from pathlib import Path

def extract_all_assets(extraction_dir: Path, assets_dir: Path):
    _extract_all_assets(extraction_dir, assets_dir, 'jp')
