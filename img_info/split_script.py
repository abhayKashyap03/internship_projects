import os
import ast
import sys
import shutil
import random
import argparse
import pandas as pd
from time import time


def separate_folder(data_, dest_, args_):
    folder = args_.image_folder
    data = pd.read_csv(args_.csv_path)
    train_files_, train_folder = data_[0], dest_[0]
    test_files_, test_folder = data_[1], dest_[1]
    val_files_, val_folder = data_[2], dest_[2]

    for file_ in train_files_:
        class_ = data['class'][data['filename'] == file_].to_numpy()[0]
        if args_.class_folders:
            shutil.copy(os.path.join(folder, file_), os.path.join(train_folder, class_))
        else:
            shutil.copy(os.path.join(folder, file_), train_folder)

    for file_ in test_files_:
        class_ = data['class'][data['filename'] == file_].to_numpy()[0]
        if args_.class_folders:
            shutil.copy(os.path.join(folder, file_), os.path.join(test_folder, class_))
        else:
            shutil.copy(os.path.join(folder, file_), test_folder)

    for file_ in val_files_:
        class_ = data['class'][data['filename'] == file_].to_numpy()[0]
        if args_.class_folders:
            shutil.copy(os.path.join(folder, file_), os.path.join(val_folder, class_))
        else:
            shutil.copy(os.path.join(folder, file_), val_folder)


parser = argparse.ArgumentParser()
parser.add_argument('--image_folder', type=str, required=True, help='Location where images are stored')
parser.add_argument('--csv_path', type=str, required=True, help='Location of CSV file')
parser.add_argument('--separate_folders', type=ast.literal_eval, required=False, default=True, help='Create new folders for each split or not')
parser.add_argument('--class_folders', type=ast.literal_eval, required=False, default=False, help='Create new subfolders for each class or not')
parser.add_argument('--dest_folder', type=str, required=False, help='Location to store images in respective folders after split')
parser.add_argument('--train_size', type=float, required=True, help='Fraction of training images')
parser.add_argument('--test_size', type=float, required=True, help='Fraction of test images')
parser.add_argument('--val_size', type=float, required=True, help='Fraction of validation images')
parser.add_argument('--shuffle', type=ast.literal_eval, required=False, default=True, help='Shuffle dataset before splitting')
args = parser.parse_args()

start = time()
ROOT = ''
train_size = args.train_size
test_size = args.test_size
val_size = args.val_size
if (train_size+test_size+val_size > 1) :
    print("Invalid split sizes. Input valid train, test, and val split sizes (must add up to 1)")
    sys.exit()

if os.path.exists(args.image_folder):
    ROOT = os.path.split(args.image_folder)[0]

data = pd.read_csv(args.csv_path)
filenames = list(set(data['filename']))
x = len(filenames)
classes = list(set(data['class']))
if args.shuffle:
    random.shuffle(filenames)

train_size, test_size, val_size = round(train_size * x), round(test_size * x), round(val_size * x)
train_files, test_files, val_files = filenames[:train_size], filenames[train_size:(train_size + test_size)], \
                                     filenames[-val_size:]

columns = data.columns
train_ = [pd.DataFrame(data[data['filename'].str.contains(file)].to_numpy().tolist(), columns=columns)
          for file in train_files]
train_csv = pd.concat(train_)

test_ = [pd.DataFrame(data[data['filename'].str.contains(file)].to_numpy().tolist(), columns=columns)
         for file in test_files]
test_csv = pd.concat(test_)

val_ = [pd.DataFrame(data[data['filename'].str.contains(file)].to_numpy().tolist(), columns=columns)
        for file in val_files]
val_csv = pd.concat(val_)

train_csv_classes, test_csv_classes, val_csv_classes = {}, {}, {}

if args.separate_folders:
    if args.dest_folder is None:
        args.dest_folder = ROOT
    if args.dest_folder is not None and not os.path.exists(args.dest_folder):
        print("Folder does not exist, creating directory...")
        os.makedirs(args.dest_folder)
    if not os.path.exists(os.path.join(args.dest_folder, 'train')):
        os.mkdir(os.path.join(args.dest_folder, 'train'))
    if not os.path.exists(os.path.join(args.dest_folder, 'test')):
        os.mkdir(os.path.join(args.dest_folder, 'test'))
    if not os.path.exists(os.path.join(args.dest_folder, 'val')):
        os.mkdir(os.path.join(args.dest_folder, 'val'))
    if args.class_folders:
        for class_ in classes:
            if not os.path.exists(os.path.join(args.dest_folder, 'train', class_)):
                os.makedirs(os.path.join(args.dest_folder, 'train', class_))
            train_csv_classes[class_] = train_csv.loc[train_csv['class'] == class_]
            if not os.path.exists(os.path.join(args.dest_folder, 'test', class_)):
                os.makedirs(os.path.join(args.dest_folder, 'test', class_))
            test_csv_classes[class_] = test_csv.loc[test_csv['class'] == class_]
            if not os.path.exists(os.path.join(args.dest_folder, 'val', class_)):
                os.makedirs(os.path.join(args.dest_folder, 'val', class_))
            val_csv_classes[class_] = val_csv.loc[val_csv['class'] == class_]

    dest = [os.path.join(args.dest_folder, 'train'), os.path.join(args.dest_folder, 'test'),
            os.path.join(args.dest_folder, 'val')]
    data = [train_files, test_files, val_files]
    separate_folder(data, dest, args)


if args.separate_folders:
    if args.class_folders:
        for class_ in classes:
            train_csv_classes[class_].to_csv(os.path.join(args.dest_folder, 'train', class_, class_+'.csv'), index=False)
            test_csv_classes[class_].to_csv(os.path.join(args.dest_folder, 'test', class_, class_+'.csv'), index=False)
            val_csv_classes[class_].to_csv(os.path.join(args.dest_folder, 'val', class_, class_+'.csv'), index=False)
    else:
        train_csv.to_csv(os.path.join(args.dest_folder, 'train', 'train_csv.csv'), index=False)
        test_csv.to_csv(os.path.join(args.dest_folder, 'test', 'test_csv.csv'), index=False)
        val_csv.to_csv(os.path.join(args.dest_folder, 'val', 'val_csv.csv'), index=False)
else:
    train_csv.to_csv(os.path.join(ROOT, 'train_csv.csv'), index=False)
    test_csv.to_csv(os.path.join(ROOT, 'test_csv.csv'), index=False)
    val_csv.to_csv(os.path.join(ROOT, 'val_csv.csv'), index=False)

print('Completed in : ', round(time() - start), 'seconds')
