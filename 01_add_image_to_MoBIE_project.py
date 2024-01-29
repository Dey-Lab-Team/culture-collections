import argparse
import os
import mobie
import xml.etree.ElementTree as ET


# make one huge dataset with all the data
# make one dataset per species
# make one thumbnail as default for each dataset
# add projections


# mobie_project_folder = "/home/hellgoth/Documents/work/projects/"
# "culture-collections_project/culture-collections"
# input_file = "/home/hellgoth/Documents/work/projects/"
# "culture-collections_project/converted_data/5488_5533.ome.zarr"
# input_key = os.path.join("0", "0")

# # dataset_name = "test_species_01"
# dataset_name = "all_the_data"
# dataset_folder = os.path.join(mobie_project_folder, dataset_name)

# menu_name = "species"


def get_number_of_channels_from_ome_metadata(xml_file):
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
    zarr_file,
    zarr_key,
    mobie_project_directory,
    dataset_name,
    menu_name,
    is_default_dataset=False,
):
    image_name = zarr_file.split('/')[-1].split('.')[0]
    xml_file = os.path.join(zarr_file, "OME/METADATA.ome.xml")
    num_channels = get_number_of_channels_from_ome_metadata(xml_file)
    for channel in range(num_channels):
        # just move data, don't copy, apparently internally only changes
        # pointer not moving a single byte (as long as on same filesystem),
        # so it should not matter if we call this multiple times (for each
        # channel)
        mobie.add_image(
            input_path=zarr_file,
            input_key=zarr_key,
            root=mobie_project_directory,
            dataset_name=dataset_name,
            image_name=image_name + f"_ch{channel}",
            menu_name=menu_name,
            file_format="ome.zarr",
            is_default_dataset=is_default_dataset,
            move_only=True,
            resolution=None,  # not needed since we just move data
            chunks=None,  # not needed since we just move data
            scale_factors=None,  # not needed since we just move data
            channel=channel
        )


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
        default=os.path.join("0", "0"),
        type=str,
        help="Key of the data inside the input file.",
    )
    parser.add_argument(
        "--mobie_project_folder",
        "-p",
        default="./data",  # or os.getcwd()? or even hardcode?
        type=str,
        help="Path to the MoBIE project folder.",
    )
    parser.add_argument(
        "--dataset_name",
        "-d",
        default="all_single_channel_images",
        type=str,
        help="Name of the dataset to add the data to."
        "If it does not exist, it will be created.",
    )
    parser.add_argument(
        "--menu_name",
        "-m",
        default="species",
        type=str,
        help="Name of the menu to add the data to."
        "If it does not exist, it will be created.",
    )
    parser.add_argument(
        "--is_default_dataset",
        "-i",
        default=False,
        type=bool,
        help="Whether this dataset should be the default one.",
    )
    return parser.parse_args()


def main():
    # make argparser
    # run it once to create the project
    # adjust contrast (need to handle vieww)
    # make a folder input and iterate over all files in there
    # do single steps but then combine into one file (maybe via snakmake?)
    args = get_args()
    add_multichannel_zarr_image(
        args.input_file,
        args.input_key,
        args.mobie_project_folder,
        args.dataset_name,
        args.menu_name,
        args.is_default_dataset,
    )


if __name__ == "__main__":
    main()
