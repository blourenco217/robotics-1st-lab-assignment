############################################################################
    # ROBOTICS 22-23: trajectory_planning.py
    # It contanis 
    # - reading the image, 
    # - analyzing the key points,
    # - find the paths 
    # - organize the paths based on the key points
############################################################################

# Robotics 22-23, Lab1 serial communications with the Scorbot example

import matplotlib.pyplot as plt
import numpy as np
import cv2
from scipy.spatial.distance import cdist
import imageio
import os
import math

# Returns the unit norm of a vector
def unit_vector(vector):
    return vector / np.linalg.norm(vector)

# Measure the angle between 2 vectors from the arguments
def angle(x1, y1, x2, y2, x3, y3):
    dir1 = np.array([x3-x2, y3-y2]) #vector from point 1 to 3
    dir2 = np.array([x2-x1, y2-y1]) #vector from point 1 to 2
    
    dir1 = np.squeeze(unit_vector(dir1))
    dir2 = np.squeeze(unit_vector(dir2))
    return np.arccos(np.clip(np.dot(dir1, dir2), -1.0, 1.0))

# Count the number of non-zero pixels around the 
# pixel under study with a window of 1-pixel width
def count_around(image,x,y,win): 
    count = 0
    w = len(image[0]) #number of pixels in x
    l = len(image) #number of pixels in y
    
    for i in range(-win,win+1): #-1 to 1, -2 to 2
        if i == -win or i == win:
            for j in range(-win,win+1):
                count += image[y+i][x+j]
        else:
            count += image[y+i][x-win]
            count += image[y+i][x+win]

    count /= 255

    return count

# CASE 1    
# Check to see if there is one pixel in each window
# If there is, that is taken as an indication of the end
# CASE 2
# If more than 1 pixel is found in additional windows, 
# the point is not considered to be the end point
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

# Verify whether each window contains more than 2 pixels
# If there is, it is interpreted as evidence of a bifurcation point
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

# Check if there is just 1 pixel inside each window """
def nearest_index(array, value):
    value_ = value.reshape(-1,2)
    array_ = array.reshape(-1,2)
    idx = cdist(array_,value_).argmin()
    return idx

# Plot the trajectory
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
        plt.pause(0.01)
    plt.show()
    # build gif
    with imageio.get_writer('outputs/trajectory_planning.gif', mode='I') as writer:
        for filename in filenames:
            image = imageio.imread(filename)
            writer.append_data(image)         
    # remove files
    for filename in set(filenames):
        os.remove(filename)

# Reduze the number of points to be drawn
# Considering 
# If is a straight line - only the start/end point need to be represented
# If is a curve line, consider each point based on the angle between 2 points of the curve
# just in case f
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
            x_new.append(x[ii + 1])
            y_new.append(y[ii + 1])
        # else:
        #     x = np.delete(x, ii + 1)
        #     y = np.delete(y, ii + 1)
        #     ii = ii - 1
    x_new.append(x[-1])
    y_new.append(y[-1])
    return x_new, y_new

# Reduze the size of the image by a A5 paper multiplied by 1.5 
# A5 dimensions y 1480 x 2100 tenths of mm
def normalize(self,x_, y_):
    # A5 dimensions
    h_paper = 1480 * 1.5
    w_paper =  2100 * 1.5
    
    # image dimensions
    h_image, w_image = self.original_image.shape #y,x
    x = np.zeros(len(x_))
    y = np.zeros(len(y_))

    # get coordinates vector
    for i in range(len(x_)):
        x[i] = int(x_[i])
        y[i] = int(y_[i])

    # Resize to width of paper if the image's width is bigger than the paper's 
    if w_image > w_paper: 
        x = x * w_paper / w_image 
        y = y * w_paper / w_image
        h = h_image * w_paper / w_image #height of the image just after resizing
        # After resizing, the height of the image is still bigger 
        # than the dimensions of the paper, the image is scaled down.
        if h > h_paper: 
            x = x * h_paper / h_image
            y = y * h_paper / h_image

    # Resize to height of paper if the image's height is bigger than the paper's 
    elif h_image > h_paper:
        x = x * h_paper / h_image
        y = y * h_paper / h_image
        w = w_image * h_paper / h_image #width of the image just after resizing
        # After resizing, the width of the image is still bigger 
        # than the dimensions of the paper, the image is scaled down.
        if w > w_paper:
            x = x * w_paper / w_image
            y = y * w_paper / w_image

    # ceil the new vectors created
    y = np.ceil(y)
    x = np.ceil(x)
 
    x = x - x[0]
    y = - y
    y = y - y[0]

    x = x.astype(np.int32)
    y = y.astype(np.int32)

    return x, y

class reference(object):
    """ class for the logic of the trajectory planning """
    
    # Read the image in grey scale 
    def __init__(self, file_name = 'images/test_draw_2.png'):
        self.image = cv2.imread(file_name, cv2.IMREAD_GRAYSCALE) 
        self.original_image = self.image
        self.image_processing()
    
    def image_processing(self):
        self.image = cv2.copyMakeBorder(self.image, 10, 10, 10, 10, cv2.BORDER_CONSTANT, value = 255) #To guarantee that the windows don't go out of the image's limits
        _, self.image = cv2.threshold(self.image, 128, 255, cv2.THRESH_OTSU + cv2.THRESH_BINARY_INV) 
        self.image = cv2.ximgproc.thinning(self.image) #Takes the binary image and contracts the foreground until only single-pixel wide lines remain
    
    # Locate the key points on the image
    def features2track(self, trajectory_plot = False):
        points = cv2.findNonZero(self.image)
        end_pnts=[]

        # Find endpoints
        for i in points:
            x,y = i.ravel()
            if check_end(self.image,x,y):
                if (cdist(np.array(end_pnts).reshape(-1,2), i.reshape(-1,2)) < 5).any() : continue
                end_pnts.append(i)

        biforc_pnts = []
        tresh = 10 # window to delete

        # Find biforcation points
        for i in points:
            x,y = i.ravel()
            if check_biforc(self.image,x,y):
                if (cdist(np.array(biforc_pnts).reshape(-1,2), i.reshape(-1,2)) < 5).any() : continue
                biforc_pnts.append(i)
                for ii in range(-tresh,tresh+1): #erase point and its neighbors
                    for jj in range(-tresh,tresh+1):
                        self.image[y+jj][x+ii] = 0

        good_features =  end_pnts + biforc_pnts
        i = 0
        path_unsorted = []

        # Find the contours
        contours, _ = cv2.findContours(self.image, cv2.RETR_TREE,cv2.CHAIN_APPROX_NONE) 

        # Trajectory's order
        for contour in contours:            
            path_cont = [i[:] for i in contour]
            good_features_c = [] # Good features in each contour
            # Add the key points into a vector
            for point in good_features:
                if (cdist(np.array(path_cont).reshape(-1,2), point.reshape(-1,2)) < 20).any() :
                    good_features_c.append(point)

            # If a biforcation point or a end point is found
            if len(good_features_c)==0 or len(good_features_c) == 1: 
                # Look for the nearst point that is a beggning or the end of a contour
                a = nearest_index(np.array(path_cont), good_features_c[0])
                # Clean the path to know that the point was visited
                cleaned_up_path = path_cont[a:a + round(len(path_cont)/2)]
            # If was not found a key point, the trajectory keeps going finding the closest point
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

        path_sorted = [ path_unsorted.pop(0) ] # Initialize sorted path with first contour
        pcurr  = path_sorted[-1][-1] 

        while len(path_unsorted)>0:
            sorted = False
            for ii in range(len(path_unsorted)):
                index = ii
                if np.linalg.norm(np.array(path_unsorted[ii][0]) - np.array(pcurr), axis=1) < 20:
                    #comparison between the 
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

            x, y = sampling(self,x,y)
            path_x = np.concatenate((path_x, x))
            path_y = np.concatenate((path_y, y))
        path_x, path_y = normalize(self, path_x,path_y)
        plt.scatter(path_x, path_y) 
        if trajectory_plot: trajectory_gif(self.image, path_x, path_y)
        return path_x, path_y