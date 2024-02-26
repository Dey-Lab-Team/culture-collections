import argparse

from mobie.metadata import read_dataset_metadata, upload_source


def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--dataset_folder",
        "-d",
        default="data/single_volumes",
        type=str,
        help="Path to the MoBIE dataset folder the source belongs to.",
    )
    parser.add_argument(
        "--source", "-s", type=str, help="Name of the source to upload."
    )
    parser.add_argument(
        "--s3_alias",
        "-p",
        default="culcol_s3_rw",
        type=str,
        help="Prefix of the s3 bucket.",
    )
    return parser.parse_args()


def main():
    args = get_args()
    dataset_metadata = read_dataset_metadata(args.dataset_folder)
    source_metadata = dataset_metadata["sources"][args.source]
    upload_source(
        dataset_folder=args.dataset_folder,
        metadata=source_metadata,
        data_format="ome.zarr",
        bucket_name="culture-collections/data",
        s3_prefix=args.s3_alias,
    )


if __name__ == "__main__":
    main()
