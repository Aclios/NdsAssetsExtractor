from ndstools.fs import EndianBinaryReader
from ndstools.compression import decompress
from ndstools.formats import File


class TheresiaPack(File):
    def read(self, f: EndianBinaryReader):
        self.entry_count = self.guess_entry_count(f)
        self.entries = [TheresiaPackEntry(f) for _ in range(self.entry_count)]

    def guess_entry_count(self, f: EndianBinaryReader):
        offset = f.read_UInt32()
        while offset == 0:
            f.seek(8, 1)
            offset = f.read_UInt32()
        f.seek(0)
        return offset // 12

    def get_entry_data(self, idx: int):
        if idx >= len(self.entries):
            raise Exception(
                f"There are only {self.entry_count} entries in the pack. Requested index: {idx}."
            )
        entry = self.entries[idx]
        if not entry.has_data:
            raise Exception(f"Entry on index {idx} doesn't have data.")
        if not entry.is_compressed:
            return entry.data
        decompressed_data, _ = decompress(entry.data)
        return decompressed_data


class TheresiaPackEntry:
    is_compressed: bool = False
    has_data: bool = False

    def __init__(self, f: EndianBinaryReader):
        self.data_offset = f.read_UInt32()
        self.compressed_size = f.read_UInt32()
        self.decompressed_size = f.read_UInt32() % 0x80_00_00_00

        if self.decompressed_size != 0:
            self.is_compressed = True

        if self.compressed_size != 0:
            self.has_data = True
            pos = f.tell()
            f.seek(self.data_offset)
            self.data = f.read(self.compressed_size)
            f.seek(pos)
