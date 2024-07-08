import argparse
import os
import shlex
import subprocess

from tqdm import tqdm

from utils import filter_for_supported_file_formats


def generate_zarr_file_path(input_file_path: str):
    file_name = os.path.split(input_file_path)[1].split(".")[0]
    file_name += ".ome.zarr"
    output_file_path = os.path.join(os.getcwd(), "tmp", file_name)
    return output_file_path


def convert_to_ome_zarr(
    input_file_path: str,
    overwrite: bool = False,
    chunk_size: tuple[int, int, int] = (96, 96, 96),
) -> str:
    output_file_path = generate_zarr_file_path(input_file_path)
    # escape spaces in file paths
    input_file_path = input_file_path.replace(" ", "\\ ")
    output_file_path = output_file_path.replace(" ", "_")
    if os.path.exists(output_file_path) and not overwrite:
        return output_file_path
    # use subprocess to call bioformats2raw
    cmd = (
        f"bioformats2raw {input_file_path} {output_file_path} "
        "--target-min-size 32 "
        f"-z {chunk_size[0]} "
        f"-h {chunk_size[1]} "
        f"-w {chunk_size[2]}"
    )
    cmd = shlex.split(cmd)
    subprocess.run(cmd)
    return output_file_path


def get_args():
    parser = argparse.ArgumentParser(
        description="Convert images to ome-zarr. "
        "Converted files will be saved in a tmp folder."
    )
    parser.add_argument(
        "--input_data",
        "-f",
        nargs="+",
        type=str,
        help="Path to the input data. Can be either a single file, "
        "multiple files or a directory containing multiple files. "
        "Will be converted to ome-zarr by bioformats2raw.",
    )
    return parser.parse_args()


def main():
    args = get_args()
    input_files = filter_for_supported_file_formats(args.input_data)
    for input_file in tqdm(input_files, desc="Converting images to ome-zarr"):
        _ = convert_to_ome_zarr(input_file)


if __name__ == "__main__":
    main()
