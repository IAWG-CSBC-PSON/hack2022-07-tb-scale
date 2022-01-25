# Imaging Hackathon 2022
## Challenge 7: Enabling Image Analysis for TB-scale data

Modern highly-multiplexed imaging methods are capable of producing TB-scale datasets, with individual images requiring dozens of GB of storage and extensive resources for processing. The scale of today’s images poses substantial challenges for applying existing methods that may have been developed and prototyped on smaller-scale data. As image sizes keep increasing, a shift towards more efficient implementations may be required.

Central to image analysis is cell segmentation, which aims to localize cells within images. It is a required step for nearly all downstream analyses, and inefficient segmentation methods can therefore present a substantial bottleneck to image processing. In this challenge, we will examine Cellpose [[Stringer, et al.](https://doi.org/10.1038/s41592-020-01018-x)] to understand how various steps in the segmentation process affect runtime and peak memory usage. While optimizations to the Cellpose codebase are welcome and encouraged, the goal of the hackathon challenge is to develop software engineering guidelines about efficient implementations of image analysis methods.

