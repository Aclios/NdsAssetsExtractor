from utils.excel import write_excel
from engines.chunsoft import SIR0
from ndstools.fs import EndianBinaryReader
from .utils import read_999_string_at


class Staff999(SIR0):
    def _read(self, f: EndianBinaryReader):
        f.seek(self.info_start)
        self.symb_a_offset = f.read_UInt32()
        self.table_a_offset = f.read_UInt32()
        self.symb_b_offset = f.read_UInt32()
        self.table_b_offset = f.read_UInt32()
        self.symb_c_offset = f.read_UInt32()
        self.table_c_offset = f.read_UInt32()
        self.entries: list[Staff999Entry] = []
        f.seek(self.table_a_offset)
        while f.peek(4) != bytes(4):
            self.entries.append(Staff999Entry(f))
        f.seek(self.table_b_offset)
        while f.peek(4) != bytes(4):
            self.entries.append(Staff999Entry(f))
        f.seek(self.table_c_offset)
        while f.peek(4) != bytes(4):
            self.entries.append(Staff999Entry(f))

    def export_excel(self, out_path: str):
        data = [[entry.text] for entry in self.entries]
        columns = ["Text"]
        write_excel(out_path, data, columns)


class Staff999Entry:
    def __init__(self, f: EndianBinaryReader):
        self.text_offset = f.read_UInt32()
        pos = f.tell()
        self.text = read_999_string_at(f, self.text_offset)
        f.seek(pos)
