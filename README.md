# Masks for custom Objects

**This is Part 1 of 2 to create custom dataset for YOLO. You'll find the link to the Part 2 as soon as I upload**

## Objective
This script was created to help easily create a object detection data set by putting a mask of object of interest to random backgrounds. Instead of taking many pictures of an object of interest, we can record a quick video of an object and extract the relevant information at different view points.

## Contents
1. [Envionment Setup](#environment-setup)
2. [Run](#run)
3. [Output](#output)
4. [What's missing](#what's-missing)

## Environment setup
This code has been tested on Ubuntu 18.04, Python 3.7  
All you need is as follows:  
```
opencv
numpy
matplotlib
```

## Run
- Clone the repo
`git clone https://github.com/sohn21c/yoloMask && cd yoloMask`  

- Create directory for data
`mkdir data && mkdir data/video`  

- Put video file in the `data/video` dir  
 - **You can change the intensity threshold to find the object in the frame but it is recommended to record a video of an object with black background. It'd generally work well if you have the background of contrasting color**  
 - Screeshot of video shown below   
  <img src='https://github.com/sohn21c/yoloMask/blob/master/img/IMG_1578.jpg?raw=true' width='200'>  
  
- Argument
```
-m MODE,   --mode   MODE   test or generate
-v VIDEO,  --video  VIDEO  video file
-o OBJECT, --object OBJECT name of an object
-t THRESH, --thresh THRESH image extraction threshold. Range between 0-255
```

- Command run
 - test mode: to test image extraction threshold. One image will be displayed for verification
  `python yoloMask.py -m test -v IMG_0341.MOV -o hand -t 100 255`  
 - generate mode: once threshold is set, one can run the command below to process the video in its entirety generating multiple masks for an object  
  `python yoloMask.py -m generate -v IMG_0341.MOV -o hand -t 100 255`  
  
## Output
- Mask of an image

