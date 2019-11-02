"""
Author: James Sohn
Last Modified: 11/02/2019

This script contains a number of helper functions
"""
import cv2
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import numpy as np

def showimg(img, bgr=False, gray=False):
    """
    shows the image, being handled with opencv, in-line with matplotlib
    
    args:
        gray: Grayscale option (True or False)
        bgr: opencv flips RGB to BGR (True or False)
    """
    # feel free to resize the figure size as necessary
    plt.figure(figsize = (8, 10))
    
    if bgr:
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        imgplot = plt.imshow(img)
    elif gray:
        imgplot = plt.imshow(img, cmap='gray')
    else:    
        imgplot = plt.imshow(img)
    plt.show()

def showimg_file(file):
    """
    displays the image directly from the file, in-line with matplotlib
    """
    img = mpimg.imread(file) 
    # feel free to resize the figure size as necessary
    plt.figure(figsize = (8, 10))
    imgplot = plt.imshow(img)
    plt.show()

def get_contours(cnts):
    """
    checks the openCV version and returns the contours 
    """
    # if '2', it's OpenCV v2.4 or v4
    if len(cnts) == 2:
        cnts = cnts[0]
    # if '3', it's OpenCV v3,
    elif len(cnts) == 3:
        cnts = cnts[1]
    # Otherwise, raise error
    else:
        raise Exception(("Unknown Contour Length, Check the OpenCV version"))
    
    return cnts

def rotate_bound(image, angle):
    """
    rotates an image around the centor point avoiding the unwanted translation
    """
    # grab the dimensions of the image and then determine the
    # center
    (h, w) = image.shape[:2]
    (cX, cY) = (w / 2, h / 2)

    # grab the rotation matrix (applying the negative of the
    # angle to rotate clockwise), then grab the sine and cosine
    # (i.e., the rotation components of the matrix)
    M = cv2.getRotationMatrix2D((cX, cY), -angle, 1.0)
    cos = np.abs(M[0, 0])
    sin = np.abs(M[0, 1])

    # compute the new bounding dimensions of the image
    nW = int((h * sin) + (w * cos))
    nH = int((h * cos) + (w * sin))

    # adjust the rotation matrix to take into account translation
    M[0, 2] += (nW / 2) - cX
    M[1, 2] += (nH / 2) - cY

    # perform the actual rotation and return the image
    return cv2.warpAffine(image, M, (nW, nH))

def resize_img(img, target_width):
    """
    resizes the hand mask to target width
    """
    (h, w) = img.shape[:2]
    r  = h / w
    dim = (target_width, int(target_width * r))
    resized = cv2.resize(img, dim, interpolation=cv2.INTER_AREA)
    
    return resized


