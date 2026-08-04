from ndstools.formats import File
from ndstools.fs import EndianBinaryReader
from pathlib import Path

import pandas as pd

TEXT_TYPE_MAP = {
    0xA: "Item",
    0x10: "Thoughts",
    0x14: "Flashback/Diary",
    0x84: "Choice",
    0xF2: "Room details",
}


class TheresiaScript(File):
    def __init__(self, filepath: Path, expected_next_offset: int):
        self.expected_next_offset = expected_next_offset
        super().__init__(filepath)

    def read(self, f: EndianBinaryReader):
        self.entries: list[TheresiaScriptText] = []
        filesize = f.get_size()
        val = f.read_UInt8()
        # A big hacky way to find all strings in the script
        # Works because luckily offsets are in ascending order
        while f.tell() < filesize - 5:
            if val in [0x10, 0x14, 0x84, 0xF2]:
                if val == 0xF2 or f.read_UInt8() == 0:
                    entry = TheresiaScriptText(f, val)
                    if (
                        entry.size != 0
                        and entry.offset == self.expected_next_offset
                        and entry.size < 0x80
                    ):
                        self.entries.append(entry)
                        self.expected_next_offset += entry.size
                    else:
                        f.seek(-5, 1)
                else:
                    f.seek(-1, 1)
            elif val == 0xA:
                if f.read_UInt16() == 0x1C82:
                    entry = TheresiaScriptText(f, val)
                    if (
                        entry.size != 0
                        and entry.offset == self.expected_next_offset
                        and entry.size < 0x80
                    ):
                        self.entries.append(entry)
                        self.expected_next_offset += entry.size
                    else:
                        f.seek(-5, 1)
                else:
                    f.seek(-2, 1)
            val = f.read_UInt8()

    def export_to_excel(self, out_path: Path, text_data: bytes):
        data = [(entry.type, entry.get_text(text_data)) for entry in self.entries]
        df = pd.DataFrame(data=data, columns=["Type", "Text"])
        df.to_excel(out_path, index=False)


class TheresiaScriptText:
    def __init__(self, f: EndianBinaryReader, code: str):
        self.size = f.read_UInt8()
        self.offset = f.read_UInt32()
        self.type = TEXT_TYPE_MAP[code]

    def get_text(self, text_data: bytes):
        if self.size == 0x80:
            return ""
        return text_data[self.offset : self.offset + self.size].decode("shift-jis-2004")
