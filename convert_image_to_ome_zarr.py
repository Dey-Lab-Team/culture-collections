import argparse
import os
import shlex
import subprocess


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
    if os.path.exists(output_file_path) and not overwrite:
        return output_file_path
    # escape spaces in file paths
    input_file_path = input_file_path.replace(" ", "\\ ")
    output_file_path = output_file_path.replace(" ", "_")
    # use subprocess to call bioformats2raw
    cmd = (
        f"bioformats2raw {input_file_path} {output_file_path} "
        "--target-min-size 32 "
        '--scale-format-string "%2$d/" '
        f"-z {chunk_size[0]} "
        f"-h {chunk_size[1]} "
        f"-w {chunk_size[2]}"
    )
    cmd = shlex.split(cmd)
    subprocess.run(cmd)
    return output_file_path


def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--input_file",
        "-f",
        type=str,
        help="Path to the input file. Must be a zarr file converted by"
        "bioformats2raw.",
    )
    return parser.parse_args()


def main():
    args = get_args()
    _ = convert_to_ome_zarr(args.input_file)


if __name__ == "__main__":
    main()
