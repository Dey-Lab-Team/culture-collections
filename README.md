# culture-collections
This repository contains both, the metadata of the culture-collections [MoBIE](https://mobie.github.io/) project as well as the according python scripts to create and update the project.

## Background
TODO:
- culture collections used, link to their website
- link paper
- a bit more background info

## External users
TODO:
- install Fiji, and MoBIE
- open...


## Internal users
*NOTE: This part is relevant only for researchers who are part of the project.*

### Rough idea
The basic idea of this project is to find a way to share the imaging data between the different participating labs. The imaging data itself lives on a central s3 storage provided by EMBL. In general, collaborating labs can upload data to and download data from there. For now, the internal structure of this s3 storage (called a "bucket") is defined by the MoBIE project that was established to simplify the visualization of the data. [MoBIE](https://mobie.github.io/) is a tool to visualize large image files and stream them directly from a s3 storage. By this users don't need to download GBs of data to their local machine. This is faciliated by the ome-zarr file format. This file format provides an image pyramid with different levels of resolution and image data that is cut into pieces (called "chunks"), which allows MoBIE to only load data that is currently needed. The MoBIE metadata, meaning the data that tells MoBIE where to find and how to visualize the actual imaging data, is part of this git repository. By this we have it version controlled and easily accessible from the outside (see section [Internal users](#internal-users)). For now, everything is private and not visible to the public.

TODO:
- how to open terminal?

### Prerequisites
*NOTE: You will need to work on a terminal. It's not that hard, don't be scared! If you have no experience at all, here are some links to get started [Windows](https://adamtheautomator.com/git-bash-commands/) or [Windows](https://www.wikihow.com/Open-Terminal-in-Windows), [macOS](https://support.apple.com/guide/terminal/open-or-quit-terminal-apd5265185d-f365-44cb-8b09-71a064a42125/mac), [Linux](https://www.geeksforgeeks.org/how-to-open-terminal-in-linux/).*

#### GitHub account
To update the MoBIE project you need write access to this GitHub repository. For this you need to have a GitHub account. If you don't have one yet, create one [here](https://github.com/). Then contact [Jonas Hellgoth](https://github.com/JonasHell) (easiest via [mail](mailto:jonas.hellgoth@embl.de)) to be added to the repository as a collaborator (this grants you write access to this GitHub repository).

#### Write access to s3
To upload data to the s3 bucket you need write access. For this please contact [Jonas Hellgoth](https://github.com/JonasHell). The easiest is via [mail](mailto:jonas.hellgoth@embl.de). You will recieve a key pair for read-write access. To interact with the s3 storage you need to install the MinIO client. Just follow the first step of [these instructions](https://min.io/docs/minio/linux/reference/minio-mc.html) for your operating system. You can check the installation success by running `mc --version` in your terminal. If `brew` throws an error saying you can try `xcode-select --install` do so and see if this works.

Continue with step 2 of the instructions, use the following for the command `mc alias set ALIAS HOSTNAME ACCESS_KEY SECRET_KEY`:

- `ALIAS`: `culcol_s3_rw`
- `HOSTNAME`: `https://s3.embl.de`
- `ACCESS_KEY`: the public key of the read-write key pair you got
- `SECRET_KEY`: the secret key of the read-write key pair you got

Step 3 won't work since you don't have admin rights. Use `mc alias list` instead to check if the alias is there.

#### git
*NOTE: If you have a working git installation you can skip this step.*

[git](https://creativecommons.org/2014/01/07/plaintext-versions-of-creative-commons-4-0-licenses/) is a version control system. Here, we are mainly using it to interact with this GitHub repository in order to update the MoBIE project. If you don't have it installed already follow the [installation instructions](https://git-scm.com/book/en/v2/Getting-Started-Installing-Git) and the [setup instructions](https://git-scm.com/book/en/v2/Getting-Started-First-Time-Git-Setup). To check if you have it already installed or if your installation was successfull you can run `git --version` in your terminal.

#### Connect git to GitHub
*NOTE: If you already worked with git/GitHub you can probably skip this step.*

GitHub needs a way to verify that you are you and that you have the correct permissions to push to a repository (aka write access). The easiest way to do this is to set up a key pair. Follow [this](https://docs.github.com/en/authentication/connecting-to-github-with-ssh/generating-a-new-ssh-key-and-adding-it-to-the-ssh-agent?platform=linux#generating-a-new-ssh-key) to create a key pair. If you leave the passphrase empty, there is no need to add the key to the ssh-agent (recommended). Afterwards follow [these steps](https://docs.github.com/en/authentication/connecting-to-github-with-ssh/adding-a-new-ssh-key-to-your-github-account#adding-a-new-ssh-key-to-your-account) to add the public key to GitHub.

#### micromamba/mamba/conda
*NOTE: If you already have a package & environment manager installed you can skip this step.*

The easiest way to install python and all the needed packages is a package & environment manager. There are two main options called mamba and conda. In addition, for each of them there is minimalist version called micromamba and miniconda, respectively. If you have any of these installed you can use it. In general, any `mamba` command can be replaced by `conda` and vice versa. If you do not have any of these installed, I would recommend using micromamba following [these instructions](https://mamba.readthedocs.io/en/latest/installation/micromamba-installation.html). The conda alterantive can be found [here](https://conda.io/projects/conda/en/latest/user-guide/install/index.html). Again, to check your installation you can try `mamba --version`.

### Clone repository & create environment
*NOTE: Cloning the repository and creating the environment needs to be done only once. Afterwards you can just reuse them.*

To get started we need to create a local copy of this repository on your machine (called cloning). Open a terminal and navigate to the directory the repository should be saved in by
```sh
cd <directory_of_your_choice>
```
`<directory_of_your_choice>` could be `~/software/repos` for example (`~/` is your home directory). Clone the repository by
```sh
git clone git@github.com:Dey-Lab-Team/culture-collections.git
```
Navigate into the repository by
```sh
cd culture-collections
```
Create the environment by running the following command. This will install all the necessary packages into this virtual environment.
```sh
mamba env create -f environment.yml
```
Potentially you need to accept the installation by tiping `y` and hitting enter.

### Manually adjust environment
Unfortunately, we have to add some installations manually. The bugs causing these issues are already fixed, however, the new versions are not released yet. Therefore, conda/mamba only has access to the old versions. For now, we just add the fixed versions manually to our environment. First, activate the environment:
```sh
mamba activate culture-collections
```
Change the directory out of `culture-collections`:
```sh
cd ../
```
Clone the repository:
```sh
git clone git@github.com:mobie/mobie-utils-python.git
```
And install it:
```sh
pip install -e ./mobie-utils-python
```
Do the same for the other package:
```sh
git clone git@github.com:constantinpape/elf.git
```
```sh
pip install -e ./elf
```

### Open folder & activate environment
To run a script make sure that you are inside the repository.
```sh
cd <path_to_the_repository_on_your_machine>
```
depending to which location you cloned the repository `<path_to_the_repository_on_your_machine>` could be something like `~/software/repos/culture-collections`.

Additionally, make sure the correct environment is activated by
```sh
mamba activate culture-collections
```

### Add images
*NOTE: This process can run in the background, but the terminal must stay active (don't close it!) and so does your device.*

*NOTE: depending on how many images you add at once this can take a while (and block a significant amount of your device's ressources). One option could be to run it overnight. If you have access to a cluster it may be a good idea to run it there.*

Internally, the script has multiple steps. They are briefly explained in the following. If you are interested you can have a look, if not just go on and add your images:
<details>
<summary>Internally, the script has multiple steps. They are briefly explained in this collapsable section. If you are interested you can have a look, if not just go on and add your images by:
</summary>

#### Convert images to ome-zarr
Why we need to convert to ome-zarr is explained above. For this a subprocess is used that calls [bioformats2raw](https://github.com/glencoesoftware/bioformats2raw). Converted images are saved to a temporary directory called `tmp`. Depending on the size of an image and the compute power of your device this can take a few minutes.

#### Pull from GitHub
To make sure the git repository is up to date. Done via a subprocess.

#### Add images to MoBIE project
For now the MoBIE project has one big dataset called `single_volumes`. Each multichannel image is added to this dataset as a source. Additionally, a source for each channel is added and a view that visualizes a single image with all its channels. For this, an initial guess for the brightness settings is calculated, similar to the auto contrast of Fiji. While the images are added to the MoBIE project, the data is moved from the `tmp` directory to its appropiate place in the MoBIE project directory (this should be instantaneous since the data is not actually moved, just some pointers are adjusted). If everything goes well, the `tmp` directory will be empty and removed after all the images are added.

#### Add s3 metadata
Additional metadata is added that allows MoBIE to stream the data from the s3 storage.

#### Upload image data to s3 storage
The data is uploaded to th s3 storage. Depending on the image size and the speed of your internet connection this is probably the step that takes the longest.

#### Sync with the project on GitHub
So far, the changes to the MoBIE project just happened to your local copy. We need to push these changes to the GitHub repository. If someone else changed the the state of the repository in the meantime (e.g. by adding images) this can lead to so called merge conflicts. That's the reason we use git. It helps us to keep track of these changes and to resolve potential conflicts. Unfortunately, it is not possible to solve them automatically. If this happens, please solve them manually using git. You can find some help [here](). Otherwise you can ask for help and contact [Jonas Hellgoth](https://github.com/JonasHell) via [mail](mailto:jonas.hellgoth@embl.de).

To do all at once just run:
</details>

```sh
python do_all_at_once.py -d <your_input_data>
```
`<your_input_data>` can either be a single file path, a list of file paths or a directory. In the last case all files in this directory will be added. Only files supported by [bioformats2raw](https://github.com/glencoesoftware/bioformats2raw) can be added, others are skipped. `supported_file_types.txt` contains a list of currently supported file formats. This list is also available [here](https://bio-formats.readthedocs.io/en/v7.1.0/supported-formats.html). This is checked by the script and nothing you need to take care of. Unless, your file format is not supported. In this case you need to find a different way to convert it to `ome-zarr`. If this happens please contact [Jonas Hellgoth](https://github.com/JonasHell) via [mail](mailto:jonas.hellgoth@embl.de). Furthermore, the pipeline also support files containing multiple volumes (solved via the series dimension). Again, nothing you need to take care of.

#### Special case - channels are in seperate files
In some cases the individual channels of a volume are saved in different files. In this case please use the following script:

```sh
python do_all_at_once_seperate_channels.py -d <your_input_data>
```
Here, `<your_input_data>` is expected to be a list of the files containing the individual channels (please provide them in the correct order), thus, this script can only handle a single volume at a time.

### Other scripts
All other python files can also be run as scripts. They do single steps of the pipeline. To get more information you can run
```sh
python <script> -h
```
but usually using `do_all_at_once.py` should be enough.

### Open the MoBIE project in Fiji
As soon as the project is published you can follow the steps from the section [Internal users](#internal-users). For now you need to have Fiji and MoBIE installed.

<details>
<summary>Install Fiji and MoBIE</summary>

Downlaod and install Fiji from [here](https://imagej.net/software/fiji/downloads). Start it. If you never used MoBIE before go to `Help > Update > Manage Update Sites` and check the box in front of `MoBIE`. Click on `Apply and Close` and restart Fiji to make sure MoBIE is installed and up-to-date.

</details>

Make sure your local copy of the project is up-to-date by navigating to the directory:
```sh
cd <path_to_the_repository_on_your_machine>
```
and running:

*NOTE: For consistency reasons, don't do this while you are running a python script in the background that updates the project (like `do_all_at_once.py`).*
```sh
git pull
```

Start Fiji. Enter `mobie` into the search bar (lower right). Choose `Open MoBIE Project With S3 Credentials...` and hit `run`:
- `Project Location`: path to your local copy of this repository (e.g. `/home/hellgoth/software/repos/culture-collections/`)
- `Preferentially Fetch Data From`: `Local` = local image data is used, can't open remote image data, potentially faster | `Remote` = data is streamed from s3, all data available, depends on the speed of your internet connection
- `S3 Access Key`: the public key of the read-only key pair you got
- `S3 Secret Key`: the secret key of the read-only key pair you got
