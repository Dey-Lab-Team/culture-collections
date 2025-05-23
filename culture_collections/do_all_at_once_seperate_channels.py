import argparse
import os

from tqdm import tqdm

from culture_collections.add_image import remove_local_image_folder, remove_tmp_folder
from culture_collections.add_image_seperate_channels import (
    add_image_with_seperate_channels,
)
from culture_collections.convert_image_to_ome_zarr import convert_to_ome_zarr
from culture_collections.do_all_at_once import update_remote_project
from culture_collections.scrape_supported_file_types_from_web import is_format_supported
from culture_collections.update_project_on_github import pull


def do_all_at_once_seperate_channels(
    channel_files: list[str],
    view_name: str,
    mobie_project_directory: str = "data",
    dataset_name: str = "single_volumes",
    bucket_name: str = "culture-collections",
    s3_alias: str = "culcol_s3_rw",
    tmp_dir: str = "tmp",
):
    # convert images to ome-zarr
    channel_zarr_file_paths: list[str] = []
    for file_path in tqdm(channel_files, desc="Converting files"):
        zarr_file_path = convert_to_ome_zarr(file_path, tmp_dir=tmp_dir)
        channel_zarr_file_paths.append(zarr_file_path)

    # add images to MoBIE project
    is_pulled = pull()
    if not is_pulled:
        print(
            "Could not pull from GitHub. Please check the output and resolve"
            "any conflicts using git directly."
        )
        return

    source_name_of_volumes = add_image_with_seperate_channels(
        channel_zarr_files=channel_zarr_file_paths,
        mobie_project_directory=mobie_project_directory,
        dataset_name=dataset_name,
        view_name=view_name,
    )
    remove_tmp_folder(tmp_dir=tmp_dir)

    update_remote_project(
        image_data_paths=source_name_of_volumes,
        mobie_project_directory=mobie_project_directory,
        bucket_name=bucket_name,
        s3_alias=s3_alias,
    )

    remove_local_image_folder(
        mobie_project_directory=mobie_project_directory, dataset_name=dataset_name
    )


def check_input_data(channel_files: list[str]):
    for path in channel_files:
        if not os.path.exists(path):
            raise ValueError(f"{path} does not exist.")
        if not is_format_supported(path):
            raise ValueError(f"{path} is not a supported file format.")
    return channel_files


def get_args():
    parser = argparse.ArgumentParser(
        description="Convert images to ome-zarr, add them to MoBIE, "
        "upload and sync everything. Special case where channels are in separate files."
    )
    parser.add_argument(
        "--channel_files",
        "-f",
        nargs="+",
        type=str,
        help="Path to the files containing individual channels "
        "provided in the correct order.",
    )
    parser.add_argument(
        "--view_name",
        "-n",
        type=str,
        help="Name of the entire image when you want to select it in MoBIE.",
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
        "--tmp_dir",
        "-td",
        type=str,
        default="tmp",
        help="Path to the directory where the ome-zarr files will be saved before they "
        "are moved to the project.",
    )
    # just to allow another input like 'test' to debug things
    parser.add_argument("--dataset_name", "-dsn", default="single_volumes", type=str)
    args = parser.parse_args()
    return args


def main():
    # get input arguments
    args = get_args()
    channel_files = check_input_data(args.channel_files)
    do_all_at_once_seperate_channels(
        channel_files=channel_files,
        view_name=args.view_name,
        dataset_name=args.dataset_name,
        s3_alias=args.s3_alias,
        tmp_dir=args.tmp_dir,
    )


if __name__ == "__main__":
    main()
