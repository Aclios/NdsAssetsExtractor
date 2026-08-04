from ndstools.fs import EndianBinaryReader
from ndstools.formats import File, NCLR, NCGR, NCER, ImageCanva
from pathlib import Path

from .theresia_pack import TheresiaPack


class TheresiaSpData(File):
    def read(self, f: EndianBinaryReader):
        self.entry_count = f.get_size() // 8
        self.entries = [TheresiaSpDataEntry(f, idx) for idx in range(self.entry_count)]

    def export_all(
        self,
        ncgr_pack: TheresiaPack,
        ncer_pack: TheresiaPack,
        nclr_pack: TheresiaPack,
        nanr_pack: TheresiaPack,
        out_dir: Path,
    ):
        out_dir.mkdir(exist_ok=True, parents=True)
        for entry in self.entries:
            entry.export_image(ncgr_pack, ncer_pack, nclr_pack, out_dir)


class TheresiaSpDataEntry:
    def __init__(self, f: EndianBinaryReader, idx: int):
        self.idx = idx
        self.ncgr_id = f.read_Int16()
        self.ncer_id = f.read_Int16()
        self.nclr_id = f.read_Int16()
        self.nanr_id = f.read_Int16()

    def export_image(
        self,
        ncgr_pack: TheresiaPack,
        ncer_pack: TheresiaPack,
        nclr_pack: TheresiaPack,
        out_dir: Path,
    ):
        if self.ncgr_id == -1:
            return
        ncgr_data = ncgr_pack.get_entry_data(self.ncgr_id)
        # TODO: handle that case properly, or at least try to understand wtf is going on?
        # Is this a decompression issue?
        if ncgr_data[0:4] != b"RGCN":
            return
        ncgr = NCGR(ncgr_pack.get_entry_data(self.ncgr_id))
        nclr = NCLR(nclr_pack.get_entry_data(self.nclr_id))
        ncer = NCER(ncer_pack.get_entry_data(self.ncer_id))
        canva = ImageCanva(bitmap=ncgr, palette=nclr, cell=ncer)
        canva.resolve()
        for i, image in enumerate(canva.images):
            if image:
                image.save(out_dir / f"{self.idx:04d}_{i:02d}.png")
