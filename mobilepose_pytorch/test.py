from enum import IntEnum
import os, glob
import argparse
from tqdm import tqdm
import pandas as pd
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
from natsort import natsorted
from ast import literal_eval

from signdetection import *

parser = argparse.ArgumentParser(description='MobilePose Realtime Webcam.')
parser.add_argument('--inp_path', type=str, required=True)
parser.add_argument('--output_dir', type=str, default="output")
parser.add_argument('--type', choices=['img', 'vid'], type=str, default='img')
parser.add_argument('--file')
parser.add_argument('--plot', type=str, default=False)
args = parser.parse_args()

if not os.path.exists(args.output_dir) :
    os.mkdir(args.output_dir)

joint_names = {key : value for key, value in MPIIPartMapping.__dict__.items() if
               not key.startswith('__') and not callable(key)}
joint_names = {k : v for k, v in sorted(joint_names.items(), key=lambda item : item[1])}
print(joint_names)

if not os.path.exists(os.path.join(args.output_dir, "graphs")) :
    os.mkdir(os.path.join(args.output_dir, "graphs"))

def plot_vid(files, data) :
    matplotlib.use('TkAgg')

    data = pd.read_csv(data).iloc[:, 1:].to_numpy().tolist()
    points = list(joint_names.keys())

    z = []
    for file in files :
        z.append(os.path.splitext(os.path.basename(file))[0])
    z = np.asarray(natsorted(z))

    frames = []
    for i in range(len(z)) :
        frames.append(i)

    xy = data
    for i in range(16) :
        x, y = [], []
        for j in range(len(z)) :
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
        plt.savefig(os.path.join(args.output_dir, "graphs", list(joint_names.keys())[i] + ".png"))
        plt.show()


def plot_img(data) :
    matplotlib.use('TkAgg')

    data = pd.read_csv(data).iloc[0, 1:].to_numpy().tolist()
    xy = data

    points = []
    for i in range(16) :
        points.append(i)

    x, y = [], []
    for i in range(16) :
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
    for key, value in joint_names.items() :
        ax.text(s=key, x=x[value], y=y[value], z=points[value])
    ax.plot(x, y, points)
    ax.legend(loc='upper right')
    ax.set_xlabel("x coordinates", fontsize="x-large", fontstyle="oblique", fontweight="bold", labelpad=10)
    ax.set_ylabel("y coordinates", fontsize="x-large", fontstyle="oblique", fontweight="bold", labelpad=10)
    ax.set_zlabel("ID (joint) number", fontsize="x-large", fontstyle="oblique", fontweight="bold", labelpad=10)
    plt.show()
    plt.savefig("joints.png")


if args.type == 'img' :
    if args.file is None :
        data = pd.DataFrame(
            columns=['Image']+list(joint_names.keys()))
        file = os.path.join(args.output_dir, "data.csv")
        data.to_csv(file, index=False, columns=data.columns)
        args.file = file

    os.system("python detect_sign.py --inp_path "+args.inp_path+ " --output_dir "+args.output_dir+" --type "+args.type+" --file "+args.file+" --plot "+str(args.plot))

    print("Result image and coordinates file stored in " + args.output_dir)

    if literal_eval(str(args.plot)) :
        plot_img(args.file)

elif args.type == 'vid' :
    files = glob.glob(args.inp_path + "/*.jpg")
    files = natsorted(files)

    if args.file is None :
        data = pd.DataFrame(
            columns=['Frame']+list(joint_names.keys()))
        file = os.path.join(args.output_dir, "data.csv")
        data.to_csv(file, index=False, columns=data.columns)
        args.file = file

    for path in tqdm(files) :
        os.system("python detect_sign.py --inp_path "+path+ " --output_dir "+args.output_dir+" --type "+args.type+" --file "+args.file+" --plot "+str(args.plot))

    os.system('python convert2.py --pathIn ' + args.output_dir + ' --pathOut ' + args.output_dir)

    print("Frames, result video and coordinates file stored in " + args.output_dir)

    if literal_eval(str(args.plot)) :
        plot_vid(files, args.file)
