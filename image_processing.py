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
    """
    Returns the angles between vectors.

    Parameters:
    dir is a 2D-array of shape (N,M) representing N vectors in M-dimensional space.

    The return value is a 1D-array of values of shape (N-1,), with each value
    between 0 and pi.

    0 implies the vectors point in the same direction
    pi/2 implies the vectors are orthogonal
    pi implies the vectors point in opposite directions
    """
    dir1 = np.array([x3-x1, y3-y1]) #vector from point 1 to 3
    dir2 = np.array([x2-x1, y2-y1]) #vector from point 1 to 2
    
    dir1 = unit_vector(dir1)
    dir2 = unit_vector(dir2)
    return np.arccos(np.clip(np.dot(dir1, dir2), -1.0, 1.0))

def loose_ends(points, image):
    end_points = []    
    for p in points:
        x, y = p[0], p[1]
        n = 0        
        n += image[y - 1,x]
        n += image[y - 1,x - 1]
        n += image[y - 1,x + 1]
        n += image[y,x - 1]    
        n += image[y,x + 1]    
        n += image[y + 1,x]    
        n += image[y + 1,x - 1]
        n += image[y + 1,x + 1]
        n /= 255  # normalize      
        if n == 1:
            end_points.append(p)
            x,y = p
    return end_points

def nearest_index(array, value):
    value_ = value.reshape(-1,2)
    array_ = array.reshape(-1,2)
    idx = cdist(array_,value_).argmin()
    return idx

def order_points(points, ind):
    points_new = [ points.pop(ind) ]  # initialize a new list of points with the known first point
    pcurr      = points_new[-1]       # initialize the current point (as the known point)
    while len(points)>10:
        d      = np.linalg.norm(np.array(points) - np.array(pcurr), axis=1)  # distances between pcurr and all other remaining points
        ind    = d.argmin()                   # index of the closest point
        if d[ind] > 500:
            print('jump')
            np.concatenate(points_new, axis=0)
            jump_1_idx = nearest_index(np.concatenate(points_new, axis=0), np.asarray(pcurr))
            pcurr = points.pop(ind)
            jump_2_idx = nearest_index(np.concatenate(points_new, axis=0), np.asarray(pcurr))
            add_on = points_new[jump_2_idx:jump_1_idx].copy()
            add_on.reverse()
            for ii in add_on:
                points_new.append(ii)
            continue
        points_new.append(points.pop(ind))  # append the closest point to points_new
        pcurr  = points_new[-1]               # update the current point
    return points_new

class reference_tracking(object):
    def __init__(self, file_name = 'images/test_draw_1.png'):
        self.image = cv2.imread(file_name, cv2.IMREAD_GRAYSCALE) # read image in gray scale
        self.image_processing()
    
    def image_processing(self):
        _, self.image = cv2.threshold(self.image, 128, 255, cv2.THRESH_OTSU + cv2.THRESH_BINARY_INV)
        self.image = cv2.ximgproc.thinning(self.image)
    
    def features2track(self, visual_graph = False):
        points = cv2.findNonZero(self.image)
        points = np.squeeze(points)
        ext = loose_ends(points, self.image)
        idx = nearest_index(points, ext[0])
        points_ordered = order_points(list(points), idx)
        x,y  = np.array(points_ordered).T
        x, y = self.sampling(x, y)

        if visual_graph:
            original_image = cv2.bitwise_not(self.image)
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
            with imageio.get_writer('trajectory_planning.gif', mode='I') as writer:
                for filename in filenames:
                    image = imageio.imread(filename)
                    writer.append_data(image)         
            # remove files
            for filename in set(filenames):
                os.remove(filename)

        return x,y
    
    def sampling(self, x, y):

        corners = cv2.goodFeaturesToTrack(self.image, 5,0.005,100)
        corners = np.int0(corners)

        x_new = []
        y_new = []

        theta_threshold = (5/9) * math.pi
        for ii in range(len(x)-2):

            if ii > len(x) - 3:
                break
            
            is_corner = [x[ii],y[ii]] in corners

            if is_corner:
                indices = np.where(corners==[x[ii],y[ii]])
                corners = np.delete(corners, indices)
                x_new.append(x[ii])
                y_new.append(y[ii])
                plt.scatter(x[ii], y[ii], color = 'red')
                continue
            elif angle(x[ii], y[ii], x[ii+1], y[ii+1], x[ii+2], y[ii+2]) < theta_threshold:        
                if (ii % 600) == 0:
                    x_new.append(x[ii + 1])
                    y_new.append(y[ii + 1])
            else:
                x = np.delete(x, ii + 1)
                y = np.delete(y, ii + 1)
                ii = ii - 1
        
        # print(x_new.shape, y_new.shape)
        return x_new, y_new
    
    def image_normalization(self, x_, y_):

        for x,y in x_, y_:
            x= x / 5
            x = math.ceil(x)
            y = (- y) / 5
            y= math.ceil(y)
        x = x - x[0]
        y = y - y[0]

        return x, y

# path = reference_tracking()
# path_x,path_y = path.features2track()
# path_x, path_y = path.image_normalization(path_x,path_y)
