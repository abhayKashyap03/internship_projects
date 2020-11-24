import pandas as pd
import numpy as np
import cv2
import matplotlib.pyplot as plt
import os, glob
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('--path', required=True)
parser.add_argument('--image_path', required=True)
parser.add_argument('--out_dir', required=True)
args = parser.parse_args()

def addRect() :
    df = pd.read_csv(args.path)
    coord = df.iloc[:, 3:].to_numpy()

    x, y = [], []
    for i in range(coord.shape[0]) :
        for j in list((1, 3, 5, 7)) :
            y.append(coord[i][j])
        for j in list((0, 2, 4, 6)) :
            x.append(coord[i][j])
    
    x_p, y_p = [], []    
    for i in range(0, len(x), 4) :
        x_p.append(x[i:i+4])
    for i in range(0, len(y), 4) :
        y_p.append(y[i:i+4])

    names = df.iloc[:, 1].to_numpy()

    for i in range(df.shape[0]) :
        xmin = min(x_p[i])
        xmax = max(x_p[i])
        ymin = min(y_p[i])
        ymax = max(y_p[i])
    
        path = os.path.join(args.image_path, os.path.basename(names[i]))
        img = cv2.imread(path)
        
        cv2.putText(img, str(df.iloc[i, 2]), (int(xmin*img.shape[1] - 5), int(ymin*img.shape[0] - 5)), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 0), 3)
        cv2.rectangle(img, (int(xmin*img.shape[1]), int(ymin*img.shape[0])), (int(xmax*img.shape[1]), int(ymax*img.shape[0])), (0, 255, 0), 3, )
        cv2.imwrite(os.path.join(args.out_dir, os.path.basename(names[i])), img)
        


if os.path.exists(args.path) :
    if os.path.exists(args.image_path) :
        if os.path.exists(args.out_dir) :
            addRect()
        else :
            print("Output directory does not exist, creating new directory")
            os.mkdir(args.out_dir)
            addRect()
    else :
        print("Image directory does not exist")
else :
    print("CSV does not exist")