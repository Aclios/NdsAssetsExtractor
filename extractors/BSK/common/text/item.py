from utils.excel import write_excel
from engines.chunsoft import SIR0
from ndstools.fs import EndianBinaryReader
from .utils import read_999_string_at


class Item999(SIR0):
    def _read(self, f: EndianBinaryReader):
        f.seek(self.info_start)
        self.sections: list[Item999Section] = []
        while f.peek(4) != bytes(4):
            self.sections.append(Item999Section(f))

    def export_excel(self, out_path: str):
        data = []
        for section in self.sections:
            data.append([section.symbol, "", "", ""])
            data.extend(
                [
                    ["", entry.japanese, entry.english, entry.context]
                    for entry in section.entries
                ]
            )
        columns = ["Symbol", "Japanese", "English", "Context"]
        write_excel(out_path, data, columns)


class Item999Section:
    def __init__(self, f: EndianBinaryReader):
        self.symb_offset = f.read_UInt32()
        self.pointers_offset = f.read_UInt32()
        pos = f.tell()
        f.seek(self.pointers_offset)
        self.entries: list[Item999Entry] = []
        while f.peek(4) != bytes(4):
            self.entries.append(Item999Entry(f))
        self.symbol = read_999_string_at(f, self.symb_offset)
        f.seek(pos)


class Item999Entry:
    def __init__(self, f: EndianBinaryReader):
        self.japanese_offset = f.read_UInt32()
        self.unk = f.read_UInt32()
        self.english_offset = f.read_UInt32()
        self.context_offset = f.read_UInt32()
        self.stuff = f.read(0x10)
        pos = f.tell()
        self.japanese = read_999_string_at(f, self.japanese_offset)
        self.english = read_999_string_at(f, self.english_offset)
        self.context = read_999_string_at(f, self.context_offset)
        f.seek(pos)
