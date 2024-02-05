import time
from elf.io import open_file
import numpy as np


def calc_contrast_limits(image):
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


def get_contrast_limits(zarr_file_path, channel, zarr_key="1"):
    zarr_file = open_file(zarr_file_path, mode="r")
    contrast_limits = calc_contrast_limits(zarr_file[zarr_key][0, channel])
    return contrast_limits


def main():
    file_path = "/home/hellgoth/Documents/work/projects/" \
        "culture-collections_project/converted_copy/5488_5534.ome.zarr"
    zarr_file = open_file(file_path, mode="r")
    print(zarr_file)
    for key in range(8):
        print(key)
        s = time.time()
        contrast_limits = get_contrast_limits(file_path, zarr_key=key)
        e = time.time()
        print(contrast_limits, e-s)


if __name__ == "__main__":
    main()
