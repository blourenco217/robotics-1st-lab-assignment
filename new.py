import matplotlib.pyplot as plt
import numpy as np
import cv2
from scipy.spatial.distance import cdist

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

file_name = 'images/test_draw_2.png'
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
        if (cdist(np.array(end_pnts).reshape(-1,2), i.reshape(-1,2)) < 5).any() : continue
        end_pnts.append(i)
        plt.scatter(x,y,color = 'blue')

biforc_pnts = []
tresh = 5 # window to delete
for i in points:
    x,y = i.ravel()
    if check_biforc(image,x,y):
        if (cdist(np.array(biforc_pnts).reshape(-1,2), i.reshape(-1,2)) < 5).any() : continue
        biforc_pnts.append(i)
        plt.scatter(x,y,color = 'red')
        for ii in range(-tresh,tresh+1): #erase point and its neighbors
            for jj in range(-tresh,tresh+1):
                image[y+jj][x+ii] = 0

contours, _ = cv2.findContours(image, cv2.RETR_LIST,cv2.CHAIN_APPROX_NONE)
path_cont_x = []
path_cont_y = []
path_cont = []
i=0
for contour in contours:
    print('coucou')
    x = [i[:,0] for i in contour]
    y = [i[:,1] for i in contour]

    x = x[::100]
    y = y[::100]

    path_cont_x.append(x)
    path_cont_y.append(y)

    path_cont = [i[:] for i in contour]

    a = nearest_index(np.array(path_cont), biforc_pnts[2])
    b = nearest_index(np.array(path_cont), end_pnts[0])
    cleaned_up_path = path_cont[a: b]
    cleaned_up_path.reverse()

    x,y  = np.array(cleaned_up_path).T
    x = x.T[::200]
    y = y.T[::200]
    for j in range(len(x)):
        plt.scatter(x[j], y[j])
        plt.pause(0.001)

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
    plt.pause(1)

# print(end_pnts[0])
# print(nearest_index(np.array(path_cont), end_pnts[0]))
# print(nearest_index(np.array(path_cont), end_pnts[1]))

# cleaned_up_path = path_cont[nearest_index(np.array(path_cont), end_pnts[0]): nearest_index(np.array(path_cont), end_pnts[1])]

# x,y  = np.array(cleaned_up_path).T

# x = x.T[::200]
# y = y.T[::200]

# for i in range(len(x)):
#     plt.scatter(x[i], y[i])
#     plt.pause(0.001)
plt.show()