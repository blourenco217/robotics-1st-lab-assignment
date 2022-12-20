import matplotlib.pyplot as plt
import numpy as np
import cv2
from scipy.spatial.distance import cdist
import imageio
import os
import math

def unit_vector(vector):
    """ Returns the unit vector of the vector.  """
    return vector / np.linalg.norm(vector)

def angle(x1, y1, x2, y2, x3, y3):
    dir1 = np.array([x3-x2, y3-y2]) #vector from point 1 to 3
    dir2 = np.array([x2-x1, y2-y1]) #vector from point 1 to 2
    
    dir1 = np.squeeze(unit_vector(dir1))
    dir2 = np.squeeze(unit_vector(dir2))
    return np.arccos(np.clip(np.dot(dir1, dir2), -1.0, 1.0))

def count_around(image,x,y,win): #count number of non zero pixels around certain window
    count = 0
    w = len(image[0]) #3075 - x
    l = len(image) #6031 - y
    
    for i in range(-win,win+1): #-1 to 1, -2 to 2
        if i == -win or i == win:
            for j in range(-win,win+1):
                count += image[y+i][x+j]
        else:
            count += image[y+i][x-win]
            count += image[y+i][x+win]

    count /= 255

    return count
    
def check_end(image,x,y):
    end_pnt=0

    if count_around(image,x,y,1)==1 or \
        count_around(image,x,y,2)==1:
            if count_around(image,x,y,1)>=3 or \
            count_around(image,x,y,2)>=3 or\
            count_around(image,x,y,3)>=3 or\
            count_around(image,x,y,4)>=3 or\
            count_around(image,x,y,5)>=3 or\
            count_around(image,x,y,6)>=3 or\
            count_around(image,x,y,7)>=3 or\
            count_around(image,x,y,8)>=3 or\
            count_around(image,x,y,8)>=3 or\
            count_around(image,x,y,10)>=3:
                return end_pnt
            end_pnt = 1

    return end_pnt

def check_biforc(image,x,y):
    biforc=0

    branches = count_around(image,x,y,1)
    if branches > 2:
        if  count_around(image,x,y,2)>=branches and \
            count_around(image,x,y,3)>=branches and \
            count_around(image,x,y,4)>=branches and \
            count_around(image,x,y,5)>=branches and \
            count_around(image,x,y,6)>=branches and \
            count_around(image,x,y,7)>=branches and \
            count_around(image,x,y,8)>=branches and \
            count_around(image,x,y,9)>=branches and \
            count_around(image,x,y,10)>=branches:
                biforc=1
                                
    return biforc

def nearest_index(array, value):
    value_ = value.reshape(-1,2)
    array_ = array.reshape(-1,2)
    idx = cdist(array_,value_).argmin()
    return idx

def trajectory_gif(image, x, y):
    plt.close()
    original_image = cv2.bitwise_not(image)
    plt.imshow(original_image, aspect="auto", cmap="gray")
    filenames = []
    for ii in range(len(x)):
        filename = f'{ii}.png'
        filenames.append(filename)
        plt.scatter(x[ii], y[ii], color = 'blue')
        plt.savefig(filename)
        #plt.pause(0.01)
    plt.show()
    # build gif
    with imageio.get_writer('outputs/trajectory_planning.gif', mode='I') as writer:
        for filename in filenames:
            image = imageio.imread(filename)
            writer.append_data(image)         
    # remove files
    for filename in set(filenames):
        os.remove(filename)

class reference(object):
    def __init__(self, file_name = 'images/test_draw_2.png'):
        self.image = cv2.imread(file_name, cv2.IMREAD_GRAYSCALE) # read image in gray scale
        self.image_processing()
    
    def image_processing(self):
        self.image = cv2.copyMakeBorder(self.image, 10, 10, 10, 10, cv2.BORDER_CONSTANT, value = 255)
        _, self.image = cv2.threshold(self.image, 128, 255, cv2.THRESH_OTSU + cv2.THRESH_BINARY_INV)
        self.image = cv2.ximgproc.thinning(self.image)
    
    def features2track(self, trajectory_plot = False):
        points = cv2.findNonZero(self.image)

        end_pnts=[]
        for i in points:
            x,y = i.ravel()
            if check_end(self.image,x,y):
                if (cdist(np.array(end_pnts).reshape(-1,2), i.reshape(-1,2)) < 5).any() : continue
                end_pnts.append(i)

        biforc_pnts = []
        tresh = 10 # window to delete
        for i in points:
            x,y = i.ravel()
            if check_biforc(self.image,x,y):
                if (cdist(np.array(biforc_pnts).reshape(-1,2), i.reshape(-1,2)) < 5).any() : continue
                biforc_pnts.append(i)
                for ii in range(-tresh,tresh+1): #erase point and its neighbors
                    for jj in range(-tresh,tresh+1):
                        self.image[y+jj][x+ii] = 0

        contours, _ = cv2.findContours(self.image, cv2.RETR_TREE,cv2.CHAIN_APPROX_NONE)

        good_features =  end_pnts + biforc_pnts
        i = 0
        path_unsorted = []
        for contour in contours:
            path_cont = [i[:] for i in contour]
            good_features_c = [] # good features in each contour
            for point in good_features:
                if (cdist(np.array(path_cont).reshape(-1,2), point.reshape(-1,2)) < 20).any() :
                    good_features_c.append(point)

            if len(good_features_c)==0 or len(good_features_c) == 1:
                a = nearest_index(np.array(path_cont), good_features_c[0])
                cleaned_up_path = path_cont[a:a + round(len(path_cont)/2)]
            else:
                a = nearest_index(np.array(path_cont), good_features_c[0])
                b = nearest_index(np.array(path_cont), good_features_c[1])
                if a > b:
                    cleaned_up_path = path_cont[b: a]
                    cleaned_up_path.reverse()
                else:
                    cleaned_up_path = path_cont[a: b]
                    cleaned_up_path.reverse()
            path_unsorted.append(cleaned_up_path)


        path_sorted = [ path_unsorted.pop(0) ] # initialize sorted path with first contour
        pcurr  = path_sorted[-1][-1] 
        while len(path_unsorted)>0:
            sorted = False
            for ii in range(len(path_unsorted)):
                index = ii
                if np.linalg.norm(np.array(path_unsorted[ii][0]) - np.array(pcurr), axis=1) < 20:
                    path_sorted.append(path_unsorted.pop(index))
                    sorted = True
                    break

            if sorted: index = index - 1
            if np.linalg.norm(np.array(path_unsorted[index][0]) - np.array(pcurr), axis=1) > 200:
                print('backtrak')
                add_on = path_unsorted.pop(index).copy()
                add_on.reverse()
                path_sorted.append(add_on)
                sorted = True

            if not sorted:
                path_sorted.append(path_unsorted.pop(index))
            pcurr = path_sorted[-1][-1]

        path_x = []
        path_y = []
        original_image = cv2.bitwise_not(self.image)
        plt.imshow(original_image, aspect="auto", cmap="gray")
        for line in path_sorted:
            x,y  = np.array(line).T
            x = x.T.flatten()[::200]
            y = y.T.flatten()[::200]

            x, y = self.sampling(x,y)
            path_x = np.concatenate((path_x, x))
            path_y = np.concatenate((path_y, y))
        # path_x, path_y =  path_x[0], path_y[0]
        plt.scatter(path_x, path_y)
        plt.show()
        if trajectory_plot: trajectory_gif(self.image, path_x, path_y)

        return path_x, path_y
    
    def sampling(self, x, y):

        x_new = []
        y_new = []
        theta_threshold_min = 15 * math.pi/180
        theta_threshold_max = 165 * math.pi/180
        x_new.append(x[0])
        y_new.append(y[0])
        for ii in range(len(x)-2):
            ag = angle(x_new[-1], y_new[-1], x[ii+1], y[ii+1], x[ii+2], y[ii+2])
            if  ag > theta_threshold_min and ag < theta_threshold_max:
                print(ag * 180 / math.pi)      
                x_new.append(x[ii + 1])
                y_new.append(y[ii + 1])
            # else:
            #     x = np.delete(x, ii + 1)
            #     y = np.delete(y, ii + 1)
            #     ii = ii - 1
        x_new.append(x[-1])
        y_new.append(y[-1])
        # print(x_new.shape, y_new.shape)
        return x_new, y_new

    def normalize(self,x, y):
        x = np.asarray(x)
        y = np.asarray(y)
        x = x / 5
        x = np.round(x)
        y = (- y) / 5
        y = np.round(y)
        x = x - x[0]
        y = y - y[0]
        return x, y
    
path = reference()
path_x,path_y = path.features2track()