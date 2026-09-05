from utils.excel import write_excel
from engines.chunsoft import SIR0
from ndstools.fs import EndianBinaryReader
from .utils import read_999_string_at


class Chara999(SIR0):
    def _read(self, f: EndianBinaryReader):
        f.seek(self.info_start)
        self.entries: list[Chara999Entry] = []
        while f.peek(4) != bytes(4):
            self.entries.append(Chara999Entry(f))

    def export_excel(self, out_path: str):
        data = [
            [entry.japanese, entry.english, entry.context, entry.se_ref]
            for entry in self.entries
        ]
        columns = ["Japanese", "English", "Context", "SE Ref"]
        write_excel(out_path, data, columns)


class Chara999Entry:
    def __init__(self, f: EndianBinaryReader):
        self.japanese_offset = f.read_UInt32()
        self.english_offset = f.read_UInt32()
        self.context_offset = f.read_UInt32()
        self.unk = f.read_UInt32()
        self.se_ref_offset = f.read_UInt32()
        pos = f.tell()
        self.japanese = read_999_string_at(f, self.japanese_offset)
        self.english = read_999_string_at(f, self.english_offset)
        self.context = read_999_string_at(f, self.context_offset)
        self.se_ref = read_999_string_at(f, self.se_ref_offset)
        f.seek(pos)
