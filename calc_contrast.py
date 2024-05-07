import argparse
from typing import Any

import numpy as np
import numpy.typing as npt
from elf.io import open_file  # pyright: ignore


def calc_contrast_limits_fiji_style(image: npt.NDArray[Any]) -> list[int]:
    # adapted from
    # https://forum.image.sc/t/macro-for-image-adjust-brightness-contrast-auto-button/37157/5
    min_value = image.min()
    max_value = image.max()
    histogram = np.histogram(image, bins=256, range=(min_value, max_value))[0]
    bin_size = (max_value - min_value) / 256
    voxel_count = image.size
    const_auto_threshold = 5000
    threshold = int(voxel_count / const_auto_threshold)
    limit = voxel_count / 10

    i = -1  # find the first bin with a count > threshold
    found = False
    while not found and i <= 255:
        i += 1
        count = histogram[i]
        found = threshold < count < limit
    histo_min = i
    i = 256  # find the last bin with a count > threshold
    while not found and i > 0:
        i -= 1
        count = histogram[i]
        found = threshold < count < limit
    histo_max = i

    # if we found proper bins, compute the min and max values
    if histo_max > histo_min:
        # added the min and max calls, because sometimes the new max_value
        # was higher than the old one, not sure if this is a problem
        min_value = max(int(min_value + histo_min * bin_size), min_value)
        max_value = min(int(min_value + histo_max * bin_size), max_value)

    # otherwise, just return the min and max of the image
    return [min_value, max_value]


def calc_contrast_limits_percentile(
    image: npt.NDArray[Any], percentile: tuple[float, float] = (0.1, 99.9)
) -> list[int]:
    lower_bound = np.percentile(image, percentile[0])
    upper_bound = np.percentile(image, percentile[1])
    return [int(lower_bound), int(upper_bound)]


def get_contrast_limits(
    zarr_file_path: str,
    zarr_key: str,
    channel: int,
    func: str = "percentile",
    central_slice: bool = True,
) -> list[int]:
    zarr_file = open_file(zarr_file_path, mode="r")  # pyright: ignore
    zarr_array = zarr_file[zarr_key]  # pyright: ignore
    if central_slice:
        image = zarr_array[0, channel, zarr_array.shape[2] // 2]  # pyright: ignore
    else:
        image = zarr_array[0, channel]  # pyright: ignore
    if func == "percentile":
        contrast_limits = calc_contrast_limits_percentile(image)  # pyright: ignore
    elif func == "fiji":
        contrast_limits = calc_contrast_limits_fiji_style(image)  # pyright: ignore
    else:
        raise ValueError(f"Unknown function {func}")
    return contrast_limits


def get_args():
    parser = argparse.ArgumentParser(description="Calculate and print contrast limits.")
    parser.add_argument(
        "--input_file",
        "-f",
        type=str,
        help="Path to the input file. Must be a ome-zarr file converted by "
        "bioformats2raw.",
    )
    parser.add_argument(
        "--input_key",
        "-k",
        default="0/0",
        type=str,
        help="Key to the zarr array.",
    )
    parser.add_argument(
        "--channel",
        "-c",
        type=int,
        help="Channel to calculate the contrast limits for.",
    )
    parser.add_argument(
        "--func",
        "-fu",
        default="percentile",
        type=str,
        help="Function to calculate the contrast limits. Options are "
        "'percentile' and 'fiji'.",
    )
    parser.add_argument(
        "--full_volume",
        "-fv",
        action="store_true",
        help="If set, calculate the contrast limits for the entire volume "
        "instead of only using the enctral slice.",
    )
    return parser.parse_args()


def main():
    args = get_args()
    contrast_limits = get_contrast_limits(
        zarr_file_path=args.input_file,
        zarr_key=args.input_key,
        channel=args.channel,
        func=args.func,
        central_slice=not args.full_volume,
    )
    print(contrast_limits)


if __name__ == "__main__":
    main()
