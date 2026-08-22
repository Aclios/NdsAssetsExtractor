from engines.chunsoft import SIR0
from ndstools.fs import EndianBinaryReader
from ndstools.formats import ImageCanva, RawBitmap, RawPalette

from pathlib import Path
from PIL import Image


class Char999(SIR0):
    """
    Characters sprites in 999
    """

    def _read(self, f: EndianBinaryReader):
        f.seek(self.info_start)
        self.symbols_offset = [f.read_UInt32() for _ in range(0x10)]
        self.pointers_offset = f.read_UInt32()
        f.seek(self.pointers_offset)
        self.total_bitmap_size = f.read_UInt32()
        self.unk1 = f.read_UInt32()
        self.unk2 = f.read_UInt32()
        self.unk3 = f.read_UInt32()
        self.unk4 = f.read_UInt32()
        self.palette_start = f.read_UInt32()
        self.bitmap_start = f.read_UInt32()
        self.regions_start = f.read_UInt32()
        self.additional_starts = [f.read_UInt32() for _ in range(0x10)]

        self.palette_data = f.read_data_at(self.palette_start, 0x200)
        self.bitmap_data = f.read_data_at(self.bitmap_start, self.total_bitmap_size)
        f.seek(self.regions_start)
        # There should be a better way to do that surely
        regions_end = (
            self.additional_starts[0]
            if self.additional_starts[0]
            else self.pointers_offset
        )
        self.region_count = (regions_end - self.regions_start) // 0xA
        self.regions = [Char999Region(f) for _ in range(self.region_count)]

        for region in self.regions:
            region.bitmap_data = self.bitmap_data[
                region.data_start_offset : region.data_start_offset
                + (region.width * region.height)
            ]
        self.palette = RawPalette(self.palette_data, try_decompress=False)

    def export_sprite(self, out_path: str):
        im_size, offsets = self._calculate_dimensions()
        im = Image.new(mode="RGBA", size=im_size)
        for region in self.regions:
            canva = ImageCanva(
                RawBitmap(region.bitmap_data),
                self.palette,
                bit_depth=8,
                im_size=(region.width, region.height),
                linear=True,
                transparency=True,
            )
            canva.resolve()
            im.paste(
                canva.image, (region.dest_x - offsets[0], region.dest_y - offsets[1])
            )
        im.save(out_path)

    def _calculate_dimensions(self):
        width = max(region.width + region.dest_x for region in self.regions)
        height = max(region.height + region.dest_y for region in self.regions)
        x_offset = min(region.dest_x for region in self.regions)
        y_offset = min(region.dest_y for region in self.regions)
        return (width - x_offset, height - y_offset), (x_offset, y_offset)


class Char999Region:
    bitmap_data: bytes

    def __init__(self, f: EndianBinaryReader):
        self.width = f.read_UInt16()
        self.height = f.read_UInt16()
        self.dest_x = f.read_UInt16()
        self.dest_y = f.read_UInt16()
        self.data_start_offset = f.read_UInt16()
