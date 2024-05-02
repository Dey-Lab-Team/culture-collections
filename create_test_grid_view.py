from mobie.view_utils import create_grid_view

DATASET_FOLDER = "data/single_volumes"
VIEW_NAME = "test_grid_view"
SOURCES = [
    ["5488_5533_ch0", "5488_5533_ch1", "5488_5533_ch2"],
    ["5488_5534_ch0", "5488_5534_ch1", "5488_5534_ch2"],
    ["5810_6123_ch0", "5810_6123_ch1", "5810_6123_ch2"],
]
DISPLAY_GROUPS = {
    "5488_5533_ch0": "5488_5533_ch0",
    "5488_5533_ch1": "5488_5533_ch1",
    "5488_5533_ch2": "5488_5533_ch2",
    "5488_5534_ch0": "5488_5534_ch0",
    "5488_5534_ch1": "5488_5534_ch1",
    "5488_5534_ch2": "5488_5534_ch2",
    "5810_6123_ch0": "5810_6123_ch0",
    "5810_6123_ch1": "5810_6123_ch1",
    "5810_6123_ch2": "5810_6123_ch2",
}
DISPLAY_GROUPS_SETTINGS = {
    "5488_5533_ch0": {
        "imageDisplay": {
            "color": "white",
            "contrastLimits": [84, 15004],
            "name": "5488_5533_ch0",
            "opacity": 1.0,
            "sources": ["5488_5533_ch0"],
        }
    },
    "5488_5533_ch1": {
        "imageDisplay": {
            "color": "green",
            "contrastLimits": [82, 158],
            "name": "5488_5533_ch1",
            "opacity": 1.0,
            "sources": ["5488_5533_ch1"],
        }
    },
    "5488_5533_ch2": {
        "imageDisplay": {
            "color": "blue",
            "contrastLimits": [369, 1127],
            "name": "5488_5533_ch2",
            "opacity": 1.0,
            "sources": ["5488_5533_ch2"],
        }
    },
    "5488_5534_ch0": {
        "imageDisplay": {
            "color": "white",
            "contrastLimits": [90, 5681],
            "name": "5488_5534_ch0",
            "opacity": 1.0,
            "sources": ["5488_5534_ch0"],
        }
    },
    "5488_5534_ch1": {
        "imageDisplay": {
            "color": "green",
            "contrastLimits": [89, 121],
            "name": "5488_5534_ch1",
            "opacity": 1.0,
            "sources": ["5488_5534_ch1"],
        }
    },
    "5488_5534_ch2": {
        "imageDisplay": {
            "color": "blue",
            "contrastLimits": [378, 551],
            "name": "5488_5534_ch2",
            "opacity": 1.0,
            "sources": ["5488_5534_ch2"],
        }
    },
    "5810_6123_ch0": {
        "imageDisplay": {
            "color": "white",
            "contrastLimits": [90, 5681],
            "name": "5810_6123_ch0",
            "opacity": 1.0,
            "sources": ["5810_6123_ch0"],
        },
    },
    "5810_6123_ch1": {
        "imageDisplay": {
            "color": "green",
            "contrastLimits": [89, 121],
            "name": "5810_6123_ch1",
            "opacity": 1.0,
            "sources": ["5810_6123_ch1"],
        }
    },
    "5810_6123_ch2": {
        "imageDisplay": {
            "color": "blue",
            "contrastLimits": [378, 551],
            "name": "5810_6123_ch2",
            "opacity": 1.0,
            "sources": ["5810_6123_ch2"],
        }
    },
}
MENU_NAME = "test_species"

if __name__ == "__main__":
    create_grid_view(
        DATASET_FOLDER,
        VIEW_NAME,
        SOURCES,
        display_groups=DISPLAY_GROUPS,
        display_group_settings=DISPLAY_GROUPS_SETTINGS,
        menu_name=MENU_NAME,
        overwrite=True,
    )
