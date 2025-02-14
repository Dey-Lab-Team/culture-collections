import argparse
import os
import subprocess

from tqdm import tqdm

from .utils import filter_for_ome_zarr


def upload_to_s3(
    relative_path_local: str,
    s3_prefix: str,
    bucket_name: str,
):
    assert os.path.exists(relative_path_local)
    cmd = [
        "mc",
        "cp",
        "-r",
        f"{relative_path_local}/",
        f"{s3_prefix}/{bucket_name}/{relative_path_local}/",
    ]
    subprocess.run(cmd)


def get_args():
    parser = argparse.ArgumentParser(description="Upload ome-zarr files to s3.")
    parser.add_argument(
        "--input_data",
        "-f",
        nargs="+",
        type=str,
        help="Path to the input data. Can be either a single file, "
        "multiple files or a directory containing multiple files. "
        "Only ome-zarr files are supported.",
    )
    parser.add_argument(
        "--s3_alias",
        "-p",
        default="culcol_s3_rw",
        type=str,
        help="Prefix of the s3 bucket. "
        "You defined this when you added the s3 to the minio "
        "client as an alias.",
    )

    parser.add_argument(
        "--bucket_name",
        "-b",
        default="culture-collections",
        type=str,
        help="Name of the bucket to upload to.",
    )
    return parser.parse_args()


def main():
    args = get_args()
    input_files = filter_for_ome_zarr(args.input_data)
    for path in tqdm(input_files, desc="Uploading to s3"):
        upload_to_s3(
            relative_path_local=path,
            s3_prefix=args.s3_alias,
            bucket_name=args.bucket_name,
        )


if __name__ == "__main__":
    main()
