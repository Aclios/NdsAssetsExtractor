from engines.chunsoft import SIR0
from ndstools.fs import EndianBinaryReader
from ndstools.formats import ImageCanva, RawBitmap, RawPalette

from pathlib import Path


class Bg999(SIR0):
    """
    Background data in 999
    """

    def _read(self, f: EndianBinaryReader):
        f.seek(self.info_start)
        self.left = f.read_UInt32()
        self.top = f.read_UInt32()
        self.right = f.read_UInt32()
        self.bottom = f.read_UInt32()
        self.unk3 = f.read_UInt32()
        self.unk4 = f.read_UInt32()
        self.bitmap_start = f.read_UInt32()
        self.palette_start = f.read_UInt32()
        self.palette_end = f.read_UInt32()
        self.bitmap_data = f.read_data_at(
            self.bitmap_start, self.palette_start - self.bitmap_start
        )
        self.palette_data = f.read_data_at(
            self.palette_start, self.palette_end - self.palette_start
        )

        self.width = (self.right - self.left + 1) * 8
        self.height = (self.bottom - self.top + 1) * 8

    def export_image(self, out_path: str):
        canva = ImageCanva(
            bitmap=RawBitmap(self.bitmap_data, try_decompress=False),
            palette=RawPalette(self.palette_data, try_decompress=False),
            bit_depth=8,
            im_size=(self.width, self.height),
            linear=True,
        )
        canva.resolve()
        Path(out_path).parent.mkdir(exist_ok=True, parents=True)
        canva.image.save(out_path)
