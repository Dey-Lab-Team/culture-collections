import argparse
import os
import shutil
import xml.etree.ElementTree as ET
from typing import Any

import mobie

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


def get_number_of_channels_from_ome_metadata(xml_file: str) -> int:
    tree = ET.parse(xml_file)
    root = tree.getroot()
    # all the tags have this weird prefix
    channel_tag = "{http://www.openmicroscopy.org/Schemas/OME/2016-06}Channel"
    channels = list(root.iter(channel_tag))
    # potential alternative:
    # root[1][2].findall("{http://www.openmicroscopy.org/Schemas/OME/2016-06}Channel")
    # other alternative:
    # open data and read number of channels from shape
    return len(channels)


def add_multichannel_zarr_image(
    zarr_file: str,
    zarr_key: str,
    mobie_project_directory: str,
    dataset_name: str,
    is_default_dataset: bool = False,
    calculate_contrast_limits: bool = True,
):
    file_format = "ome.zarr"
    image_name = os.path.basename(zarr_file).split(".")[0]
    xml_file = os.path.join(zarr_file, "OME/METADATA.ome.xml")
    num_channels = get_number_of_channels_from_ome_metadata(xml_file)
    sources = [f"{image_name}_ch{channel}" for channel in range(num_channels)]
    # add image volume once (by this added as a source, but never used as one)
    # just move data, don't copy, apparently internally only changes
    # pointer not moving a single byte (as long as on same filesystem),
    # so it should not matter if we call this multiple times (for each
    # channel)
    mobie.add_image(
        input_path=zarr_file,
        input_key=zarr_key,
        root=mobie_project_directory,
        dataset_name=dataset_name,
        image_name=image_name,
        file_format=file_format,
        view={},  # manually add view at the end
        is_default_dataset=is_default_dataset,
        move_only=True,
        resolution=None,  # not needed since we just move data
        chunks=None,  # not needed since we just move data
        scale_factors=None,  # not needed since we just move data
    )
    # add each channel as a seperate source
    for channel, channel_name in enumerate(sources):
        dataset_folder = os.path.join(mobie_project_directory, dataset_name)
        image_data_path, image_metadata_path = mobie.utils.get_internal_paths(
            dataset_folder, file_format, image_name
        )
        mobie.metadata.add_source_to_dataset(
            dataset_folder=dataset_folder,
            source_type="image",
            source_name=channel_name,
            image_metadata_path=image_metadata_path,
            view={},
            channel=channel,
        )
    # set color and contrast limits for each channel
    display_settings: list[dict[str, Any]] = [
        {"color": DEFAULT_COLORS_PER_CHANNEL[channel]}
        for channel in range(num_channels)
    ]
    if calculate_contrast_limits:  # flag since this can take a few seconds
        for channel, channel_settings in enumerate(display_settings):
            channel_settings["contrastLimits"] = get_contrast_limits(
                image_data_path, channel  # should be the same for all channels
            )
    # add one view to visualize all channels at once
    mobie.view_utils.create_view(
        dataset_folder=dataset_folder,
        view_name=image_name,
        sources=[[source] for source in sources],
        display_settings=display_settings,
        display_group_names=DEFAULT_NAMES_PER_CHANNEL[:num_channels],
        menu_name="volumes",
        overwrite=True,
    )
    return image_name


def add_image_with_seperate_channels(
    channel_zarr_files: list[str],
    channel_zarr_keys: list[str],
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
    for channel, (zarr_file, zarr_key) in enumerate(
        zip(channel_zarr_files, channel_zarr_keys)
    ):
        channel_name = os.path.basename(zarr_file).split(".")[0]
        channel_names.append(channel_name)
        # add image volume once (by this added as a source, but never used as one)
        # just move data, don't copy, apparently internally only changes
        # pointer not moving a single byte (as long as on same filesystem),
        # so it should not matter if we call this multiple times (for each
        # channel)
        mobie.add_image(
            input_path=zarr_file,
            input_key=zarr_key,
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
        )
        if calculate_contrast_limits:  # flag since this can take a few seconds
            image_data_path, _ = mobie.utils.get_internal_paths(
                dataset_folder, file_format, channel_name
            )
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
        "--input_key",
        "-k",
        default="0",
        type=str,
        help="Key of the data inside the input file.",
    )
    parser.add_argument(
        "--mobie_project_folder",
        "-p",
        default="data",  # or os.getcwd()? or even hardcode?
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
        "--is_default_dataset",
        "-i",
        default=False,
        type=bool,
        help="Whether this dataset should be the default one.",
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
        args.input_key,
        args.mobie_project_folder,
        args.dataset_name,
        args.is_default_dataset,
        args.calculate_contrast_limits,
    )
    remove_tmp_folder()


if __name__ == "__main__":
    main()
