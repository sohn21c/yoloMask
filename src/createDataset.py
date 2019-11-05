"""
Author: James Sohn
Last Modified: 11/04/19

This script is to create a dataset to train YOLO by adding custom object masks to random backgrounds while rotating, scaling and jittering color. For more details about the code, please visit the github repo listed below.

https://github.com/sohn21c/yoloMask
"""
import argparse
import cv2
import numpy as np
import os
import util


def main():
    """
    Mode:
        - train:    create train set
        - test:     create test dataset
        - count:    count the number of images of objects of interest
    """
    # parse arguments
    ap = argparse.ArgumentParser(description='Generate Custom Object Dataset From Mask.')
    ap.add_argument('-m', '--mode', required=True, help='train, test or count')
    ap.add_argument('-c', '--cfg', required=True, help='path to cfg file')
    args = vars(ap.parse_args())

    # mode assertion
    assert(args['mode'] in ['train', 'test', 'count']), 'Mode should be one of the followings: \'train\', \'test\', \'count\''

    # parse configuration file
    info = util.parse_cfg(args['cfg'])



if __name__ == '__main__':
    main()
