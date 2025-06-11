import subprocess

from tqdm import tqdm


def main():
    with open("file_name_map.csv", "r") as f:
        new_file_names = [line.split(",")[1].strip() for line in f.readlines()]

    processes: list[subprocess.Popen] = []  # type: ignore
    for new_file_name in new_file_names:
        cmd = [
            "mc",
            "mv",
            "-r",
            "culcol_s3_rw/culture-collections/data/single_volumes/images/ome-zarr/"
            + f"{new_file_name}.ome.zarr/{new_file_name}.zarr/",
            "culcol_s3_rw/culture-collections/data/single_volumes/images/ome-zarr/"
            + f"{new_file_name}.ome.zarr/",
        ]
        processes.append(subprocess.Popen(cmd))  # type: ignore

    for p in tqdm(processes):  # type: ignore
        p.wait()


if __name__ == "__main__":
    main()
