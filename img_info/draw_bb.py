import os
import cv2
import ast
import time
import argparse
import numpy as np
import pandas as pd


def draw_box(points_, img, class_, colors_):
    color_ = colors_[class_]
    cv2.putText(img, class_, (points_[0], points_[1]-5), cv2.FONT_HERSHEY_SIMPLEX, 1, color_, 2)
    return cv2.rectangle(img, (points_[0], points_[1]), (points_[2], points_[3]), color_, 2)


parser = argparse.ArgumentParser()
parser.add_argument('--csv', type=str, required=True)
parser.add_argument('--image_folder', type=str, required=True)
parser.add_argument('--save_images', type=ast.literal_eval, default=True, required=False)
parser.add_argument('--dest_folder', type=str)
parser.add_argument('--wait', type=int, default=0)
args = parser.parse_args()

start = time.time()
data = pd.read_csv(args.csv)
filenames = list(set(data['filename']))
files = [os.path.join(args.image_folder, file) for file in filenames]
points = [data[data['filename'].str.contains(filename)][['xmin', 'ymin', 'xmax', 'ymax']].to_numpy().tolist() for
          filename in filenames]
classes = [data[data['filename'].str.contains(filename)]['class'].to_numpy().tolist() for filename in filenames]
colors = {'Plastic_Bottle': (255, 0, 0), 'Metal_Can': (0, 0, 255), 'Tetra_Pak': (255, 255, 0), 'Other_Object': (0, 255, 255),
          'Doubt_Object': (0, 255, 0)}

if args.dest_folder is None:
    args.dest_folder = os.path.join(os.path.split(args.image_folder)[0], 'annotated')
if args.dest_folder is not None and not os.path.exists(args.dest_folder):
    os.makedirs(args.dest_folder)

cv2.namedWindow("Image")
for i, file in enumerate(files):
    image = cv2.imread(file)
    if len(points[i]) > 1:
        for j in range(len(points[i])):
            image = draw_box(np.array(points[i][j], dtype=np.int64), image, classes[i][j], colors)
    else:
        image = draw_box(np.array(points[i][0], dtype=np.int64), image, classes[i][0], colors)
    cv2.imshow("Image", image)
    cv2.waitKey(args.wait)
    if args.save_images:
        cv2.imwrite(os.path.join(args.dest_folder, filenames[i]), image)

print('Completed in : ', round(time.time() - start), 'seconds')
