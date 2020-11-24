import cv2
import numpy as np
import os
from os.path import isfile, join
import argparse
from natsort import natsorted
from tqdm import tqdm

parser = argparse.ArgumentParser()
parser.add_argument('--pathIn')
parser.add_argument('--pathOut')
args = parser.parse_args()

image_folder = args.pathIn
video_name = os.path.join(args.pathOut, "result.mp4")

images = [img for img in os.listdir(image_folder) if img.startswith('Frame')]
images = natsorted(images)
frame = cv2.imread(os.path.join(image_folder, images[0]))
height, width, layers = frame.shape

video = cv2.VideoWriter(video_name, cv2.VideoWriter_fourcc(*'mp4v'), 7, (width,height))

print("\n", "Converting to video...")
for image in tqdm(images):
    video.write(cv2.imread(os.path.join(image_folder, image)))

cv2.destroyAllWindows()
video.release()