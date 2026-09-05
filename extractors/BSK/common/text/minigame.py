from utils.excel import write_excel
from engines.chunsoft import SIR0
from ndstools.fs import EndianBinaryReader
from .utils import read_999_string_at


class Minigame999(SIR0):
    def _read(self, f: EndianBinaryReader):
        f.seek(self.info_start)
        self.symb_offset = f.read_UInt32()
        self.table_start = f.read_UInt32()
        f.seek(self.table_start)
        self.entries: list[Minigame999Entry] = []
        while f.peek(4) != bytes(4):
            self.entries.append(Minigame999Entry(f))

    def export_excel(self, out_path: str):
        data = [[entry.symb, entry.text] for entry in self.entries]
        columns = ["Symbol", "Text"]
        write_excel(out_path, data, columns)


class Minigame999Entry:
    def __init__(self, f: EndianBinaryReader):
        self.symb_offset = f.read_UInt32()
        self.text_offset = f.read_UInt32()
        pos = f.tell()
        self.symb = read_999_string_at(f, self.symb_offset)
        self.text = read_999_string_at(f, self.text_offset)
        f.seek(pos)
