import cv2
import numpy as np
import argparse
import matplotlib.pyplot as plt
import math

def find_nearest(array, value):
    array = np.asarray(array)
    idx = (np.abs(array - value)).argmin()
    return array[idx], idx

def get_end_pnts(pnts, img):
    extremes = []    
    for p in pnts:
        x = p[0]
        y = p[1]
        n = 0        
        n += img[y - 1,x]
        n += img[y - 1,x - 1]
        n += img[y - 1,x + 1]
        n += img[y,x - 1]    
        n += img[y,x + 1]    
        n += img[y + 1,x]    
        n += img[y + 1,x - 1]
        n += img[y + 1,x + 1]
        n /= 255        
        if n == 1:
            extremes.append(p)
    return extremes

def sampling( x, y):
    return x[::500], y[::500]

def order_points(points, ind):
    points_new = [ points.pop(ind) ]  # initialize a new list of points with the known first point
    pcurr      = points_new[-1]       # initialize the current point (as the known point)
    while len(points)>0:
        d      = np.linalg.norm(np.array(points) - np.array(pcurr), axis=1)  # distances between pcurr and all other remaining points
        ind    = d.argmin()                   # index of the closest point
        points_new.append( points.pop(ind) )  # append the closest point to points_new
        pcurr  = points_new[-1]               # update the current point
    return points_new

def connect_paths(x,y):
    new_x = x
    new_y = y
    # for ii in range(1, len(x)):
    ii = 1
    while ii < len(new_x):
        d = np.sqrt((new_x[ii]-new_x[ii-1])**2 + (new_y[ii]-new_y[ii-1])**2)
        if d > 500:
            print( (new_x[ii-1], new_y[ii-1]), (new_x[ii], new_y[ii]))
            add_x = x[:ii]
            add_x = np.flip(add_x)
            add_y = y[:ii]
            add_y = np.flip(add_y)
            new_x = np.insert(new_x, (ii+1), add_x, axis=0)
            new_y = np.insert(new_y, (ii+1), add_y, axis=0)
            rest_x = new_x[ii-1:]
            rest_y = new_y[ii-1:]
            if len(rest_x) == 0:
                break
            points = [(xx,yy)  for xx,yy in zip(rest_x,rest_y)]
            rest_x,rest_y  = np.array(order_points(points, 0)).T
            new_x = np.append(new_x, rest_x, axis=0)
            new_y = np.append(new_y, rest_y, axis=0)
            ii = ii*2 
        ii = ii+1
            
    
    print( (x[len(x)-2], y[len(x)-2]), (x[len(x)-1], y[len(x)-1]),)
    return new_x,new_y  




file_name = 'images/test_draw_1.png'
img = cv2.imread(file_name, cv2.IMREAD_GRAYSCALE)
# plt.imshow(img, aspect="auto", cmap="gray")


_, img = cv2.threshold(img, 128, 255, cv2.THRESH_OTSU + cv2.THRESH_BINARY_INV)

img_t = cv2.ximgproc.thinning(img)
pnts = cv2.findNonZero(img_t)
pnts = np.squeeze(pnts)
ext = get_end_pnts(pnts, img_t)
print(ext)

po = ext[0]

print(ext)
print(po)


# (rows, cols) = np.nonzero(img)
# endpoint_coords = []# Initialize empty list of coordinates
# for (r, c) in zip(rows, cols):# Loop through all non-zero pixels
#     top = max(0, r - 1)
#     right = min(img.shape[1] - 1, c + 1)
#     bottom = min(img.shape[0] - 1, r + 1)
#     left = max(0, c - 1)

#     sub_img = img[top: bottom + 1, left: right + 1]
#     if np.sum(sub_img) == 0:
#         endpoint_coords.append((r,c))

# print('ENDDD POINTTTT')
# print(endpoint_coords)

# img = cv2.ximgproc.thinning(img)

no_ccs, labels = cv2.connectedComponents(img)
label_pnts_dic = {}
i = 1 # skip label 0 as it corresponds to the backgground points
sum_of_cc_points = 0 
print(no_ccs)
while i < no_ccs:
    print('inside looop')
    label_pnts_dic[i] = np.where(labels == i) #where return tuple(list of x cords, list of y cords)

    l = label_pnts_dic[i]

    x = l[0]
    y = l[1]
    x, y = sampling(x,y)
    
    # ind = x.argmin()
    points = [(xx,yy)  for xx,yy in zip(x,y)]
    _, ind = find_nearest(x, po[0])
    print(ind)
    points_new = order_points(points, ind)

    x,y  = np.array(points_new).T

    # x,y = connect_paths(x,y)

    
    # plt.scatter(x,y)
    plt.plot(x, y)
    for i in range(len(x)):
        plt.scatter(x[i], y[i])
        plt.pause(0.0001)
    i +=1
plt.show()
# print (no_ccs, labels)