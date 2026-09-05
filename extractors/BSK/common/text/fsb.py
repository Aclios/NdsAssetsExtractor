from utils.excel import write_excel
from engines.chunsoft import SIR0
from ndstools.fs import EndianBinaryReader, EndianBinaryStreamReader
from .utils import read_999_string_at

SCRIPT_START = 0x10


class Fsb(SIR0):
    def _read(self, f: EndianBinaryReader):
        f.seek(self.info_start)
        self.name_offset = f.read_UInt32()
        self.script_table_offset = f.read_UInt32()
        self.text_entry_count = f.read_UInt32()
        self.text_table_offset = f.read_UInt32()
        self.flags_symb_offset = f.read_UInt32()
        self.flags_table_offset = f.read_UInt32()
        f.seek(self.text_table_offset)
        self.text_entries = [FsbTextEntry(f) for _ in range(self.text_entry_count)]
        f.seek(SCRIPT_START)
        self.raw_script = f.read(self.text_entries[0].offset - SCRIPT_START)
        self._get_text_order()

    def _get_text_order(self):
        self._ordered_text = []
        f = EndianBinaryStreamReader(self.raw_script)
        while True:
            lookup = f.peek(4)
            if len(lookup) != 4:
                break
            if int.from_bytes(lookup, "little") in [0x2F_00_68_28, 0x2F_00_69_28]:
                f.read(4)
                text_entry_idx = f.read_UInt16()
                self._ordered_text.append(self.text_entries[text_entry_idx].text)
            else:
                f.read(1)

    def export_excel(self, out_path: str):
        data = [[text] for text in self._ordered_text]
        columns = ["Text"]
        write_excel(out_path, data, columns)


class FsbTextEntry:
    def __init__(self, f: EndianBinaryReader):
        self.offset = f.read_UInt32()
        pos = f.tell()
        self.text = read_999_string_at(f, self.offset)
        f.seek(pos)
