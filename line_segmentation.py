import matplotlib.pyplot as plt
import numpy as np
import cv2
from scipy.spatial.distance import cdist

import math

# def angle(x1, y1, x2, y2):
#     """
#     The return value is a 1D-array of values of shape (N-1,), with each value
#     between 0 and pi.
#     0 implies points in the same direction
#     pi/2 implies points are orthogonal
#     pi implies points in opposite directions
#     """
#     return math.atan2(y2-y1, x2-x1)

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

def sampling(x, y):
    return x[::300], y[::300]

def find_nearest(array, value):
    # array = np.asarray(array)
    value_ = value.reshape(-1,2)
    array_ = array.reshape(-1,2)
    idx = cdist(array_,value_).argmin()
    return idx

def neighbors(image, x,y): 
    neigh_count = count_around(image,x,y,1)
    return neigh_count



def count_around_1(image,x,y): #count number of non zero pixels around
    count = 0
    count += image[y - 1,x]
    count += image[y - 1,x - 1]
    count += image[y - 1,x + 1]
    count += image[y,x - 1]   
    count += image[y,x + 1]
    count += image[y + 1,x]    
    count += image[y + 1,x - 1]
    count += image[y + 1,x + 1]
    count /= 255
    return count

def count_around(image,x,y,win): #count number of non zero pixels around certain window
    count = 0
    w = len(image[0]) #3075 - x
    l = len(image) #6031 - y
    
    # if (x + win) > w or (x - win) < 0 or (y + win) > l or (y - win) < 0: #estava a sair fora das bounds e entao fizemos check
    #    return 0
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

    if count_around(image,x,y,1)==1 or\
       count_around(image,x,y,2)==1 or\
       count_around(image,x,y,3)==1 or\
       count_around(image,x,y,4)==1:# or\
       #count_around(image,x,y,5)==1:
        # print(count_around(image,x,y,1))
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

def clustering(points,start, stop): #takes array and saves it in cluster

    return 




def order_points(points, ind):

    points_new = [ points.pop(ind) ]  # initialize a new list of points with the known first point
    pcurr      = points_new[-1]       # initialize the current point (as the known point)
    print(len(points))
    while len(points)>10:
        d      = np.linalg.norm(np.array(points) - np.array(pcurr), axis=1)  # distances between pcurr and all other remaining points
        ind    = d.argmin() # index of the closest point
        if d[ind] > 500:
            print(pcurr)
            print(points)
            print(len(points))
            print('jump')
            np.concatenate(points_new, axis=0)
            jump_1_idx = find_nearest(np.concatenate(points_new, axis=0), np.asarray(pcurr))
            pcurr = points.pop(ind)
            jump_2_idx = find_nearest(np.concatenate(points_new, axis=0), np.asarray(pcurr))
            print(jump_1_idx, jump_2_idx)
            print(points_new[jump_1_idx], points_new[jump_2_idx])
            add_on = points_new[jump_2_idx:jump_1_idx].copy()
            add_on.reverse()
            for ii in add_on:
                points_new.append(ii)
            continue
        points_new.append(points.pop(ind))  # append the closest point to points_new
        pcurr  = points_new[-1]               # update the current point
    return points_new


"""""
def contour():
    return contour
    


def path_choice (countors)
#countors is a an array of countors, which are arrays

"""

file_name = 'images/test_draw_2.png'
original_image = cv2.imread(file_name, cv2.IMREAD_GRAYSCALE)

# scale_percent = 50 # percent of original size
# width = int(image.shape[1] * scale_percent / 100)
# height = int(image.shape[0] * scale_percent / 100)
# dim = (width, height)
# image = cv2.resize(image, dim, interpolation = cv2.INTER_AREA)
image = cv2.copyMakeBorder(original_image, 10, 10, 10, 10, cv2.BORDER_CONSTANT, value = 255)
_, image = cv2.threshold(image, 128, 255, cv2.THRESH_OTSU + cv2.THRESH_BINARY_INV)
image = cv2.ximgproc.thinning(image)
points = cv2.findNonZero(image)

plt.imshow(image,  aspect="auto", cmap="gray")

biforc_pnts = []
tresh = 5 #window to delete
for i in points:
    x,y = i.ravel()
    if check_biforc(image,x,y):
        biforc_pnts = np.append(biforc_pnts,i)
        plt.scatter(x,y,color = 'red')
        for ii in range(-tresh,tresh+1): #erase point and its neighbors
            for jj in range(-tresh,tresh+1):
                image[y+jj][x+ii] = 0
            #points = np.delete(points,ii)
            pass
print(biforc_pnts)
end_pnts=[]
for i in points:
    x,y = i.ravel()
    if check_end(image,x,y):
        end_pnts = np.append(end_pnts,i)
        plt.scatter(x,y,color = 'orange')

contours, _ = cv2.findContours(image, cv2.RETR_LIST,cv2.CHAIN_APPROX_SIMPLE)

plot = False
i = 0
for contour in contours:
    print('coucou')
    x = [i[:,0] for i in contour]
    y = [i[:,1] for i in contour]

    if plot:
        if i == 0:
            plt.plot(x,y, color='blue')
        if i == 1:
            plt.plot(x,y, color='red')
        if i == 2:
            plt.plot(x,y, color='green')
        if i == 3:
            plt.plot(x,y, color='pink')
        if i == 4:
            plt.plot(x,y, color='orange')
        if i == 5:
            plt.plot(x,y, color='yellow')
        i = i+1

    x = x[::100]
    y = y[::100]

    for i in range(len(x)):
        plt.scatter(x[i], y[i])
        plt.pause(0.01)
    plt.pause(1)

#plt.imshow(original_image, aspect="auto", cmap="gray")
plt.show()



""""
countors = [] # ja ordenados a comecar num end point
for i in countors[]
"""





""""
corners = cv2.goodFeaturesToTrack(image, 5,0.005,100)
corners = np.int0(corners)

for i in corners:
    points = np.append(points, i, axis = 0)
    # x, y = i.ravel()
    # plt.scatter(x,y)
plt.imshow(image, aspect="auto", cmap="gray")


# x, y = np.array(points).T
# x, y = sampling(x, y)
# print(x.shape, y.shape)
# points = np.array([x, y]).T
# print(points.shape)

"""

"""""
idx = find_nearest(points, end_pnts[0])
points_new = order_points(list(points), idx)

x,y  = np.array(points_new).T


x_new = []
y_new = []

theta_threshold = (5/9) * math.pi
for ii in range(len(x)-2):

    if ii > len(x) - 3:
        break
    
    is_corner = [x[ii],y[ii]] in corners

    if is_corner:
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

# x_new, y_new = sampling(x, y)

for ii in range(len(x_new)): 
    plt.scatter(x_new[ii], y_new[ii], color = 'blue')
    plt.pause(0.0000001)

print(len(x_new))
plt.show()

x_new = np.asarray(x_new)
y_new = np.asarray(y_new)
x_new = x_new / 5 #scale
x_new = np.round(x_new)
y_new = (- y_new) / 5
y_new = np.round(y_new)
x_new = x_new - x_new[0]
y_new = y_new - y_new[0]
"""
"""""
with open('path_x.npy', 'wb') as f:
    np.save(f, np.array(x_new))

with open('path_y.npy', 'wb') as f:
    np.save(f, np.array(y_new))

with open('path_x.npy', 'rb') as f:
    path_x = np.load(f)
    print(path_x)
    
with open('path_y.npy', 'rb') as f:
    path_y = np.load(f)
    print(path_y)
"""