import argparse

from utils import filter_for_supported_file_formats


def get_args():
    parser = argparse.ArgumentParser(
        description="List all input files based on an input you would give "
        "to a script that adds images to MoBIE."
    )
    parser.add_argument(
        "--input_data",
        "-f",
        nargs="+",
        type=str,
        help="Path to the input data. Can be either a single file, "
        "multiple files or a directory containing multiple files.",
    )
    args = parser.parse_args()
    return args


def print_input_files(input_files: list[str]):
    print("Input files:")
    for file in input_files:
        print(file)


def main():
    args = get_args()
    input_files = filter_for_supported_file_formats(args.input_data)
    print_input_files(input_files)


if __name__ == "__main__":
    main()
