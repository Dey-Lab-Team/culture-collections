import json
import os
import warnings
import requests
from bs4 import BeautifulSoup
import pickle


URL = "https://bio-formats.readthedocs.io/en/v7.1.0/supported-formats.html"


def get_page(url=URL, save=False):
    if os.path.isfile("page.pickle"):
        return pickle.load(open("page.pickle", "rb"))
    page = requests.get(url)
    if save:
        pickle.dump(page, open("page.pickle", "wb"))
    return page


def scrape_supported_file_types_from_page(page):
    soup = BeautifulSoup(page.content, "html.parser")
    table = soup.find("table", class_="sortable docutils align-default")
    table_body = table.find("tbody")
    rows = table_body.find_all("tr", class_=["row-odd", "row-even"])
    entries = []
    for row in rows:
        entry = row.find_all("td")[1]
        text = entry.text
        file_formats = text.split(", ")
        entries.extend(
            # remove empty strings
            # remove leading . from file formats
            [file_format[1:] for file_format in file_formats
             if file_format and file_format != "etc."]
        )
    return entries


def get_supported_file_types(url=URL, scrape_again=False):
    if os.path.isfile("supported_file_types.txt") and not scrape_again:
        return json.load(open("supported_file_types.txt", "r"))
    page = get_page(url)
    entries = scrape_supported_file_types_from_page(page)
    entries = sorted(entries)
    with open("supported_file_types.txt", "w", encoding="utf-8") as f:
        json.dump(entries, f, ensure_ascii=False, indent=4)
    return entries


# TODO: is this the correct way of doing it?
SUPPORTED_FILE_TYPES = get_supported_file_types()


def is_format_supported(file_path, warn=False):
    file_format = ".".join(os.path.split(file_path)[1].split(".")[1:])
    if file_format in SUPPORTED_FILE_TYPES:
        return True
    if warn:
        warnings.warn(
            f"{file_format} is not a supported file format. "
            "Skipping this file."
        )
    return False


def main():
    _ = get_supported_file_types(scrape_again=True)


if __name__ == "__main__":
    main()
