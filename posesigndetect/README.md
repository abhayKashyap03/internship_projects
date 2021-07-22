# PoseSignDetect

PoseSignDetect is an algorithm for detecting rescue and naval signals from human poses in images, videos, and live streams.
The project is based on pose estimation (MobilePose) to detect the pose of the person in the input media and determine the signal using trigonoetric operations. <br>
The deep learning model gives joints' keypoints as output (predictions) and the pose is determined by calculating angles between keypoints to identify the signal. <br>
This project uses ResNet and MobileNet, giving it speed without compromising accuracy. This makes it possible to implement the project on mobile devices and edge devices, and apply in real life scenarios without the need of bulk computer equipments. <br>

## Requirements

- Python 3.x
- PyTorch >= 1.0
- dsntnn >= 1.0

## Features

- [x] multi-thread dataloader with augmentations (dataloader.py)
- [x] training and inference (training.py)
- [x] performance evaluation (eval.py)
- [x] multiple models support (network.py)
- [x] ipython notebook visualization (demo.ipynb)
- [x] camera realtime display script (run_webcam.py)
- [x] sign detection from image, video, and realtime (sign_detect.py)

## Usage

1. Requirements/Dependencies Installation:

```shell
pip install -r requirements.txt
```

2. Training:

```shell
python training.py --model ['mobilenetv2', 'resnet18'] --gpu int --inputsize int --lr int --batchsize int --t7 ./models/['mobilenetv2', 'resnet18']_224_adam_best.t7
```

3. Evaluation

```shell
ln -s cocoapi/PythonAPI/pycocotools
cd cocoapi/PythonAPI && make

python eval.py --t7 ./models/['mobilenetv2', 'resnet18']_224_adam_best.t7 --model ['mobilenetv2', 'resnet18'] --gpu int
```

4. Web Camera Demo (Only pose estimation)
```shell
python run_webcam.py --model ['mobilenetv2', 'resnet18'] --inp_dim 224 --camera int
```

5. Identifying sign from image/video/live camera

```shell
python sign_detect.py --type ['img', 'vid', 'live'] --inp_path /path/to/image --out_dir /path/to/result --file path/to/file/storing/info  --plot False/True --model ['mobilenetv2', 'resnet18'] --cam int
```

Arguments :\
gpu : number of the GPU to be used (usually '0' for primary GPU or if using single GPU)
t7 : model path (models/.....)
lr : learning rate of model
type : type of input - image, video or live camera\
inp_path : location or path where image/video is stored; argument not required if input type is live camera\
out_dir : location or path where results have to be stored\
model : name of model to be used - 'resnet18' or 'mobilenetv2'; resnet18 gives best results\
cam : camera to be used for live (required only if input is live type)\
file : file to store skeleton (keypoints) information\
plot : whether or not points should be plotted
    
Default model is resnet18, can be changed to user requirement, options are resnet18 and mobilenetv2\
Default output path is the 'output' folder, can be changed to user requirement

## Contributors

MobilePose original repository is developed and maintained by [Yuliang Xiu](http://xiuyuliang.cn/about/), [Zexin Chen](https://github.com/ZexinChen) and [Yinghong Fang](https://github.com/Fangyh09).
