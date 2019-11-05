# Masks for custom Objects

**This is Part 1 of 2 to create custom dataset for YOLO. You'll find the link to the Part 2 as soon as I upload**

## Objective
This script was to help easily create a object detection data set by putting a mask of object of interest to random backgrounds. Instead of taking many pictures of an object of interest, one can record a quick video of an object and extract the relevant information at different view points by recording the moving objects in the video.

## Contents
1. [Envionment Setup](#environment-setup)
2. [Run](#run)
3. [Output](#output)
4. [What's missing](#what's-missing)
5. [Script](#script)

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
        <img src='https://github.com/sohn21c/yoloMask/blob/master/img/IMG_1578.jpg?raw=true' width='300'>  
  
- Argument
    ```
    -m MODE,   --mode   MODE   test or generate
    -v VIDEO,  --video  VIDEO  video file
    -o OBJECT, --object OBJECT name of an object
    -t THRESH, --thresh THRESH image extraction threshold. Range between 0-255
    ```

- Command run
    - test mode:  
        to test image extraction threshold. One image will be displayed for verification  
        `python yoloMask.py -m test -v IMG_0341.MOV -o hand -t 100 255`  
        
    - generate mode:  
        once threshold is set, one can run the command below to process the video in its entirety generating multiple masks for an object   
        `python yoloMask.py -m generate -v IMG_0341.MOV -o hand -t 100 255`  
  
## Output
- Mask of an image  
    - Output Mask  
        <img src='https://github.com/sohn21c/yoloMask/blob/master/img/output1.png?raw=true' width='300'>  
        
    - Sample image with bbox. **Not an output**  
        <img src='https://github.com/sohn21c/yoloMask/blob/master/img/output2.png?raw=true' width='300'>  
        
- Text file with bounding box coordinates  
    ```
    <path-to-repo>/data/mask/hand_mask_0.jpg,(577, 132),(1653, 937)
    <path-to-repo>/data/mask/hand_mask_1.jpg,(544, 100),(1696, 972)
    ...
    ```
## Script
- [This script here](https://github.com/sohn21c/yoloMask/blob/master/scripts/hand_mask_generation.ipynb) shows what each line of the code does with in-line pictures as well. It'd help you understand the code.  
  
## What's missing  
- Control over the number of masks  
    Currently, the feature generates a mask per 1/3 sec (10hz). If one wants to manipulate the number of generated masks, please modify the part [here](https://github.com/sohn21c/yoloMask/blob/111e4f4c0dce0710d9d7f285df7a96ed8023eb43/src/yoloMask.py#L139)  

- Feature to check the quality of mask and get rid of the bad  
    There's a high chance that your first couple frames and the last from the video record may not have captured the object properly and produced the bad mask. You need to get rid of them manually.  
    
