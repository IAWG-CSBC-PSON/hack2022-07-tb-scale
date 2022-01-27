# Imaging Hackathon 2022
## Challenge 7: Enabling Image Analysis for TB-scale data

Modern highly-multiplexed imaging methods are capable of producing TB-scale datasets, with individual images requiring dozens of GB of storage and extensive resources for processing. The scale of today’s images poses substantial challenges for applying existing methods that may have been developed and prototyped on smaller-scale data. As image sizes keep increasing, a shift towards more efficient implementations may be required.

Central to image analysis is cell segmentation, which aims to localize cells within images. It is a required step for nearly all downstream analyses, and inefficient segmentation methods can therefore present a substantial bottleneck to image processing. In this challenge, we will examine Cellpose [[Stringer, et al.](https://doi.org/10.1038/s41592-020-01018-x)] to understand how various steps in the segmentation process affect runtime and peak memory usage. While optimizations to the Cellpose codebase are welcome and encouraged, the goal of the hackathon challenge is to develop software engineering guidelines about efficient implementations of image analysis methods.

## Data

The dataset for this challenge consists of three images, each larger than the previous one. It is recommended to use the first image for prototyping and benchmarking, while the other two images are meant to serve as "stress tests". All three images can be downloaded from [Synapse](https://www.synapse.org/#!Synapse:syn26848688):

* `exemplar-001.ome.tif` - a 400MB file that represents a minimal example for method development and benchmarking. It is a part of the MCMICRO datasets (https://mcmicro.org/datasets.html). The image contains 3,138 x 2,509 pixel intensities across 12 channels.
* `LUNG-1-LN_40X.ome.tif` - a 12GB image of a lung adenocarcinoma that metastasized to a lymph node. The image is a part of a CyCIF data release [[Rashid, et al.](https://www.nature.com/articles/s41597-019-0332-y)] and captures 10,101 x 9,666 pixels across 44 channels.
* `WD-76845-097.ome.tif` - an 80GB image of primary human colorectal adenocarcinoma. The image is the 97th serial section of a single multi-TB dataset [TNP-SARDANA](https://www.cycif.org/data/tnp-2020/osd-crc-case-1-ffpe-cycif-pilot) and contains 27,120 x 26,139 pixels in 40 channels.

All three images were acquired using Cyclic Immunofluorescence (CyCIF) [[Lin, et al.](https://elifesciences.org/articles/31657)] with the first channel of every 4-channel cycle corresponding to the nuclear stain.

## Setup

* Ensure that you have [Git](https://git-scm.com/) and [Conda](https://docs.conda.io/en/latest/) available in your environment.
* Fork the Cellpose repository to your own GitHub account by going to https://github.com/MouseLand/cellpose, clicking "Fork" in the top right corner and selecting yourself.
* Clone your fork to the local environment: `git clone https://github.com/<username>/cellpose.git`, replacing `<username>` with your GitHub username.
* Instantiate a new Conda environment and install Cellpose from your local copy of the source code, allowing you to edit and test the code in a continuous development cycle.

```
conda create -y --name cellpose python=3.8
conda activate cellpose
python -m pip install -e ./cellpose
```

where the last command should be run in the same directory as where you executed `git clone`.

* You may find it useful to visualize the input images and Cellpose output. Install `napari` to help with this.

```
python -m pip install PyQt5 napari
```
