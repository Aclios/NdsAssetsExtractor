from utils.excel import write_excel
from engines.chunsoft import SIR0
from ndstools.fs import EndianBinaryReader
from .utils import read_shift_jis_at


class Room999(SIR0):
    def _read(self, f: EndianBinaryReader):
        f.seek(self.info_start)
        self.symb_a_offset = f.read_UInt32()
        self.table_a_offset = f.read_UInt32()
        self.symb_b_offset = f.read_UInt32()
        self.table_b_offset = f.read_UInt32()
        self.symb_c_offset = f.read_UInt32()
        self.table_c_offset = f.read_UInt32()
        self.entries: list[Room999Entry] = []
        f.seek(self.table_a_offset)
        while f.peek(4) != bytes(4):
            self.entries.append(Room999Entry(f))
        f.seek(self.table_b_offset)
        while f.peek(4) != bytes(4):
            self.entries.append(Room999Entry(f))
        f.seek(self.table_c_offset)
        while f.peek(4) != bytes(4):
            self.entries.append(Room999Entry(f))

    def export_excel(self, out_path: str):
        data = [
            [entry.symb1, entry.text, entry.symb2, entry.symb3, entry.symb4]
            for entry in self.entries
        ]
        columns = ["Symbol 1", "Text", "Symbol 2", "Symbol 3", "Symbol 4"]
        write_excel(out_path, data, columns)


class Room999Entry:
    def __init__(self, f: EndianBinaryReader):
        self.symb1_offset = f.read_UInt32()
        self.text_offset = f.read_UInt32()
        self.symb2_offset = f.read_UInt32()
        self.symb3_offset = f.read_UInt32()
        self.symb4_offset = f.read_UInt32()
        pos = f.tell()
        self.symb1 = read_shift_jis_at(f, self.symb1_offset)
        self.text = read_shift_jis_at(f, self.text_offset)
        self.symb2 = read_shift_jis_at(f, self.symb2_offset)
        self.symb3 = read_shift_jis_at(f, self.symb3_offset)
        self.symb4 = read_shift_jis_at(f, self.symb4_offset)
        f.seek(pos)
