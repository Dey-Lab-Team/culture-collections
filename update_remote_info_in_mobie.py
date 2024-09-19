import warnings

from mobie.metadata import add_remote_project_metadata  # pyright: ignore


def update_remote_info_in_mobie(
    mobie_project_directory: str = "data",
    bucket_name: str = "culture-collections",
):
    print("Adding s3 metadata...")
    # ignore useless spamy warning from mobie
    with warnings.catch_warnings():
        warnings.filterwarnings("ignore")
        add_remote_project_metadata(
            root=mobie_project_directory,
            bucket_name=bucket_name + "/data",
            service_endpoint="https://s3.embl.de",
        )


def main():
    update_remote_info_in_mobie()


if __name__ == "__main__":
    main()
