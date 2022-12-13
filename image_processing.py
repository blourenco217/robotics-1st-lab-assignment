import matplotlib.pyplot as plt
import numpy as np
import cv2
from scipy.spatial.distance import cdist
import imageio
import os

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
    while len(points)>0:
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
    def __init__(self, file_name = 'images/test_draw_2.png'):
        self.image = cv2.imread(file_name, cv2.IMREAD_GRAYSCALE) # read image in gray scale
        self.image_processing()
    
    def image_processing(self):
        _, self.image = cv2.threshold(self.image, 128, 255, cv2.THRESH_OTSU + cv2.THRESH_BINARY_INV)
        self.image = cv2.ximgproc.thinning(self.image)
    
    def features2track(self, visual_graph = True):
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
        return x[::200], y[::200]
    
    def image_normalization(self, x, y):
        pass

path = reference_tracking()
path_x,path_y = path.features2track()
