import cv2, os, argparse

parser = argparse.ArgumentParser()
parser.add_argument('--video', required=True)
parser.add_argument('--out_dir', required=True)
args = parser.parse_args()

if not os.path.exists(args.out_dir) :
    os.mkdir(args.out_dir)

vidcap = cv2.VideoCapture(args.video)
def getFrame(sec):
    vidcap.set(cv2.CAP_PROP_POS_MSEC,sec*1000)
    hasFrames,image = vidcap.read()
    if hasFrames:
        cv2.imwrite(os.path.join(args.out_dir, "Frame"+str(count)+".jpg"), image)     # save frame as JPG file
    return hasFrames
sec = 0
frameRate = (0.5) #//it will capture image in each 0.5 second
count=1
success = getFrame(sec)
while success:
    count = count + 1
    sec = sec + frameRate
    sec = round(sec, 2)
    success = getFrame(sec)
