
import argparse
import os
import subprocess
import shlex


def generate_zarr_file_path(input_file):
    file_name = os.path.split(input_file)[1].split('.')[0]
    file_name += ".ome.zarr"
    file_path = os.path.join(os.getcwd(), "tmp", file_name)
    return file_path


def convert_to_ome_zarr(input_file, putput_file):
    # use subprocess to call bioformats2raw
    cmd = f'bioformats2raw {input_file} {putput_file} ' \
        '--target-min-size 32 ' \
        '--scale-format-string "%2$d/"'
    cmd = shlex.split(cmd)
    subprocess.run(cmd)


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
    zarr_file = generate_zarr_file_path(args.input_file)
    convert_to_ome_zarr(args.input_file, zarr_file)


if __name__ == "__main__":
    main()
