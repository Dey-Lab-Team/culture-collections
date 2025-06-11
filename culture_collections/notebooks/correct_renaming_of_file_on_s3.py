import os
import subprocess
from concurrent.futures import ThreadPoolExecutor

from tqdm import tqdm


def main():
    with open(os.path.dirname(__file__) + "/file_name_map.csv", "r") as f:
        file_name_map = {
            line.split(",")[0].strip(): line.split(",")[1].strip()
            for line in f.readlines()
        }

    # sort for the ones that did not work
    p = "/home/hellgoth/culture-collections/data/single_volumes/images/ome-zarr/"
    new_dict: dict[str, str] = {}
    for old_file_name, new_file_name in file_name_map.items():
        if old_file_name + ".ome.zarr" in os.listdir(p + new_file_name + ".ome.zarr/"):
            new_dict[old_file_name] = new_file_name
    print("Number of files that did not work:", len(new_dict))

    pbar = tqdm(
        total=len(new_dict),
        desc="Renaming files on S3",
        unit="file",
    )

    def rename_file(old_file_name: str, new_file_name: str):
        cmd = [
            "mc",
            "mv",
            "-r",
            "culcol_s3_rw/culture-collections/data/single_volumes/images/ome-zarr/"
            + f"{new_file_name}.ome.zarr/{old_file_name}.ome.zarr/",
            "culcol_s3_rw/culture-collections/data/single_volumes/images/ome-zarr/"
            + f"{new_file_name}.ome.zarr/",
        ]
        p = subprocess.Popen(cmd)
        p.wait()
        pbar.update(1)

    with ThreadPoolExecutor(4) as ex:
        ex.map(
            rename_file,
            new_dict.keys(),
            new_dict.values(),
        )


if __name__ == "__main__":
    main()
