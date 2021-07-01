# MobilePose

MobilePose is a **Tiny** PyTorch implementation of single person 2D pose estimation framework. The aim is to provide the interface of the training/inference/evaluation, and the dataloader with various data augmentation options. And final trained model can satisfy basic requirements(speed+size+accuracy) for mobile device.

## Requirements

- Python 3.x
- PyTorch >= 1.0
- [dsntnn >= 1.0](https://github.com/anibali/dsntnn)

## Features

- [x] multi-thread dataloader with augmentations (dataloader.py)
- [x] training and inference (training.py)
- [x] performance evaluation (eval.py)
- [x] multiple models support (network.py)
- [x] ipython notebook visualization (demo.ipynb)
- [x] camera realtime display script (run_webcam.py)
- [x] sign detection from image, video, and realtime (sign_detect.py)

## Usage

1. Installation:

```shell
pip install -r requirements.txt
```

2. Training:

```shell
python training.py --model shufflenetv2 --gpu 0 --inputsize 224 --lr 1e-3 --batchsize 128 --t7 ./models/shufflenetv2_224_adam_best.t7
```

3. Evaluation

```shell
ln -s cocoapi/PythonAPI/pycocotools
cd cocoapi/PythonAPI && make

python eval.py --t7 ./models/resnet18_224_adam_best.t7 --model resnet18 --gpu 0
```

4. Web Camera Demo (Only pose estimation)
```shell
python run_webcam.py --model squeezenet --inp_dim 224 --camera 0
```

5. Identifying sign from image/video/live camera

```shell
python sign_detect.py --type {'img','vid', 'live'} --inp_path /path/to/image --out_dir /path/to/result --file path/to/file/storing/info  --plot False/True --model ['mobilenetv2', 'resnet18'] --cam int
```

Arguments :\
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
