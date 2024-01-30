from mobie.metadata import add_remote_project_metadata


def main():
    add_remote_project_metadata(
        root="data",
        bucket_name="culture-collections",
        service_endpoint="https://s3.embl.de"
    )


if __name__ == "__main__":
    main()
