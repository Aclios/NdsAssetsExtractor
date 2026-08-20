from ndstools.fs import (
    EndianBinaryFileReader,
    EndianBinaryReader,
    EndianBinaryStreamReader,
)

from .atxp import atxp_decompress


class SIR0:
    """
    The SIR0 format is just a container for arbitrary data.

    The whole file may be compressed.
    """

    def __init__(self, filepath: str):
        with EndianBinaryFileReader(filepath) as f:
            magic = f.read(4)
            if magic == b"SIR0":
                f.seek(0)
            else:
                try:
                    data = magic + f.read()
                    dec_data = atxp_decompress(data)
                    f = EndianBinaryStreamReader(dec_data)
                except:
                    raise Exception(
                        f"Couldn't open SIR0 file with magic {magic}. Maybe it uses an unsupported compression?"
                    )
            self.magic = f.check_magic(b"SIR0")
            self.info_start = f.read_UInt32()
            self.info_end = f.read_UInt32()
            self.unk = f.read_UInt32()
            self._read(f)

    def _read(self, f: EndianBinaryReader):
        """
        Overwrite this in children classes to read data.
        """
        pass
