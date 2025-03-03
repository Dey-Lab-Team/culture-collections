import json


def main():
    metadata_path = "/home/hellgoth/Documents/work/projects/culture-collections_project/culture-collections/data/single_volumes/dataset.json"
    with open(metadata_path, "r") as f:
        dataset_metadata = json.load(f)
    print()
    for key in dataset_metadata["views"].keys():
        print(key)
    print(len(dataset_metadata["views"]))


if __name__ == "__main__":
    main()
