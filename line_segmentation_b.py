import matplotlib.pyplot as plt
import numpy as np
import cv2
from scipy.spatial.distance import cdist

import math


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

    if count_around(image,x,y,1)==1 or \
        count_around(image,x,y,2)==1:
        #count_around(image,x,y,3)==1 or \
        #count_around(image,x,y,4)==1 or \
        #count_around(image,x,y,5)==1:
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

file_name = 'images/test_draw_1.png'
original_image = cv2.imread(file_name, cv2.IMREAD_GRAYSCALE)
image = cv2.copyMakeBorder(original_image, 10, 10, 10, 10, cv2.BORDER_CONSTANT, value = 255)
_, image = cv2.threshold(image, 128, 255, cv2.THRESH_OTSU + cv2.THRESH_BINARY_INV)
image = cv2.ximgproc.thinning(image)
points = cv2.findNonZero(image)

plt.imshow(image,  aspect="auto", cmap="gray")

end_pnts=[]
for i in points:
    x,y = i.ravel()
    if check_end(image,x,y):
        end_pnts.append(i)
        plt.scatter(x,y,color = 'blue')
print(end_pnts)

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

contours, _ = cv2.findContours(image, cv2.RETR_LIST,cv2.CHAIN_APPROX_NONE)

plot = False
i = 0
path_cont_x = []
path_cont_y = []
end_points_visited_idx = []
for point in end_pnts:
    if (cdist(points[end_points_visited_idx].reshape(-1,2), point.reshape(-1,2)) < 5).any() : continue
    end_points_visited_idx.append(nearest_index(points, point))
print(points[end_points_visited_idx[0]], points[end_points_visited_idx[1]])
for contour in contours:
    print('coucou')
    x = [i[:,0] for i in contour]
    y = [i[:,1] for i in contour]

    x = x[::100]
    y = y[::100]

    path_cont_x.append(x)
    path_cont_y.append(y)
    


    # x = x[::100]
    # y = y[::100]

    # for i in range(len(x)):
    #     plt.scatter(x[i], y[i])
    #     plt.pause(0.01)
    #     pass

path_contours = np.column_stack((path_cont_x, path_cont_y))
end_points_visited_idx = []
end_points_visited_path_idx = []
for point in end_pnts:
    if (cdist(points[end_points_visited_idx].reshape(-1,2), point.reshape(-1,2)) < 5).any() : continue
    end_points_visited_idx.append(nearest_index(points, point))


for ii in range(len(path_contours)):
    point = path_contours[ii]
    if np.linalg.norm(point - points[end_points_visited_idx[0]], axis=1) < 2:
        print(point)
        break


print(end_points_visited_path_idx)
print(points[end_points_visited_idx[0]], points[end_points_visited_idx[1]])
print(path_contours[end_points_visited_path_idx[0]], points[end_points_visited_path_idx[1]])
jump_1_idx = nearest_index(path_contours, points[end_points_visited_idx[0]])
jump_2_idx = nearest_index(path_contours, points[end_points_visited_idx[1]])
print(jump_1_idx, jump_2_idx)

add_on = np.column_stack((path_cont_x, path_cont_y))[jump_1_idx:jump_2_idx].copy()

add_on = np.array(add_on).reshape(-1,2)


print(add_on.shape)
x = add_on[:,0]
y = add_on[:,1]
plt.scatter(x,y)
#plt.imshow(original_image, aspect="auto", cmap="gray")
plt.show()