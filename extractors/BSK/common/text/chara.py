from utils.excel import write_excel
from engines.chunsoft import SIR0
from ndstools.fs import EndianBinaryReader

class Chara999(SIR0):
    def _read(self, f: EndianBinaryReader):
        f.seek(self.info_start)
        self.entries: list[CharaEntry] = []
        while f.peek(4) != bytes(4):
            self.entries.append(CharaEntry(f))

    def export_excel(self, out_path: str):
        data = [
            [entry.japanese, entry.english, entry.context, entry.se_ref]
            for entry in self.entries
        ]
        columns = ["Japanese", "English", "Context", "SE Ref"]
        write_excel(out_path, data, columns)

class CharaEntry:
    def __init__(self, f: EndianBinaryReader):
        self.japanese_offset = f.read_UInt32()
        self.english_offset = f.read_UInt32()
        self.context_offset = f.read_UInt32()
        self.unk = f.read_UInt32()
        self.se_ref_offset = f.read_UInt32()
        pos = f.tell()
        f.seek(self.japanese_offset)
        self.japanese = f.read_string().decode("shift-jis-2004")
        f.seek(self.english_offset)
        self.english = f.read_string().decode("shift-jis-2004")
        f.seek(self.context_offset)
        self.context = f.read_string().decode("shift-jis-2004")
        f.seek(self.se_ref_offset)
        self.se_ref = f.read_string().decode("shift-jis-2004")
        f.seek(pos)

