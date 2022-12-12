import matplotlib.pyplot as plt
import numpy as np
import cv2
from scipy.spatial.distance import cdist

def angle(dir):
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
    dir2 = dir[1:]
    dir1 = dir[:-1]
    return np.arccos((dir1*dir2).sum(axis=1)/(
        np.sqrt((dir1**2).sum(axis=1)*(dir2**2).sum(axis=1))))

def sampling(x, y):
    return x[::100], y[::100]

def find_nearest(array, value):
    # array = np.asarray(array)
    value_ = value.reshape(-1,2)
    array_ = array.reshape(-1,2)
    idx = cdist(array_,value_).argmin()
    return idx


def get_end_pnts(pnts, image):
    extremes = []    
    for p in pnts:
        x = p[0]
        y = p[1]
        n = 0        
        n += image[y - 1,x]
        n += image[y - 1,x - 1]
        n += image[y - 1,x + 1]
        n += image[y,x - 1]    
        n += image[y,x + 1]    
        n += image[y + 1,x]    
        n += image[y + 1,x - 1]
        n += image[y + 1,x + 1]
        n /= 255        
        if n == 1:
            extremes.append(p)
            x,y = p
            # plt.scatter(x,y, color='red')
    return extremes

def order_points(points, ind):
    points_new = [ points.pop(ind) ]  # initialize a new list of points with the known first point
    pcurr      = points_new[-1]       # initialize the current point (as the known point)
    while len(points)>0:
        d      = np.linalg.norm(np.array(points) - np.array(pcurr), axis=1)  # distances between pcurr and all other remaining points
        ind    = d.argmin()                   # index of the closest point
        if d[ind] > 500:
            print('jump')
            np.concatenate(points_new, axis=0)
            jump_1_idx = find_nearest(np.concatenate(points_new, axis=0), np.asarray(pcurr))
            pcurr = points.pop(ind)
            jump_2_idx = find_nearest(np.concatenate(points_new, axis=0), np.asarray(pcurr))
            add_on = points_new[jump_2_idx:jump_1_idx].copy()
            add_on.reverse()
            for ii in add_on:
                points_new.append(ii)
            continue
        points_new.append(points.pop(ind))  # append the closest point to points_new
        pcurr  = points_new[-1]               # update the current point
    return points_new

file_name = 'images/test_draw_2.png'
image = cv2.imread(file_name, cv2.IMREAD_GRAYSCALE)
_, image = cv2.threshold(image, 128, 255, cv2.THRESH_OTSU + cv2.THRESH_BINARY_INV)
image = cv2.ximgproc.thinning(image)
points = cv2.findNonZero(image)
points = np.squeeze(points)
ext = get_end_pnts(points, image)
print(ext[0])
plt.imshow(image, aspect="auto", cmap="gray")

idx = find_nearest(points, ext[0])
print(idx)
print(points.shape)
points_new = order_points(list(points), idx)

x,y  = np.array(points_new).T
x, y = sampling(x, y)
for ii in range(len(x)): 
    plt.scatter(x[ii], y[ii], color = 'blue')
    plt.pause(0.01)
plt.show()
