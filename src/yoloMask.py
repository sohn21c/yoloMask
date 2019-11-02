"""
Author: James Sohn
Last Modified: 11/02/19

The code is to generate mask of an object processing and extracting an object from the video frames. It can be used to create custom dataset for object detection. One use case may be to use the code below to create set of object masks and add them to random background for YOLO dataset.

    Input: Video (.MOV used in the code)
    Output: Image files containing object mask
"""
import argparse
import cv2
import numpy as np
import os

class generateMask(object):
    def __init__(self):
        self.path = os.getcwd()

    def set_thresh(self, thresh):
        try:
            self.low = thresh[0]
            self.high = thresh[1]
        except AssertionError as error:
            print(error)
            print('Threshold should be two integer range of 0-255')

    def set_objName(self, obj_name):
        self.obj_name = obj_name

    def load_video(self, video_file):
        return cv2.VideoCapture(video_file)

    def create_mask(self, frame):
	# image processing
	gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
     	thresh = cv2.threshold(gray, self.low, self.high, cv2.THRESH_BINARY)[1]
        erode = cv2.erode(thresh, None, iterations=1)
        cnts = cv2.findContours(erode, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        cnts = get_contours(cnts)
        c = max(cnts, key=cv2.contourArea)
            
        # mask generation
        mask = np.zeros((frame.shape[0], frame.shape[1]))
        cv2.drawContours(mask, [c], -1, (1,0,0), cv2.FILLED)
            
        # bounding box
        extLeft = tuple(c[c[:, :, 0].argmin()][0])
        extRight = tuple(c[c[:, :, 0].argmax()][0])
        extTop = tuple(c[c[:, :, 1].argmin()][0])
        extBot = tuple(c[c[:, :, 1].argmax()][0])

	bbox_coord = (extLeft, extRight, extTop, extBot)
	
	return mask


def main():
    """
    Mode:
        - generate: generate mask
        - test: test threshold value
    """
    # parse arguments
    ap = argparse.ArgumentParser(description='Generate Object Mask From Video.')
    ap.add_argument("-m", "--mode", required=True, help="test or generate")
    ap.add_argument("-v", "--video", required=True, help="video files")
    ap.add_argument("-o", "--object", required=True, help="name of an object")
    ap.add_argument("-t", "--thresh", type=int, default="100 255", nargs='+', help="image extraction threshold. Range between 0-255")
    args = vars(ap.parse_args())

    # mode assertion
    assert (args['mode'] == 'test' or args['mode'] == 'generate'), 'Mode should be either \'test\' or \'generate\'.'
    
    # mode selection
    if args['mode'] == 'test':
        gen_mask = generateMask(args['video'])

    elif args['mode'] == 'generate':
        pass
    else:
        pass

if __name__ == '__main__':
    main()


