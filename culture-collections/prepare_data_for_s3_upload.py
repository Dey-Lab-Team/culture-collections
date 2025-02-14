import argparse

from mobie.metadata import add_remote_project_metadata  # pyright: ignore


def get_args():
    parser = argparse.ArgumentParser(
        description="Add s3 information to MoBIE project files. No arguments needed."
    )
    parser.parse_args()


def main():
    add_remote_project_metadata(
        root="data",
        bucket_name="culture-collections/data",
        service_endpoint="https://s3.embl.de",
    )


if __name__ == "__main__":
    get_args()
    main()
