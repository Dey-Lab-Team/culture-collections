import argparse
import os
import subprocess


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
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--file_path",
        "-f",
        nargs="+",
        type=str,
        help="Paths to files to upload to s3.",
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
    for path in args.file_path:
        upload_to_s3(
            relative_path_local=path,
            s3_prefix=args.s3_alias,
            bucket_name=args.bucket_name,
        )


if __name__ == "__main__":
    main()
