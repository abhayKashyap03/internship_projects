import os
import cv2
import argparse
import numpy as np
import pandas as pd
from glob import glob
from time import time


def avg_x(img, channel, places):
    if len(img.shape) == 2:
        x_ = img[:, :].flatten()
        return round(np.mean(x_), places)
    elif len(img.shape) == 3:
        x_ = img[:, :, channel].flatten()
        return round(np.mean(x_), places)


def median_x(img, channel, places):
    if len(img.shape) == 2:
        x_ = img[:, :].flatten()
        return round(np.median(x_), places)
    elif len(img.shape) == 3:
        x_ = img[:, :, channel].flatten()
        return round(np.median(x_), places)


def std_dev_x(img, channel, places):
    if len(img.shape) == 2:
        x_ = img[:, :].flatten()
        return round(np.std(x_), places)
    elif len(img.shape) == 3:
        x_ = img[:, :, channel].flatten()
        return round(np.std(x_), places)


parser = argparse.ArgumentParser()
parser.add_argument('--image_folder', type=str, required=True)
parser.add_argument('--decimal_places', type=int, default=2)
parser.add_argument('--save_as', type=str, required=True)
args = parser.parse_args()

start = time()

ext = ['.jpeg', '.jpg', '.png', '.bmp']
files = [file for files in list(filter(None, [glob(os.path.join(args.image_folder, '*'+e)) for e in ext])) for file in files]
images = [cv2.imread(file) for file in files]
img_types = [0 if len(img.shape) == 2 else 1 for img in images]

r = [[avg_x(img, 2, args.decimal_places), median_x(img, 2, args.decimal_places), std_dev_x(img, 2, args.decimal_places)]
     for img in images]
g = [[avg_x(img, 1, args.decimal_places), median_x(img, 1, args.decimal_places), std_dev_x(img, 1, args.decimal_places)]
     for img in images]
b = [[avg_x(img, 0, args.decimal_places), median_x(img, 0, args.decimal_places), std_dev_x(img, 0, args.decimal_places)]
     for img in images]

pd.DataFrame({'S.No.': [(i + 1) for i in range(len(files))], 'Image Name': [os.path.basename(file) for file in files],
              'RGB/GRAY': img_types, 'avg_b': [b[i][0] for i in range(len(b))], 'avg_g': [g[i][0] for i in range(len(g))],
              'avg_r': [r[i][0] for i in range(len(r))], 'median_b': [b[i][1] for i in range(len(b))],
              'median_g': [g[i][1] for i in range(len(g))], 'median_r': [r[i][1] for i in range(len(r))],
              'std_dev_b': [b[i][2] for i in range(len(b))], 'std_dev_g': [g[i][2] for i in range(len(g))],
              'std_dev_r': [r[i][2] for i in range(len(r))]}).to_csv(args.save_as, index=False)

print('Completed in : ', round(time() - start), 'seconds')
