from utils.excel import write_excel
from engines.chunsoft import SIR0
from ndstools.fs import EndianBinaryReader
from .utils import read_shift_jis_at


class File999(SIR0):
    def _read(self, f: EndianBinaryReader):
        f.seek(self.info_start)
        self.entries: list[File999Entry] = []
        while f.peek(4) != bytes(4):
            self.entries.append(File999Entry(f))

    def export_excel(self, out_path: str):
        data = []
        for entry in self.entries:
            data.append([entry.symb1, entry.symb2, entry.title])
            data.extend([["", "", page] for page in entry.pages])
        columns = ["Symbol1", "Symbol2", "Text"]
        write_excel(out_path, data, columns)


class File999Entry:
    def __init__(self, f: EndianBinaryReader):
        self.symb1_offset = f.read_UInt32()
        self.title_offset = f.read_UInt32()
        self.symb2_offset = f.read_UInt32()
        self.pages_table_offset = f.read_UInt32()
        pos = f.tell()
        f.seek(self.pages_table_offset)
        self.pages_offset = list(iter(lambda: f.read_UInt32(), 0))
        self.symb1 = read_shift_jis_at(f, self.symb1_offset)
        self.title = read_shift_jis_at(f, self.title_offset)
        self.symb2 = read_shift_jis_at(f, self.symb2_offset)
        self.pages = [read_shift_jis_at(f, offset) for offset in self.pages_offset]
        f.seek(pos)
