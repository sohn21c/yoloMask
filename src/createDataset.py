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

class createDataset(object):
    def __init__(self):
        pass
   
    def set_target(self, target):
        res = []
        targets = target.split(',')
        for item in targets:
            res.append(item)
        self.target = res

    def set_size(self, size):
        self.dtSize = size

    def load_labels(self, pathLabel):
        self.pathLabel = pathLabel
        self.labelList = os.listdir(pathLabel)

    def count_target(self):
        tally = {}
        for obj in self.target:
            tally[obj] = 0

        ind = 0
        for label in self.labelList:
            filename = self.pathLabel + label
            f = open(filename, 'r')
            content = f.read().split('\n')
            for line in content:
                items = line.split(' ')
                if items[0] in self.target:
                    tally[items[0]] += 1
            f.close()
            if ind % 100 == 0:
                print(f'[COUNT] {ind} of {len(self.labelList)} processed')
            ind += 1
        
        print('[COUNT] done counting targets in dataset')
        print(tally)

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
    for key, val in info.items():
        #exec(key + '=val')
        globals()[key] = val
    
    # body 
    mode = args['mode']
    if mode == 'train':
        c = createDataset()
        c.set_target(TARGET)
        c.load_labels(TRAIN_LABEL)
        c.count_target()

    elif mode == 'test':
        pass
    else: 
        pass

if __name__ == '__main__':
    main()
