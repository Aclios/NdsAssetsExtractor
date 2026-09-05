from utils.excel import write_excel
from engines.chunsoft import SIR0
from ndstools.fs import EndianBinaryReader
from .utils import read_999_string_at

SECTION_COUNT = 17


class Camera999(SIR0):
    def _read(self, f: EndianBinaryReader):
        f.seek(self.info_start)
        self.sections = [Camera999Section(f) for _ in range(SECTION_COUNT)]
        self.entries: list[Camera999Entry] = []
        for idx, section in enumerate(self.sections):
            f.seek(section.pointers_start)
            entry_count = (
                self.sections[idx + 1].pointers_start - section.pointers_start
                if idx < len(self.sections) - 1
                else self.info_start - section.pointers_start
            ) // 24
            self.entries.extend([Camera999Entry(f) for _ in range(entry_count)])

    def export_excel(self, out_path: str):
        data = [
            [entry.english, entry.japanese, entry.context] for entry in self.entries
        ]
        columns = ["English", "Japanese", "Context"]
        write_excel(out_path, data, columns)


class Camera999Section:
    def __init__(self, f: EndianBinaryReader):
        self.data_start = f.read_UInt32()
        self.pointers_start = f.read_UInt32()


class Camera999Entry:
    def __init__(self, f: EndianBinaryReader):
        self.english_offset = f.read_UInt32()
        self.japanese_offset = f.read_UInt32()
        self.context_offset = f.read_UInt32()
        self.unk1 = f.read_UInt32()
        self.unk2 = f.read_UInt32()
        self.unk3 = f.read_UInt32()
        pos = f.tell()
        self.english = read_999_string_at(f, self.english_offset)
        self.japanese = read_999_string_at(f, self.japanese_offset)
        self.context = read_999_string_at(f, self.context_offset)
        f.seek(pos)
