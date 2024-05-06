import argparse
import os
from typing import Any

from mobie.metadata import add_source_to_dataset  # pyright: ignore
from mobie.view_utils import create_view  # pyright: ignore

from add_image_to_MoBIE_project import (
    DEFAULT_COLORS_PER_CHANNEL,
    DEFAULT_NAMES_PER_CHANNEL,
    move_zarr_file_to_correct_place,
    remove_tmp_folder,
)
from calc_contrast import get_contrast_limits
from update_project_on_github import pull


def add_image_with_seperate_channels(
    channel_zarr_files: list[str],
    mobie_project_directory: str,
    dataset_name: str,
    view_name: str,
    calculate_contrast_limits: bool = True,
):
    file_format = "ome.zarr"
    dataset_folder = os.path.join(mobie_project_directory, dataset_name)
    image_data_paths: list[str] = []
    num_channels = len(channel_zarr_files)
    # create color and contrast limits for each channel
    display_settings: list[dict[str, Any]] = [
        {"color": DEFAULT_COLORS_PER_CHANNEL[channel]}
        for channel in range(num_channels)
    ]
    # loop over channels, add each as a seperate source
    sources: list[list[str]] = []
    for channel, zarr_file in enumerate(channel_zarr_files):
        channel_name = os.path.basename(zarr_file).split(".")[0]
        # move file to correct place in MoBIE project
        image_data_path = move_zarr_file_to_correct_place(
            zarr_file_path=zarr_file,
            mobie_project_directory=mobie_project_directory,
            dataset_name=dataset_name,
            image_name=channel_name,
            file_format=file_format,
            is_default_dataset=False,
            dataset_folder=dataset_folder,
        )
        image_data_paths.append(image_data_path)
        # MoBIE can't handle multi-series zarr files, so we need to
        # add the series name to the path
        image_data_path_with_series = image_data_path + "/0"
        add_source_to_dataset(
            dataset_folder=dataset_folder,
            source_type="image",
            source_name=channel_name,
            image_metadata_path=image_data_path_with_series,
            file_format=file_format,
            view={},
            # channel=0,  # TODO: or no channel?
        )
        if calculate_contrast_limits:  # flag since this can take a few seconds
            display_settings[channel]["contrastLimits"] = get_contrast_limits(
                zarr_file_path=image_data_path, zarr_key="0/0", channel=0
            )
        sources.append([channel_name])
    # add one view to visualize all channels at once
    create_view(
        dataset_folder=dataset_folder,
        view_name=view_name,
        sources=sources,
        display_settings=display_settings,
        display_group_names=DEFAULT_NAMES_PER_CHANNEL[:num_channels],
        menu_name="volumes",
        overwrite=True,
    )
    return image_data_paths


def get_args():
    parser = argparse.ArgumentParser()
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
        "-v",
        type=str,
        help="Name of the entire image when you want to select it in MoBIE.",
    )
    parser.add_argument(
        "--mobie_project_folder",
        "-p",
        default="data",
        type=str,
        help="Path to the MoBIE project folder.",
    )
    parser.add_argument(
        "--dataset_name",
        "-d",
        default="single_volumes",
        type=str,
        help="Name of the dataset to add the data to."
        "If it does not exist, it will be created.",
    )
    parser.add_argument(
        "--calculate_contrast_limits",
        "-c",
        default=True,
        type=bool,
        help="Whether to calculate contrast limits for the image."
        "Makes adding the image slower, but the image will look better.",
    )
    return parser.parse_args()


def main():
    args = get_args()
    is_pulled = pull()
    if not is_pulled:
        print(
            "Could not pull from GitHub. Please check the output and resolve"
            "any conflicts using git directly."
        )
        return
    _ = add_image_with_seperate_channels(
        channel_zarr_files=args.channel_files,
        mobie_project_directory=args.mobie_project_folder,
        dataset_name=args.dataset_name,
        view_name=args.view_name,
        calculate_contrast_limits=args.calculate_contrast_limits,
    )
    remove_tmp_folder()


if __name__ == "__main__":
    main()
