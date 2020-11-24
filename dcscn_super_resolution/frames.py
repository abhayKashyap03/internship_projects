# Importing all necessary libraries 
import cv2 
import os 
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('--video_path', required=True)
parser.add_argument('--frame_out_dir', required=True)
args = parser.parse_args()
# Read the video from specified path 
cam = cv2.VideoCapture(args.video_path)

# frame 
currentframe = 0

while(True): 
	
	# reading from frame 
    ret, frame = cam.read()
    
    if ret :
        name = args.frame_out_dir + '/' + str(currentframe) + '.jpg'
        print("Creating frame %d" % currentframe)
        cv2.imwrite(name, frame)
        
        currentframe += 1
        
    else :
        break
 
# Release all space and windows once done 
cam.release() 
cv2.destroyAllWindows() 
