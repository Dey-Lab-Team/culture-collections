import argparse
import os

from mobie.metadata import (
    add_remote_project_metadata,
    read_dataset_metadata,
    upload_source,
)
from tqdm import tqdm

from add_image_to_MoBIE_project import add_multichannel_zarr_image, remove_tmp_folder
from convert_image_to_ome_zarr import convert_to_ome_zarr
from scrape_supported_file_types_from_web import is_format_supported
from update_project_on_github import pull, stage_all_and_commit, sync_with_remote


def check_input_data(input_data: str):
    # TODO: is there a better way than the comma-seperated list?
    # regex?
    if "," in input_data:  # comma-seperated list
        files = input_data.split(",")
        files = [file for file in files if is_format_supported(file)]
    elif is_format_supported(input_data):  # single file
        files = [input_data] if is_format_supported(input_data) else []
    else:  # directory
        assert os.path.isdir(input_data)
        files = [
            os.path.join(input_data, file)
            for file in os.listdir(input_data)
            if is_format_supported(file, warn=True)
        ]
    return files


def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--input_data",
        "-d",
        type=str,
        help="Path to the input data. Can be either a single file"
        "(identified by a dot in the file name),"
        "a comma-seperated (no spaces) list of files"
        "or a directory containing multiple files.",
    )
    parser.add_argument(
        "--s3_alias",
        "-p",
        default="culcol_s3_rw",
        type=str,
        help="Prefix of the s3 bucket."
        "You defined this when you added the s3 to the minio"
        "client as an alias.",
    )
    parser.add_argument(
        "--overwrite",
        "-o",
        default=False,
        type=bool,
        help="Whether to overwrite existing ome.zarr files in tmp folder.",
    )
    args = parser.parse_args()
    input_data = check_input_data(args.input_data)
    args.input_data = input_data
    return args


def main():
    # get input arguments
    args = get_args()
    mobie_project_directory = "data"
    dataset_name = "single_volumes"
    bucket_name = "culture-collections/data"

    # convert images to ome-zarr
    zarr_file_paths: list[str] = []
    pbar = tqdm(total=len(args.input_data))
    for file_path in args.input_data:
        pbar.set_description(f"Converting files, currently {file_path}")
        zarr_file_path = convert_to_ome_zarr(file_path)
        zarr_file_paths.append(zarr_file_path)
        pbar.update(1)
    pbar.close()

    # add images to MoBIE project
    is_pulled = pull()
    if not is_pulled:
        print(
            "Could not pull from GitHub. Please check the output and resolve"
            "any conflicts using git directly."
        )
        return
    source_name_of_volumes: list[str] = []
    pbar = tqdm(total=len(zarr_file_paths))
    for zarr_file_path in zarr_file_paths:
        file_name = os.path.split(zarr_file_path)[-1].split(".")[0]
        pbar.set_description(f"Add images to MoBIE, currently {file_name}")
        source_name_of_volume = add_multichannel_zarr_image(
            zarr_file_path,
            zarr_key="0",
            mobie_project_directory=mobie_project_directory,
            dataset_name=dataset_name,
        )
        source_name_of_volumes.append(source_name_of_volume)
        pbar.update(1)
    pbar.close()
    remove_tmp_folder()

    # add s3 metadata
    print("Adding s3 metadata...")
    add_remote_project_metadata(
        root=mobie_project_directory,
        bucket_name=bucket_name,
        service_endpoint="https://s3.embl.de",
    )

    # upload images to s3
    dataset_folder = os.path.join(mobie_project_directory, dataset_name)
    dataset_metadata = read_dataset_metadata(dataset_folder)
    pbar = tqdm(total=len(source_name_of_volumes), leave=True)
    for source_name_of_volume in source_name_of_volumes:
        pbar.set_description(f"Upload data to s3, currently {source_name_of_volume}")
        source_metadata = dataset_metadata["sources"][source_name_of_volume]
        upload_source(
            dataset_folder=dataset_folder,
            metadata=source_metadata,
            data_format="ome.zarr",
            bucket_name=bucket_name,
            s3_prefix=args.s3_alias,
        )
        pbar.update(1)
    pbar.close()

    # sync metadata with GitHub
    print("Syncing with GitHub...")
    stage_all_and_commit()
    is_synced = sync_with_remote()

    # let user know we are done
    if is_synced:
        print("All done!")
    else:
        print(
            "Some errors occured while syncing with GitHub (see above)."
            "Please check the output and resolve any conflicts"
            "using git directly."
        )


if __name__ == "__main__":
    main()


# TODO:
# decide on default view? thumbnail for each dataset?
# other datasets? per species? grid views?

# change all_volumes to single_volumes

# add subprocess to install minio client?
# or is this possible in docker, then just add the alias
# what about git in docker?
# how to share keys?
