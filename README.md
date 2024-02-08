# culture-collections
The metadata of a [MoBIE](https://github.com/mobie-org/mobie) project to publish and inspect image data from different culture collections and the according python scripts.

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
Only for researchers that are part of the project.

### Rough idea
TODO:
- explain MoBIE and idea
- how to open terminal?

### Prerequisites
#### GitHub account
To update the MoBIE project you need write access to this GitHub repository. For this you need to have a GitHub account. If you don't have one yet, create one [here](https://github.com/). Then contact [Jonas Hellgoth](https://github.com/JonasHell) (easiest via [mail](mailto:jonas.hellgoth@embl.de)) to be added to the repository as a collaborator (this grants you write access). TODO: is this correct???

#### write access to s3
To upload data to the s3 bucket you need write access. For this please contact [Jonas Hellgoth](https://github.com/JonasHell). The easiest is via [mail](mailto:jonas.hellgoth@embl.de).

#### git
[git](https://creativecommons.org/2014/01/07/plaintext-versions-of-creative-commons-4-0-licenses/) is a version control system. Here, we are mainly using it to interact with this GitHub repository in order to update the MoBIE project. If you don't have it installed already follow the [installation instructions](https://git-scm.com/book/en/v2/Getting-Started-Installing-Git) and the [setup instructions](https://git-scm.com/book/en/v2/Getting-Started-First-Time-Git-Setup). To check if you have it already installed or if your installation was successfull you can run `git --version` in your terminal.

#### micromamba/mamba/conda
The easiest way to install python and all the needed packages is a package & environment manager. There are different options called mamba and conda. In addition, for each of them there is minimalist version called micromamba and miniconda, respectively. If you have any of these installed you can use it. In general, any `mamba` command can be replaced by `conda` and vice versa. If you do not have any of these installed, I would recommend using micromamba following [these instructions](https://mamba.readthedocs.io/en/latest/installation/micromamba-installation.html). The conda alterantive can be found [here](https://conda.io/projects/conda/en/latest/user-guide/install/index.html). Again, to check your installation you can try `mamba --version`.

### Clone repository & create environment
*NOTE: Cloning the repository and creating the environment needs to be done only once. Afterwards you can just reuse them.*

To get started we need to create a local copy of this repository on your machine (called cloning). Open a terminal and navigate to the directory the repository should be saved in by
```sh
$ cd <directory_of_your_choice>
```
`<directory_of_your_choice>` could be `~/software/repos` for example (`~/` is your home directory). Clone the repository by
```sh
$ git clone ...
```
Navigate into the repository by
```sh
$ cd culture-collections
```
Create the environment by running the following command. This will install all the necessary packages into this virtual environment.
```sh
$ mamba create -n culture-collections -f environment.yaml
```
Potentially you need to accept the installation by tiping `y` and hitting enter.

### Open folder & activate environment
To run a script make sure that you are inside the repository.
```sh
$ cd <path_to_the_repository_on_your_machine>
```
depending to which location you cloned the repository `<path_to_the_repository_on_your_machine>` could be something like `~/software/repos/culture-collections`
Additionally, make sure the correct environment is activated by
```sh
$ mamba activate culture-collections
```

### Add images
```sh
python do_all_at_once.py -d <your_input_data>
```
`<your_input_data>` can either be a single file, a comma-seperated list of files (no spaces) or a directory. In the last case all files in this directory will be added. Only files supported by [bioformats2raw](https://github.com/glencoesoftware/bioformats2raw) can be added, others are skipped. `supported_file_types.txt` contains a list of currently supported file formats. This list is also available [here](). This is checked by the script and nothing you need to take care of. Unless, your file format is not supported. In this case you need to find a different way to convert it to `ome-zarr`. If this happens please contact [Jonas Hellgoth](https://github.com/JonasHell) via [mail](mailto:jonas.hellgoth@embl.de).