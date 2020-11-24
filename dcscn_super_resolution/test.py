import os
import argparse
import sys

parser = argparse.ArgumentParser()
parser.add_argument('--video_path', required=True)
parser.add_argument('--frame_out_dir', required=True)
parser.add_argument('--video_out_dir', required=True)

args = parser.parse_args()

if os.path.isfile(args.video_path) == False :
    print("File does not exist")
    sys.exit()

if os.path.isdir(args.video_out_dir) == False :
    print("Directory does not exist. Making directory...")
    os.mkdir(args.video_out_dir)

if os.path.isdir(args.frame_out_dir) == False :
    print("Directory does not exist. Making directory...")
    os.mkdir(args.frame_out_dir)

os.system('python frames.py --video_path '+args.video_path + ' --frame_out_dir '+args.frame_out_dir)

for i in range(len(os.listdir(args.frame_out_dir))) :
    img = args.frame_out_dir+"/"+str(i)+".jpg"
    os.system('python sr.py --file='+img)
    
os.system('python sr_video.py --frame_path '+args.frame_out_dir+' --out_dir '+args.video_out_dir)
