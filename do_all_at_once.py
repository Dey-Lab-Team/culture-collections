import argparse
import warnings

from mobie.metadata import add_remote_project_metadata  # pyright: ignore
from tqdm import tqdm

from add_image import add_multichannel_zarr_image, remove_tmp_folder
from convert_image_to_ome_zarr import convert_to_ome_zarr
from update_project_on_github import pull, stage_all_and_commit, sync_with_remote
from upload_data_to_s3 import upload_to_s3
from utils import filter_for_supported_file_formats


def update_remote_project(
    image_data_paths: list[str],
    mobie_project_directory: str,
    bucket_name: str,
    s3_alias: str,
):
    # add s3 metadata
    print("Adding s3 metadata...")
    add_remote_project_metadata(
        root=mobie_project_directory,
        bucket_name=bucket_name + "/data",
        service_endpoint="https://s3.embl.de",
    )

    # upload images to s3
    for data_path in tqdm(image_data_paths, desc="Uploading data to s3"):
        upload_to_s3(
            relative_path_local=data_path,
            s3_prefix=s3_alias,
            bucket_name=bucket_name,
        )

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


def do_all_at_once(
    input_files: list[str],
    mobie_project_directory: str = "data",
    dataset_name: str = "single_volumes",
    bucket_name: str = "culture-collections",
    s3_alias: str = "culcol_s3_rw",
):
    # convert images to ome-zarr
    zarr_file_paths: list[str] = []
    for file_path in tqdm(input_files, desc="Converting files"):
        zarr_file_path = convert_to_ome_zarr(file_path)
        zarr_file_paths.append(zarr_file_path)

    # add images to MoBIE project
    is_pulled = pull()
    if not is_pulled:
        print(
            "Could not pull from GitHub. Please check the output and resolve"
            "any conflicts using git directly."
        )
        return
    source_name_of_volumes: list[str] = []
    for zarr_file_path in tqdm(zarr_file_paths, desc="Adding images to MoBIE"):
        # ignore useless spamy warning from mobie
        with warnings.catch_warnings():
            warnings.filterwarnings("ignore")
            source_name_of_volume = add_multichannel_zarr_image(
                zarr_file_path,
                mobie_project_directory=mobie_project_directory,
                dataset_name=dataset_name,
            )
            source_name_of_volumes.append(source_name_of_volume)
    remove_tmp_folder()

    update_remote_project(
        image_data_paths=source_name_of_volumes,
        mobie_project_directory=mobie_project_directory,
        bucket_name=bucket_name,
        s3_alias=s3_alias,
    )


def get_args():
    parser = argparse.ArgumentParser(
        description="Convert images to ome-zarr, add them to MoBIE, "
        "upload and sync everything."
    )
    parser.add_argument(
        "--input_data",
        "-f",
        nargs="+",
        type=str,
        help="Path to the input data. Can be either a single file, "
        "multiple files or a directory containing multiple files.",
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
    # just to allow another input like 'test' to debug things
    parser.add_argument("--dataset_name", "-dsn", default="single_volumes", type=str)
    args = parser.parse_args()
    return args


def main():
    # get input arguments
    args = get_args()
    input_files = filter_for_supported_file_formats(args.input_data)
    do_all_at_once(
        input_files=input_files, dataset_name=args.dataset_name, s3_alias=args.s3_alias
    )


if __name__ == "__main__":
    main()


# TODO:
# decide on default view? thumbnail for each dataset?
# other datasets? per species? grid views?

# add subprocess to install minio client?
# or is this possible in docker, then just add the alias
# what about git in docker?
# how to share keys?
