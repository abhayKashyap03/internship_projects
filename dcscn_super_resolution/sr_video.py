import cv2
import numpy as np
import glob
import argparse
import os
from os.path import  isfile, join

parser = argparse.ArgumentParser()
parser.add_argument('--frame_path', required=True)
parser.add_argument('--out_dir', required=True)
args = parser.parse_args()

fps = 30

frame_array = []
files = [f for f in os.listdir(args.frame_path) if f.endswith("_result.jpg")]

#for sorting the file names properly
files = sorted(files, key=lambda item: (int(item.partition('_')[0])
                               if item[0].isdigit() else float('inf'), item))

print(files)

for i in range(len(files)):
    filename = args.frame_path + files[i]
    #reading each files
    img = cv2.imread(filename)
    height, width, layers = img.shape
    size = (width,height)
    #inserting the frames into an image array
    frame_array.append(img)
    
out = cv2.VideoWriter(args.out_dir, cv2.VideoWriter_fourcc(*'DIVX'), fps, size)
    
for i in range(len(frame_array)):
    # writing to a image array
    out.write(frame_array[i])
    
out.release()

print("----------------------Video compilation complete----------------------")
