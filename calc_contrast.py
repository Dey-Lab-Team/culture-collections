import time

import numpy as np
from elf.io import open_file


def calc_contrast_limits_fiji_style(image):
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


def calc_contrast_limits_percentile(image, percentile=(0.1, 99.9)):
    lower_bound = np.percentile(image, percentile[0])
    upper_bound = np.percentile(image, percentile[1])
    return [int(lower_bound), int(upper_bound)]


def get_contrast_limits(
    zarr_file_path, channel, zarr_key="0", func="percentile", central_slice=True
):
    zarr_file = open_file(zarr_file_path, mode="r")
    zarr_array = zarr_file[zarr_key]
    if central_slice:
        image = zarr_array[0, channel, zarr_array.shape[2] // 2]
    else:
        image = zarr_array[0, channel]
    if func == "percentile":
        contrast_limits = calc_contrast_limits_percentile(image)
    elif func == "fiji":
        contrast_limits = calc_contrast_limits_fiji_style(image)
    else:
        raise ValueError(f"Unknown function {func}")
    return contrast_limits


def main():
    file_path = (
        "/home/hellgoth/Documents/work/projects/"
        "culture-collections_project/converted_copy/5488_5534.ome.zarr"
    )
    zarr_file = open_file(file_path, mode="r")
    print(zarr_file)
    for key in range(8):
        print(key)
        s = time.time()
        contrast_limits = get_contrast_limits(file_path, zarr_key=key)
        e = time.time()
        print(contrast_limits, e - s)


if __name__ == "__main__":
    main()
