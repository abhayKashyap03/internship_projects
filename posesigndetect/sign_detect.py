import os, glob
import argparse
from tqdm import tqdm
import pandas as pd
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
from natsort import natsorted
from ast import literal_eval
from time import time
from estimator import ResEstimator
from network import CoordRegressionNetwork
from signdetection import *

parser = argparse.ArgumentParser(description='MobilePose Realtime Webcam.')
parser.add_argument('--inp_path', type=str, required=False, help='location or path where image/video is stored')
parser.add_argument('--out_dir', type=str, default='output', help='location or path where results have to be stored')
parser.add_argument('--model', type=str, default='resnet18', choices=['mobilenetv2', 'resnet18'], help='name of model to be used')
parser.add_argument('--type', choices=['img', 'vid', 'live'], type=str, default='img', help='type of input')
parser.add_argument('--cam', type=int, default=0)
parser.add_argument('--file')
parser.add_argument('--plot', type=str, default=False)
args = parser.parse_args()


start = time()

if not os.path.exists(args.out_dir):
    os.mkdir(args.out_dir)

joint_names = {key: value for key, value in MPIIPartMapping.__dict__.items() if
               not key.startswith('__') and not callable(key)}
joint_names = {k: v for k, v in sorted(joint_names.items(), key=lambda item: item[1])}
print(joint_names)

if not os.path.exists(os.path.join(args.out_dir, "graphs")):
    os.mkdir(os.path.join(args.out_dir, "graphs"))


def plot_vid(files, data):
    matplotlib.use('TkAgg')

    data = pd.read_csv(data).iloc[:, 1:].to_numpy().tolist()
    points = list(joint_names.keys())

    z = []
    for file in files:
        z.append(os.path.splitext(os.path.basename(file))[0])
    z = np.asarray(natsorted(z))

    frames = []
    for i in range(len(z)):
        frames.append(i)

    xy = data
    for i in range(16):
        x, y = [], []
        for j in range(len(z)):
            x.append(literal_eval(xy[j][i])[0] / 224)
            y.append(literal_eval(xy[j][i])[1] / 224)
        x, y = np.asarray(x), np.asarray(y)
        fig = plt.figure(figsize=(25, 25))
        ax = plt.axes(projection='3d')
        plt.title(points[i].replace('_', ' ').title() + " Coordinates (x,y) (Normalized)")
        ax.scatter3D(x[0], y[0], frames[0], c='r')
        ax.text(s="1", x=x[0], y=y[0], z=frames[0])
        ax.scatter3D(x[1:-1], y[1:-1], frames[1:-1])
        for k in range(1, len(z) - 1):
            ax.text(s=str(k + 1), x=x[k], y=y[k], z=frames[k])
        ax.scatter3D(x[-1], y[-1], frames[-1], c='y')
        ax.text(s=str(len(z)), x=x[-1], y=y[-1], z=frames[-1])
        ax.plot(x, y, frames)
        ax.set_zlabel("frame number", fontsize="x-large", fontstyle="oblique", fontweight="bold", labelpad=10)
        ax.set_ylabel("y coordinates", fontsize="x-large", fontstyle="oblique", fontweight="bold", labelpad=10)
        ax.set_xlabel("x coordinates", fontsize="x-large", fontstyle="oblique", fontweight="bold", labelpad=10)
        plt.savefig(os.path.join(args.out_dir, "graphs", list(joint_names.keys())[i] + ".png"))
        plt.show()


def plot_img(data):
    matplotlib.use('TkAgg')

    data = pd.read_csv(data).iloc[0, 1:].to_numpy().tolist()
    xy = data

    points = []
    for i in range(16):
        points.append(i)

    x, y = [], []
    for i in range(16):
        x.append(literal_eval(xy[i])[0] / 224)
        y.append(literal_eval(xy[i])[1] / 224)
    fig = plt.figure(figsize=(60, 60))
    ax = plt.axes(projection='3d')
    ax.set_xlim(min(x) - 0.1, max(x) + 0.1)
    ax.set_ylim(min(y) - 0.1, max(y) + 0.1)
    ax.set_zlim(0, 18)
    plt.title("Joints Coordinates (Normalized)")
    ax.scatter3D(x[0], y[0], points[0], c='r', label="Joint 1")
    ax.scatter3D(x[1:-1], y[1:-1], points[1:-1], label="Joints 2-15")
    ax.scatter3D(x[-1], y[-1], points[-1], c='coral', label="Joint 16")
    for key, value in joint_names.items():
        ax.text(s=key, x=x[value], y=y[value], z=points[value])
    ax.plot(x, y, points)
    ax.legend(loc='upper right')
    ax.set_xlabel("x coordinates", fontsize="x-large", fontstyle="oblique", fontweight="bold", labelpad=10)
    ax.set_ylabel("y coordinates", fontsize="x-large", fontstyle="oblique", fontweight="bold", labelpad=10)
    ax.set_zlabel("ID (joint) number", fontsize="x-large", fontstyle="oblique", fontweight="bold", labelpad=10)
    plt.show()
    plt.savefig("joints.png")


def detect(name, img, args_):
    # load the model
    model_path = os.path.join("models", args_.model + "_224_adam_best.t7")
    net = CoordRegressionNetwork(n_locations=16, backbone=args_.model).to("cpu")
    e = ResEstimator(model_path, net, 224)
    # predict keypoints
    humans = e.inference(img)
    # Comment below line if skeleton is not to be drawn :
    img = ResEstimator.draw_humans(img, humans, imgcopy=False)
    # detect sign
    sign = sign_detector(humans)
    # draw sign name on image
    draw_sign(img, sign)
    # add keypoints and img name to csv file ---> data storage
    humans = humans.tolist()
    cv2.imwrite(os.path.join(args_.out_dir, str(name) + '.jpg'), img)
    data = pd.read_csv(args_.file)
    data = data.append(pd.DataFrame([[str(name)] + humans], columns=data.columns))
    data.to_csv(os.path.join(args_.out_dir, "data.csv"), index=False, columns=data.columns)


if args.type == 'img':
    if args.file is None:
        data = pd.DataFrame(
            columns=['Image'] + list(joint_names.keys()))
        file = os.path.join(args.out_dir, "data.csv")
        data.to_csv(file, index=False, columns=data.columns)
        args.file = file
    img = cv2.resize(cv2.imread(args.inp_path), (224, 224))
    name = os.path.splitext(os.path.basename(args.inp_path))[0]
    detect(name, img, args)
    print("Result image and coordinates file stored in " + args.out_dir)
    if literal_eval(str(args.plot)):
        plot_img(args.file)


elif args.type == 'live':
    if args.file is None:
        data = pd.DataFrame(
            columns=['Frame'] + list(joint_names.keys()))
        file = os.path.join(args.out_dir, "data.csv")
        data.to_csv(file, index=False, columns=data.columns)
        args.file = file
    cam = cv2.VideoCapture(args.cam)
    c = 0
    while True:
        ret, img = cam.read()
        if img is None:
            break
        c += 1
        img = cv2.resize(img, (224, 224))
        detect(c, img, args)
        cv2.imshow('MobilePose Demo', img)
        if cv2.waitKey(1) == 27:  # ESC
            break
    cv2.destroyAllWindows()


elif args.type == 'vid':
    if args.file is None:
        data = pd.DataFrame(
            columns=['Frame'] + list(joint_names.keys()))
        file = os.path.join(args.out_dir, "data.csv")
        data.to_csv(file, index=False, columns=data.columns)
        args.file = file
    cam = cv2.VideoCapture(args.inp_path)
    c = 0
    while True:
        ret, img = cam.read()
        if ret is not True:
            break
        print(c)
        c += 1
        img = cv2.resize(img, (224, 224))
        detect(c, img, args)
    print("\n", "Converting to video...")
    video = cv2.VideoWriter(os.path.join(args.out_dir, "result.mp4"), cv2.VideoWriter_fourcc(*'mp4v'), 15, (224, 224))
    files = glob.glob(os.path.join(args.out_dir, '*.jpg'))
    files = natsorted(files)
    for file in tqdm(files):
        video.write(cv2.imread(file))
    video.release()
    print("Frames, result video and coordinates file stored in " + args.out_dir)
    if literal_eval(str(args.plot)):
        plot_vid(files, args.file)


print("Time taken : %d seconds" % round(time() - start))
