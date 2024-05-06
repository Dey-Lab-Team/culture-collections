import argparse
import os
import shutil
from typing import Any

import mobie
from elf.io import open_file

from calc_contrast import get_contrast_limits
from update_project_on_github import pull

DEFAULT_COLORS_PER_CHANNEL = ["white", "green", "blue", "red"]
# TODO: read them from file name?
DEFAULT_NAMES_PER_CHANNEL = ["channel-1", "channel-2", "channel-3", "channel-4"]


def remove_tmp_folder():
    if not os.path.exists("tmp"):
        return
    # maybe the safety if statement can be removed
    if len(os.listdir("tmp")) == 0:
        shutil.rmtree("tmp")


def _get_number_of_channels_from_zarr_file(zarr_file: str, zarr_key: str) -> int:
    # zarr_file needs to end with ome-zarr, otherwise elf misinterprets it
    with open_file(zarr_file, mode="r") as f:
        num_channels = f[zarr_key].shape[1]
        assert isinstance(num_channels, int)
    return num_channels


def _get_series_ids_from_zarr_file(zarr_file: str) -> list[int]:
    with open_file(zarr_file, mode="r") as f:
        series_ids = f["OME"].attrs["series"]
    return [int(id) for id in series_ids]


# dimensions in ome-zarr file are: [series, resolution, t, c, z, y, x]
# series and resolution are groups, the rest arrays
def add_multichannel_zarr_image(
    zarr_file: str,
    mobie_project_directory: str,
    dataset_name: str,
    calculate_contrast_limits: bool = True,
):
    file_format = "ome.zarr"
    dataset_folder = os.path.join(mobie_project_directory, dataset_name)
    image_base_name = os.path.basename(zarr_file).split(".")[0]
    # for ome-zarr data and metadata path are the same
    image_data_path, _ = mobie.utils.get_internal_paths(
        dataset_folder=dataset_folder, file_format=file_format, name=image_base_name
    )
    print(image_data_path)
    exit()
    assert isinstance(image_data_path, str)
    # move file to correct place in MoBIE project instead of calling add_image
    shutil.move(zarr_file, image_data_path)
    # loop over series, handle each as a seperate volume (i.e. giving it a view)
    series_ids = _get_series_ids_from_zarr_file(image_data_path)
    for series_id in series_ids:
        # use correct series and highe
        zarr_key = f"{series_id}/0"
        series_name = "" if len(series_ids) == 1 else f"_series{series_id:02}"
        series_specific_name = image_base_name + series_name
        # MoBIE can't handle multi-series zarr files, so we need to
        # add the series name to the path
        series_specific_data_path = image_data_path + f"/{series_id}"
        # set color and contrast limits for each channel
        num_channels = _get_number_of_channels_from_zarr_file(
            zarr_file=image_data_path, zarr_key=zarr_key
        )
        display_settings: list[dict[str, Any]] = [
            {"color": DEFAULT_COLORS_PER_CHANNEL[channel]}
            for channel in range(num_channels)
        ]
        # loop over channels, add each as a seperate source
        sources: list[list[str]] = []
        for channel, channel_settings in enumerate(display_settings):
            channel_specific_name = series_specific_name + f"_ch{channel}"
            mobie.metadata.add_source_to_dataset(
                dataset_folder=dataset_folder,
                source_type="image",
                source_name=channel_specific_name,
                image_metadata_path=series_specific_data_path,
                file_format=file_format,
                view={},
                channel=channel,
            )
            if calculate_contrast_limits:  # flag since this can take a few seconds
                channel_settings["contrastLimits"] = get_contrast_limits(
                    # should be the same for all channels
                    zarr_file_path=image_data_path,
                    channel=channel,
                    zarr_key=zarr_key,
                )
            sources.append([channel_specific_name])
        # add one view to visualize all channels at once
        mobie.view_utils.create_view(
            dataset_folder=dataset_folder,
            view_name=series_specific_name,
            sources=sources,
            display_settings=display_settings,
            display_group_names=DEFAULT_NAMES_PER_CHANNEL[:num_channels],
            menu_name="volumes",
            overwrite=True,
        )
    return image_data_path


def add_image_with_seperate_channels(
    channel_zarr_files: list[str],
    mobie_project_directory: str,
    dataset_name: str,
    view_name: str,
    is_default_dataset: bool = False,
    calculate_contrast_limits: bool = True,
):
    file_format = "ome.zarr"
    num_channels = len(channel_zarr_files)
    dataset_folder = os.path.join(mobie_project_directory, dataset_name)
    # create color and contrast limits for each channel
    display_settings: list[dict[str, Any]] = [
        {"color": DEFAULT_COLORS_PER_CHANNEL[channel]}
        for channel in range(num_channels)
    ]
    channel_names: list[str] = []
    for channel, zarr_file in enumerate(channel_zarr_files):
        channel_name = os.path.basename(zarr_file).split(".")[0]
        channel_names.append(channel_name)
        # add image volume once (by this added as a source, but never used as one)
        # just move data, don't copy, apparently internally only changes
        # pointer not moving a single byte (as long as on same filesystem),
        # so it should not matter if we call this multiple times (for each
        # channel)
        mobie.add_image(
            input_path=zarr_file,
            input_key=0,
            root=mobie_project_directory,
            dataset_name=dataset_name,
            image_name=channel_name,
            file_format=file_format,
            view={},  # manually add view at the end
            is_default_dataset=is_default_dataset,
            move_only=True,
            resolution=None,  # not needed since we just move data
            chunks=None,  # not needed since we just move data
            scale_factors=None,  # not needed since we just move data
            skip_add_to_dataset=True,  # add one source per channel manually
        )
        # for ome-zarr data and metadata path are the same
        image_data_path, _ = mobie.utils.get_internal_paths(
            dataset_folder, file_format, channel_name
        )
        assert isinstance(image_data_path, str)
        # MoBIE can't handle multi-series zarr files, so we need to
        # add the series name to the path
        image_data_path = image_data_path + "/0"
        mobie.metadata.add_source_to_dataset(
            dataset_folder=dataset_folder,
            source_type="image",
            source_name=channel_name,
            image_metadata_path=image_data_path,
            view={},
            channel=channel,
        )
        if calculate_contrast_limits:  # flag since this can take a few seconds
            display_settings[channel]["contrastLimits"] = get_contrast_limits(
                zarr_file_path=image_data_path, channel=0
            )
    # add one view to visualize all channels at once
    mobie.view_utils.create_view(
        dataset_folder=dataset_folder,
        view_name=view_name,
        sources=[[source] for source in channel_names],
        display_settings=display_settings,
        display_group_names=DEFAULT_NAMES_PER_CHANNEL[:num_channels],
        menu_name="volumes",
        overwrite=True,
    )
    return channel_names


def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--input_file",
        "-f",
        type=str,
        help="Path to the input file. Must be a zarr file converted by"
        "bioformats2raw.",
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
    _ = add_multichannel_zarr_image(
        args.input_file,
        args.mobie_project_folder,
        args.dataset_name,
    )
    remove_tmp_folder()


if __name__ == "__main__":
    main()
