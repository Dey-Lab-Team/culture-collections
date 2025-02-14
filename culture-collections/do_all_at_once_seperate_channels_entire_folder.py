import argparse
import os

from do_all_at_once_seperate_channels import do_all_at_once_seperate_channels
from utils import filter_for_supported_file_formats


def group_files_by_volume(channel_files: list[str]) -> dict[str, list[str]]:
    volume_channel_file_map: dict[str, list[str]] = {}
    for file in channel_files:
        volume_name_components = os.path.basename(file).split(".")[0].split("_")
        volume_name = "_".join(
            volume_name_components[:-2] + volume_name_components[-1:]
        )
        if volume_name not in volume_channel_file_map:
            volume_channel_file_map[volume_name] = [file]

        else:
            volume_channel_file_map[volume_name].append(file)
    return volume_channel_file_map


def generate_view_names(
    volume_channel_file_map: dict[str, list[str]]
) -> dict[str, str]:
    view_name_map: dict[str, str] = {}
    for volume_name, channel_files in volume_channel_file_map.items():
        volume_name_components = volume_name.split("_")
        view_name = "_".join(volume_name_components[:-1]) + "_"
        for channel_file in channel_files:
            view_name += f"{os.path.basename(channel_file).split('_')[-2]}-"
        view_name = view_name[:-1] + "_" + volume_name_components[-1]
        view_name_map[volume_name] = view_name
    return view_name_map


def get_args():
    parser = argparse.ArgumentParser(
        description="Convert images to ome-zarr, add them to MoBIE, "
        "upload and sync everything. Special case for a directory with volumes having "
        "their channels in separate files."
    )
    parser.add_argument(
        "--directory",
        "-f",
        nargs="+",
        type=str,
        help="Path to the directory containing volumes with channels "
        "in individual files. Assumes that the files are named "
        "like `<...>_<channel>_<volumeNumber>.<extension>`.",
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
        "-dry", "--dry_run", action="store_true", help="Just list input files."
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
    channel_files = sorted(filter_for_supported_file_formats(args.directory))
    volume_channel_file_map = group_files_by_volume(channel_files)
    view_name_map = generate_view_names(volume_channel_file_map)
    if args.dry_run:
        print(f"volume_channel_file_map (len = {len(volume_channel_file_map)}):")
        print(volume_channel_file_map)
        print()
        print(f"view_name_map (len = {len(view_name_map)}):")
        print(view_name_map)
        print()
        return
    for volume_name, channel_files in volume_channel_file_map.items():
        do_all_at_once_seperate_channels(
            channel_files=channel_files,
            view_name=view_name_map[volume_name],
            dataset_name=args.dataset_name,
            s3_alias=args.s3_alias,
            tmp_dir=args.tmp_dir,
        )


if __name__ == "__main__":
    main()
