from ndstools.fs import EndianBinaryReader


def read_999_string_at(f: EndianBinaryReader, offset: int):
    f.seek(offset)
    return decode_999_string(f.read_string())


def decode_999_string(data: bytes):
    decoded = data.decode("shift-jis-2004")
    decoded = decoded.replace("Ｓ", "'").replace("Ｄ", '"')
    return decoded
