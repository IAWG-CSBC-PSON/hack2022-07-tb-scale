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

* You may find it useful to visualize input images and Cellpose output. Install `napari` to help with this.

```
python -m pip install PyQt5 napari
```

## Running Cellpose on data

Download the above images and place each one in a separate folder. Provide individual folders as input to Cellpose. For example,

```
$ ls
cellpose  exemplar-001

$ ls exemplar-001/
exemplar-001.ome.tif

$ python -m cellpose --dir exemplar-001/ --pretrained_model nuclei --save_tif --channel_axis 0 --chan 1 --verbose
2022-01-27 16:56:08,619 [INFO] WRITING LOG OUTPUT TO /home/sokolov/.cellpose/run.log
2022-01-27 16:56:08,619 [INFO] >>>> using CPU
2022-01-27 16:56:08,620 [INFO] >>>> running cellpose on 1 images using chan_to_seg RED and chan (opt) NONE
2022-01-27 16:56:08,620 [INFO] >>>> using CPU
2022-01-27 16:56:08,703 [INFO] >>>> using diameter 30.00 for all images
2022-01-27 16:56:08,704 [INFO] 0%|          | 0/1 [00:00<?, ?it/s]
2022-01-27 16:56:09,196 [INFO] ~~~ FINDING MASKS ~~~
2022-01-27 16:56:09,196 [INFO] Evaluating with flow_threshold 0.40, mask_threshold 0.00
2022-01-27 16:56:41,164 [INFO] mask_threshold is 0.000000
2022-01-27 16:56:49,425 [INFO] >>>> TOTAL TIME 40.23 sec
2022-01-27 16:56:49,968 [INFO] 100%|##########| 1/1 [00:41<00:00, 41.26s/it]
2022-01-27 16:56:49,968 [INFO] 100%|##########| 1/1 [00:41<00:00, 41.26s/it]
2022-01-27 16:56:49,968 [INFO] >>>> completed in 41.350 sec
```

where

* `--dir` - specifies the input directory
* `--pretrained_model nuclei` - requests that Cellposes uses its built-in model for segmenting nuclei
* `--channel_axis 0` - specifices that the input image (which has shape [12, 3138, 2509]) indexes channels by the 0^th entry.
  * *Python uses 0-based indexing, so the first entry has index 0.*
* `--chan 1` - asks Cellpose to segment nuclei based on the first channel in the image.
  * *Confusingly, Cellpose uses 1-based indexing for channels.*
* `--save_tif` - specifies the output format, which can now be found in the same directory as the input

```
$ ls exemplar-001/
exemplar-001.ome_cp_masks.tif  exemplar-001.ome_seg.npy  exemplar-001.ome.tif
```

## Visualizing image

A straightforward way to inspect input images and segmentation masks produced by Cellpose is by using `tifffile` and `napari` Python packages. The following Python script will load the image and bring up a Napari viewer for interactive browsing.

``` python
import tifffile
import napari

img = tifffile.imread('exemplar-001.ome.tif')
napari.view_image(img, channel_axis=0)
```

The output segmentation mask can be visualized similarly
``` python
mask = tifffile.imread('exemplar-001.ome_cp_masks.tif')
napari.view_image(mask)
```

Note that `img.shape` is `(12, 3138, 2509)`, highlighting the input image is multi-channel. As with Cellpose, we tell Napari that the first element (i.e., `0` in 0-based indexing) of the array indexes over the channels. Conversely, `mask.shape` is `(3138, 2509)`, because the segmentation mask is a 2D array of integer indices that assign individual pixels to a given cell. Thus, no `channel_axis` specification is needed when viewing the image.
