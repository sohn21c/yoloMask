"""
Author: James Sohn
Last Modified: 11/04/19

This script is to create a dataset to train YOLO by adding custom object masks to random backgrounds while rotating, scaling and jittering color. For more details about the code, please visit the github repo listed below.

https://github.com/sohn21c/yoloMask
"""
import argparse
import cv2
import matplotlib.image as mpimg
import numpy as np
import os
import util

class createDataset(object):
    def __init__(self):
        pass

    def add_mask(self, bg, mask):
        """adds processed mask to the backround"""
        # if mask is to tall for the background image, decrease the size by 50%
        if bg.shape[0] < mask.shape[0]:
            mask = cv2.resize(mask, (int(0.5*mask.shape[0]), int(0.5*mask.shape[1])), interpolation=cv2.INTER_AREA)
        h_mask, w_mask = mask.shape[:2]
        h, w = bg.shape[:2]
        
        # select random location for mask
        h_rand = np.random.rand() * 0.9
        h_rand = np.clip(h_rand, 0, 1.0 - h_mask/h)
        h_update = int(h_rand * h)
        w_rand = np.random.rand() * 0.9
        w_rand = np.clip(w_rand, 0, 1.0 - w_mask/w)
        w_update = int(w_rand * w)
        
        # define filter for a mask
        filt = (mask == 0)
        
        # place the mask in the bg img
        mod = bg.copy()
        mod[h_update:h_update+h_mask, w_update:w_update+w_mask, :] *= filt
        mod[h_update:h_update+h_mask, w_update:w_update+w_mask, :] += mask
        
        # yolo dim for mask
        locy = (h_update+h_update+h_mask)/2/h
        locx = (w_update+w_update+w_mask)/2/w
        sizey = (h_mask/h)
        sizex = (w_mask/w)
        
        dim = [locx, locy, sizex, sizey]
        
        return mod, dim

    def choose_mask(self, bboxFile):
        """randomly chooses the object mask"""
        f = open(bboxFile, 'r')
        content = f.read().split('\n')
        ind = np.random.randint(len(content) - 1)
        line = content[ind]
        words = line.split(',')

        maskFile = words[0]
        maskCoord = []

        for item in words[1:]:
            item = util.strip_paren(item)
            item = item.lstrip().rstrip()
            maskCoord.append(item)

        f.close()

        return maskFile, maskCoord

    def color_jitter(self, img):
        """randomly changes brightness and contrast of an image"""
        # define filter not to distort the background
        filt = (img != 0)
        
        a = np.random.uniform(0.5, 1.5)
        b = np.random.uniform(-100, 100)
        img = (a * img + b).astype(np.int64)
        img = np.clip(img, 0, 255)
        img *= filt

        return img
        
    def count_target(self):
        """counts the number of objects for detection in MS-COCO dataset"""
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

    def create(self):
        """create dataset"""
        new_image = 0   # counter
        fnewList = open(self.detList, 'w')

        ind = 0 # for-loop counter
        for ind in range(len(self.labelList)):
            labelName = self.pathLabel + self.labelList[ind]
            flabel = open(labelName, 'r')
            content = flabel.read().split('\n')
            change = False  # change flag 
            newLabel = self.detLabel + self.prefix + f'{ind}.txt'
 
            # object in image in target object list
            for line in content:
                items = line.split(' ')

                if items[0] in self.target:
                    _x, _y, _w, _h = float(items[1]), float(items[2]), float(items[3]), float(items[4])
                    tx = _x - _w/2
                    ty = _y - _h/2
                    bx = _x + _w/2
                    by = _y + _h/2

                    # decrease the bbox if it steps outside the image
                    while not (tx >= 0.0 and bx <= 1.0 and ty >= 0.0 and by <= 1.0):
                        _w *= 0.95
                        _h *= 0.95
                        tx = _x - _w/2
                        ty = _y - _h/2
                        bx = _x + _w/2
                        by = _y + _h/2

                    fnewLabel = open(newLabel, 'a')
                    items[0] = self.conversion[items[0]]
                    items[3] = str(_w)
                    items[4] = str(_h)
                    newLine = " ".join(items)
                    fnewLabel.write(newLine+'\n')
                    fnewLabel.close()

                    change = True # change flag

            # object in image NOT in target object list
            if not change and new_image < (self.dtSize - 1):
                human = False # human flag
                flabel = open(labelName, 'r')
                content = flabel.read().split('\n')
                # if human presents in image, pass
                for line in content:
                    items = line.split(' ')
                    if items[0] == '0':
                        human = True

                if not human:
                    imageName = labelName.split('labels')
                    imageName = imageName[0] + 'images' + imageName[-1]
                    imageName = imageName.split('.txt')
                    imageName = imageName[0] + '.jpg'

                    bg = mpimg.imread(imageName)
                    if len(bg.shape) == 3:
                        mask, coord = self.choose_mask(BBOX_TXT)
                        ratio = np.random.rand()
                        ratio *= 0.5
                        ratio = np.clip(ratio, 0.1, 0.5)
                        targetWidth = int(ratio * bg.shape[1])
                        rot = np.random.randint(4) * 90
                        resized, shape = self.process_mask(mask, coord, targetWidth, rot)
                        resized = self.color_jitter(resized)
                        resized = resized.astype(np.uint8)
                        result, dim = self.add_mask(bg, resized)

                        fnewLabel = open(newLabel, 'a')
                        newLine = f'{len(self.target)} {dim[0]} {dim[1]} {dim[2]} {dim[3]}\n'
                        fnewLabel.write(newLine)
                        fnewLabel.close()

                        new_image += 1
            
            if change or (not change and new_image < (self.dtSize-1) and not human):
                newImage = self.detImage + self.prefix + f'{ind}.jpg'
                if not change and new_image < (self.dtSize-1) and not human:
                    result = cv2.cvtColor(result, cv2.COLOR_BGR2RGB)
                    cv2.imwrite(newImage, result)
                    fnewList.write(newImage + '\n')
                elif change:
                    imageName = labelName.split('labels')
                    imageName = imageName[0] + 'images' + imageName[-1]
                    imageName = imageName.split('.txt')
                    imageName = imageName[0] + '.jpg'
                    img = mpimg.imread(imageName)
                    if len(img.shape) == 3:
                        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
                        cv2.imwrite(newImage, img)
                        fnewList.write(newImage + '\n')
            if ind % 100 == 0:    
                print(f'[INFO] {ind} of {len(self.labelList)} processed')
        
        print(f'[INFO] done creating dataset')
        fnewList.close()
            
    def load_labels(self, pathLabel):
        """load labels as list"""
        self.pathLabel = pathLabel
        self.labelList = os.listdir(pathLabel)
    
    def process_mask(self, maskFile, coordList, targetWidth, rot):
        """crops the area outside bbox of mask and rotate"""
        img = mpimg.imread(maskFile)

        topx = int(coordList[0])
        topy = int(coordList[1])
        botx = int(coordList[2])
        boty = int(coordList[3])

        sliced = img[topy:boty, topx:botx, :]
        rotated = util.rotate_bound(sliced, rot)
        resized = util.resize_img(rotated, targetWidth)

        return resized, resized.shape

    def set_dest(self, mode, dest, prefix):
        """set up dir structure at destination folder"""
        try: 
            os.mkdir(dest)
            os.mkdir(dest+'/images')
            os.mkdir(dest+'/images'+'/train')
            os.mkdir(dest+'/images'+'/test')
            os.mkdir(dest+'/labels')
            os.mkdir(dest+'/labels'+'/train')
            os.mkdir(dest+'/labels'+'/test')
        except FileExistsError:
            pass

        if mode == 'train':
            self.detImage = dest+'images/'+'train/'
            self.detLabel = dest+'labels/'+'train/'
            self.detList = dest+'train.txt'
        elif mode == 'test':
            self.detImage = dest+'images/'+'test/'
            self.detLabel = dest+'labels/'+'test/'
            self.detList = dest+'test.txt'
        self.prefix = prefix

    def set_target(self, target):
        """convert target object index to be in consecutive order"""
        # parse target objects
        res = []
        targets = target.split(',')
        for item in targets:
            res.append(item)
        self.target = res
    
        # create conversion table for new index
        self.conversion = {}
        for i, cat in enumerate(self.target):
            self.conversion[cat] = f'{i}'
    
    def set_size(self, size):
        """set number of custom object"""
        self.dtSize = size
       

def main():
    """
    Mode:
        - train:    create train dataset
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

    # parse configuration file and set constants
    info = util.parse_cfg(args['cfg'])
    for key, val in info.items():
        globals()[key] = val
    
    # main body
    mode = args['mode']
    if mode == 'train':
        c = createDataset()
        c.set_target(TARGET)
        c.set_size(6000)
        c.load_labels(TRAIN_LABEL)
        c.set_dest(mode, DET, 'blah')
        c.create()

    elif mode == 'test':
        pass
    
    else: 
        which = input('Which dataset? train or test? > ')
       
        # input assertion
        assert(which in ['train', 'test']), 'Try again with right input'

        # set right label for each category
        if which == 'train':
            label = TRAIN_LABEL
        else:
            label = VAL_LABEL

        # count # of objects in the dataset
        c = createDataset()
        c.set_target(TARGET)
        c.load_labels(label)
        c.count_target()

if __name__ == '__main__':
    main()
