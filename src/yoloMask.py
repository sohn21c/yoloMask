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
import util

class generateMask(object):
    def __init__(self, vis=False):
        self.path = os.getcwd()
        self.vis = vis  # flag for visualization

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
        cnts = util.get_contours(cnts)
        c = max(cnts, key=cv2.contourArea)
            
        # mask generation
        mask = np.zeros((frame.shape[0], frame.shape[1]))
        cv2.drawContours(mask, [c], -1, (1,0,0), cv2.FILLED)
            
        # bounding box
        extLeft = tuple(c[c[:, :, 0].argmin()][0])
        extRight = tuple(c[c[:, :, 0].argmax()][0])
        extTop = tuple(c[c[:, :, 1].argmin()][0])
        extBot = tuple(c[c[:, :, 1].argmax()][0])
        bbox_coord = (extLeft[0], extTop[1], extRight[0], extBot[1])
       
        # apply mask
        masked = frame.copy()
        for i in range(3):
            masked[:, :, i] *= (mask != 0)

        # show image if in test mode
        if self.vis:
            print('visualize')
            cv2.drawContours(frame, [c], -1, (255, 255, 255), 0)
            cv2.rectangle(frame, (extLeft[0], extTop[1]), (extRight[0], extBot[1]), (0, 0, 255), thickness=10) # (0,0,255) is red for opencv
                
            util.showimg(masked, bgr=True)
            util.showimg(frame, bgr=True)
	
        return masked, bbox_coord

    def save_mask(self, mask, ind):
        path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'data'))
        path = path + '/' + 'mask/'
        if not os.path.exists(path):
           os.makedirs(path)
        self.maskname = path + f'{self.obj_name}_mask_{int(ind/10)}.jpg'
        cv2.imwrite(self.maskname, mask)

    def save_bbox(self, bbox_coord):
        path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'data'))
        path = path + '/' + 'mask/'
        bbox_test = path + f'{self.obj_name}_mask_bbox.txt'
        f = open(bbox_test, 'a+')
        f.write(f'{self.maskname},{(bbox_coord[0], bbox_coord[1])},{(bbox_coord[2], bbox_coord[3])}\n')


def main():
    """
    Mode:
        - generate: generate mask
        - test: test threshold value
    """
    # parse arguments
    ap = argparse.ArgumentParser(description='Generate Object Mask From Video.')
    ap.add_argument("-m", "--mode", required=True, help="test or generate")
    ap.add_argument("-v", "--video", required=True, help="video file")
    ap.add_argument("-o", "--object", required=True, help="name of an object")
    ap.add_argument("-t", "--thresh", type=int, default="100 255", nargs='+', help="image extraction threshold. Range between 0-255")
    args = vars(ap.parse_args())

    # mode assertion
    assert (args['mode'] == 'test' or args['mode'] == 'generate'), 'Mode should be either \'test\' or \'generate\'.'
    
    # get path
    PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'data', 'video')) 

    # video file
    vid_file = PATH + '/' + args['video']

    # mode selection
    if args['mode'] == 'test':
        print('[INFO] test mode initiated')
        vis = True # visualization flag
        test_mask = generateMask(vis)
        test_mask.set_thresh(args['thresh'])

        # test on the first frame
        cap = test_mask.load_video(vid_file)
        print('[INFO] video file loaded')
        while True:
            ret, frame = cap.read()
            if ret:
                _, _ = test_mask.create_mask(frame)
            break    
        cap.release()

    elif args['mode'] == 'generate':
        print('[INFO] generate mode initiated')
        gen_mask = generateMask()
        gen_mask.set_objName(args['object'])
        gen_mask.set_thresh(args['thresh'])

        # iterate through all the frames
        cap = gen_mask.load_video(vid_file)
        print('[INFO] video file loaded')
        ind = 0 # frame index
        while True:
            ret, frame = cap.read()
            if ret and ind % 10 == 0:   # 3 pics/sec
                masked, bbox = gen_mask.create_mask(frame)
                gen_mask.save_mask(masked, ind)
                gen_mask.save_bbox(bbox)
                print(f'[INFO] mask #{int(ind/10)} saved') 
            ind += 1
            if not ret:
                break
        cap.release()
    
if __name__ == '__main__':
    main()


