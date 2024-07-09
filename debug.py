from elf.io import open_file

path = "tmp/20230918_rcc3387b_pfa_centr-tub-hoechst.ome.zarr"
key = "0/2"
with open_file(path, mode="r") as f:
    shape = f[key].shape
    print(shape)
