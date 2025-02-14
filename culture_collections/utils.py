import argparse
import os
import warnings

from scrape_supported_file_types_from_web import is_format_supported


def filter_for_supported_file_formats(input_data: list[str]):
    valid_files: list[str] = []
    for path in input_data:
        if os.path.exists(path):
            if is_format_supported(path, warn=True):  # supported file case
                valid_files.append(path)
            elif os.path.isdir(path):  # directory case
                valid_files.extend(
                    [
                        os.path.join(path, file)
                        for file in os.listdir(path)
                        if is_format_supported(file, warn=True)
                    ]
                )
        else:
            warnings.warn(f"{path} does not exist. It will be ignored.")
    return valid_files


def is_ome_zarr(file_path: str, warn: bool = False) -> bool:
    is_ome_zarr = file_path.endswith(".ome.zarr")
    if not is_ome_zarr and warn:
        warnings.warn(f"{file_path} is not an ome-zarr file. It will be ignored.")
    return is_ome_zarr


def filter_for_ome_zarr(input_data: list[str]):
    valid_files: list[str] = []
    for path in input_data:
        if os.path.exists(path):
            if is_ome_zarr(path, warn=True):  # supported file case
                valid_files.append(path)
            elif os.path.isdir(path):  # directory case
                valid_files.extend(
                    [
                        os.path.join(path, file)
                        for file in os.listdir(path)
                        if is_ome_zarr(file, warn=True)
                    ]
                )
        else:
            warnings.warn(f"{path} does not exist. It will be ignored.")
    return valid_files


def parse_args():
    parser = argparse.ArgumentParser(description="This is not a script to run")
    parser.parse_args()


if __name__ == "__main__":
    parse_args()
