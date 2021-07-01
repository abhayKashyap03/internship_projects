'''
File: detect_sign.py
Project: MobilePose-PyTorch
File Created: 10th April 2020
Author: Abhay Kashyap (abhay.kashyap95@gmail.com)
'''

import argparse
import logging
import time
import cv2
import os
import numpy as np
import pandas as pd
# import matplotlib
# matplotlib.use('Agg')
import matplotlib.pyplot as plt

from estimator import ResEstimator
from networks import *
from network import CoordRegressionNetwork
from dataloader import crop_camera
from signdetection import *

parser = argparse.ArgumentParser(description='MobilePose Realtime Webcam.')
parser.add_argument('--model', type=str, default='resnet18', choices=['mobilenetv2', 'resnet18'])
parser.add_argument('--inp_dim', type=int, default=224, help='input size')
parser.add_argument('--inp_path', type=str, required=True)
parser.add_argument('--output_dir', type=str, default="output")
parser.add_argument('--type', choices=['img', 'vid'], type=str, default='img')
parser.add_argument('--file')
parser.add_argument('--plot', type=str, default=False)
args = parser.parse_args()

if os.path.exists(args.output_dir) :
    pass
else :
    print("directory does not exist. Creating directory...")
    os.mkdir(args.output_dir)

# load the model
model_path = os.path.join("./models", args.model+"_%d_adam_best.t7"%args.inp_dim)
net = CoordRegressionNetwork(n_locations=16, backbone=args.model).to("cpu")
e = ResEstimator(model_path, net, args.inp_dim)

img = cv2.resize(cv2.imread(args.inp_path), (args.inp_dim, args.inp_dim))
humans = e.inference(img)
# Comment below line if skeleton is not to be drawn :
img = ResEstimator.draw_humans(img, humans, imgcopy=False)

sign = sign_detector(humans)
draw_sign(img, sign)
humans = humans.tolist()

cv2.imwrite(os.path.join(args.output_dir, args.inp_path.split("/")[-1]), img)

data = pd.read_csv(args.file)
data = data.append(pd.DataFrame([[str(os.path.splitext(os.path.basename(args.inp_path))[0])]+humans], columns=data.columns))
data.to_csv(os.path.join(args.output_dir, "data.csv"), index=False, columns=data.columns)
