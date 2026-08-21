from utils.excel import write_excel
from engines.chunsoft import SIR0
from ndstools.fs import EndianBinaryReader

SECTION_COUNT = 17

class Camera999(SIR0):
    def _read(self, f: EndianBinaryReader):
        f.seek(self.info_start)
        self.sections = [CameraSection(f) for _ in range(SECTION_COUNT)]
        self.entries: list[CameraEntry] = []
        for idx, section in enumerate(self.sections):
            f.seek(section.pointers_start)
            entry_count = (
                self.sections[idx + 1].pointers_start - section.pointers_start
                if idx < len(self.sections) - 1 else self.info_start - section.pointers_start
            ) // 24
            self.entries.extend([CameraEntry(f) for _ in range(entry_count)])

    def export_excel(self, out_path: str):
        data = [
            [entry.english, entry.japanese, entry.context]
            for entry in self.entries
        ]
        columns=["English", "Japanese", "Context"]
        write_excel(out_path, data, columns)

class CameraSection:
    def __init__(self, f: EndianBinaryReader):
        self.data_start = f.read_UInt32()
        self.pointers_start = f.read_UInt32()

class CameraEntry:
    def __init__(self, f: EndianBinaryReader):
        self.english_offset = f.read_UInt32()
        self.japanese_offset = f.read_UInt32()
        self.context_offset = f.read_UInt32()
        self.unk1 = f.read_UInt32()
        self.unk2 = f.read_UInt32()
        self.unk3 = f.read_UInt32()
        pos = f.tell()
        f.seek(self.english_offset)
        self.english = f.read_string().decode("shift-jis-2004")
        f.seek(self.japanese_offset)
        self.japanese = f.read_string().decode("shift-jis-2004")
        f.seek(self.context_offset)
        self.context = f.read_string().decode("shift-jis-2004")
        f.seek(pos)