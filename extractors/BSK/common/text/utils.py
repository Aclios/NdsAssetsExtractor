from ndstools.fs import EndianBinaryReader


def read_shift_jis_at(f: EndianBinaryReader, offset: int):
    f.seek(offset)
    return f.read_string().decode("shift-jis-2004")
