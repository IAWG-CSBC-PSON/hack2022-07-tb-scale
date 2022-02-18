import time, os, sys
import subprocess
import argparse
import datetime as dt

import numpy as np
import tifffile
import napari

# from cellpose import models, io

# model = models.Cellpose(gpu=False, model_type='nuclei')

# command line processing of arguments
parser = argparse.ArgumentParser(description='splitrun.py: read a OME-TIFF or other file and split into tiles and run each with cellpose')
parser.add_argument("InPath", help="Provide path to the input (OME-)TIFF or other file")
parser.add_argument("OutPath", help="Provide a path for the output stuff")
parser.add_argument("-t", "--tilesize", help="Chop image up in tiles of this size (default is 512 pixels)", action="store", default="512")
parser.add_argument("-v", "--verbose", help="Be more verbose", action="store_true", default=False)

args = parser.parse_args()

inpath = args.InPath
outpath = args.OutPath
ts = int(args.tilesize)

img = tifffile.imread(inpath)

xs = img.shape[1]
ys = img.shape[2]

# viewer = napari.view_image(img, channel_axis=0)
viewer = napari.Viewer()

chanim = img[0,0:xs,0:ys]

def run_chunk(im,x,dx,y,dy):
    imname = outpath + "/chunk_%d_%d.tif" % (x, y)
    tifffile.imwrite(imname, im[x:dx,y:dy])
    img = im[x:dx,y:dy]
    # masks, flows, styles, diams = model.eval(img, diameter=None, channels=[0,0])
    # io.masks_flows_to_seg(img, masks, flows, diams, imname, [0,0])
    # io.save_to_png(img, masks, flows, imname)
    viewer.add_image(img)

y = 0
while y < ys:
    x = 0
    while x < xs:
        if y+ts > ys or x+ts > xs:
            break
        run_chunk(chanim, x, x+ts, y, y+ts)
        x += ts
        inp = input("Return to continue ..")
    y += ts

inp = input("Return to start Cellpose ..")

dt_string = dt.datetime.now().strftime("%d-%m-%Y_%H:%M:%S")
outfile = 'profiles/{}profile_tile{}_{}.txt'.format('normal_', args.tilesize, dt_string)
# fast_filename = 'profiles/{}profile_{}.txt'.format('fast_', dt_string)

normal_command = 'python -m cProfile -m cellpose --dir tmp/ --pretrained_model nuclei --save_tif --verbose > {}'.format(outfile)
# fast_command = 'python -m cProfile -m cellpose --dir tmp/ --pretrained_model nuclei --save_tif --verbose --fast_mode > {}'.format(fast_filename)
subprocess.run(normal_command, shell=True)

with open(outfile, 'r') as in_file:
    contents = in_file.read().split('\n')
    contents = contents[17:]
    contents = [i.split() for i in contents]

    # rejoin function names in positions item[5:] that are split because they contain ','
    for item in contents:
        if len(item[5:]) > 1:
            joined = [' '.join(item[5:])]
            item[5:] = joined

    contents = [','.join(i) for i in contents]

    outpath = outfile[:-3] + 'csv'
    with open(outpath, 'w') as out_file:
        for line in contents:
            out_file.write(line + '\n')

