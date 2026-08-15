from ndstools.fs import EndianBinaryFileReader
from pathlib import Path

class DashNitroArchive:
    def __init__(self, filepath: str):
        with EndianBinaryFileReader(filepath) as f:
            self.magic = f.check_magic(b"NITRO Archive 1\x00")
            self.file_count = f.read_UInt32()
            self.unk = f.read_UInt32()
            self.padding = f.read(8)
            self.entries = [ArchiveEntry(f) for _ in range(self.file_count)]

    def extract_all(self, out_dir: str):
        Path(out_dir).mkdir(exist_ok=True, parents=True)
        for entry in self.entries:
            Path(out_dir, entry.name).write_bytes(entry.data)


class ArchiveEntry:
    def __init__(self, f: EndianBinaryFileReader):
        self.name_offset = f.read_UInt32()
        self.data_offset = f.read_UInt32()
        self.data_size = f.read_UInt32()
        pos = f.tell()
        f.seek(self.name_offset)
        self.name = f.read_string_until_null().decode()
        self.data = f.read_data_at(self.data_offset, self.data_size)
        f.seek(pos)