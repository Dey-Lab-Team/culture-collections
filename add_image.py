import argparse
import os
import shutil
import warnings
from typing import Any

import zarr  # pyright: ignore
from elf.io import open_file  # pyright: ignore
from mobie import add_image  # pyright: ignore
from mobie.metadata import add_source_to_dataset  # pyright: ignore
from mobie.utils import get_internal_paths  # pyright: ignore
from mobie.view_utils import create_view  # pyright: ignore
from tqdm import tqdm

from calc_contrast import get_contrast_limits
from update_project_on_github import pull
from utils import filter_for_ome_zarr

DEFAULT_COLORS_PER_CHANNEL = ["white", "green", "blue", "red"]
# TODO: read them from file name? or from csv?
DEFAULT_NAMES_PER_CHANNEL = ["channel-1", "channel-2", "channel-3", "channel-4"]


def remove_tmp_folder():
    if not os.path.exists("tmp"):
        return
    # maybe the safety if statement can be removed
    if len(os.listdir("tmp")) == 0:
        shutil.rmtree("tmp")


def _get_number_of_channels_from_zarr_file(zarr_file: str, zarr_key: str) -> int:
    # zarr_file needs to end with ome-zarr, otherwise elf misinterprets it
    with open_file(zarr_file, mode="r") as f:  # pyright: ignore
        assert isinstance(f, zarr.Group)
        print(zarr_file, zarr_key)
        num_channels = f[zarr_key].shape[1]  # pyright: ignore
        assert isinstance(num_channels, int)
    return num_channels


def _get_series_ids_from_zarr_file(zarr_file: str) -> list[int]:
    with open_file(zarr_file, mode="r") as f:  # pyright: ignore
        assert isinstance(f, zarr.Group)
        series_ids = f["OME"].attrs["series"]  # pyright: ignore
    assert isinstance(series_ids, list)
    return [int(id) for id in series_ids]  # pyright: ignore


def move_zarr_file_to_correct_place(
    zarr_file_path: str,
    mobie_project_directory: str,
    dataset_name: str,
    image_name: str,
    file_format: str,
    is_default_dataset: bool,
    dataset_folder: str,
) -> str:
    """More or less just to move data to correct place.
    Also takes care of creating the dataset correctly.

    Args:
        image_data_path (str): _description_
        mobie_project_directory (str): _description_
        dataset_name (str): _description_
        image_name (str): _description_
        file_format (str): _description_
        is_default_dataset (bool): _description_
    """
    add_image(
        input_path=zarr_file_path,
        input_key="0/0",
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
        skip_add_to_dataset=True,  # we add it manually
    )
    # for ome-zarr data and metadata paths are the same
    image_data_path, _ = get_internal_paths(
        dataset_folder=dataset_folder, file_format=file_format, name=image_name
    )
    return image_data_path


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
    image_base_name = os.path.basename(zarr_file).replace(".ome.zarr", "")
    # move file to correct place in MoBIE project
    image_data_path = move_zarr_file_to_correct_place(
        zarr_file_path=zarr_file,
        mobie_project_directory=mobie_project_directory,
        dataset_name=dataset_name,
        image_name=image_base_name,
        file_format=file_format,
        is_default_dataset=False,
        dataset_folder=dataset_folder,
    )
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
            add_source_to_dataset(
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
                    zarr_key=zarr_key,
                    channel=channel,
                )
            sources.append([channel_specific_name])
        # add one view to visualize all channels at once
        create_view(
            dataset_folder=dataset_folder,
            view_name=series_specific_name,
            sources=sources,
            display_settings=display_settings,
            display_group_names=DEFAULT_NAMES_PER_CHANNEL[:num_channels],
            menu_name="volumes",
            overwrite=True,
        )
    return image_data_path


def get_args():
    parser = argparse.ArgumentParser(description="Add ome-zarr images to MoBIE.")
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
        "--mobie_project_folder",
        "-p",
        default="data",
        type=str,
        help="Path to the MoBIE project folder.",
    )
    parser.add_argument(
        "--dataset_name",
        "-dsn",
        default="single_volumes",
        type=str,
        help="Name of the dataset to add the data to. "
        "If it does not exist, it will be created.",
    )
    parser.add_argument(
        "--calculate_contrast_limits",
        "-c",
        default=True,
        type=bool,
        help="Whether to calculate contrast limits for the image. "
        "Makes adding the image slower, but the image will look better.",
    )
    return parser.parse_args()


def main():
    args = get_args()
    is_pulled = pull()
    if not is_pulled:
        print(
            "Could not pull from GitHub. Please check the output and resolve "
            "any conflicts using git directly."
        )
        return
    input_files = filter_for_ome_zarr(args.input_data)
    for input_file in tqdm(input_files, desc="Adding images to MoBIE"):
        _ = add_multichannel_zarr_image(
            zarr_file=input_file,
            mobie_project_directory=args.mobie_project_folder,
            dataset_name=args.dataset_name,
            calculate_contrast_limits=args.calculate_contrast_limits,
        )
    remove_tmp_folder()


if __name__ == "__main__":
    main()
