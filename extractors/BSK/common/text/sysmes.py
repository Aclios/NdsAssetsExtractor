from utils.excel import write_excel
from engines.chunsoft import SIR0
from ndstools.fs import EndianBinaryReader
from .utils import read_999_string_at


class SysMes999(SIR0):
    def _read(self, f: EndianBinaryReader):
        f.seek(self.info_start)
        self.entries: list[SysMes999Entry] = []
        while f.peek(4) != bytes(4):
            self.entries.append(SysMes999Entry(f))

    def export_excel(self, out_path: str):
        data = []
        for entry in self.entries:
            data.append([entry.symb, ""])
            data.extend([["", page] for page in entry.pages])
        columns = ["Symbol", "Text"]
        write_excel(out_path, data, columns)


class SysMes999Entry:
    def __init__(self, f: EndianBinaryReader):
        self.symb_offset = f.read_UInt32()
        self.unk1 = f.read_UInt32()
        self.unk2 = f.read_UInt32()
        self.unk3 = f.read_UInt32()
        self.unk4 = f.read_UInt32()
        self.table_offset = f.read_UInt32()
        pos = f.tell()
        f.seek(self.table_offset)
        self.pages_offsets = list(iter(lambda: f.read_UInt32(), 0))
        self.pages = [read_999_string_at(f, offset) for offset in self.pages_offsets]
        self.symb = read_999_string_at(f, self.symb_offset)
        f.seek(pos)
