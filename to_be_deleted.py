import matplotlib.pyplot as plt
import numpy as np
import cv2
from scipy.spatial.distance import cdist
import imageio
import os
import math
import scipy.ndimage as ndi
from scipy.stats import gaussian_kde
from shapely.geometry import Point
from scipy.spatial import distance_matrix


file_name = 'images/test_draw_2.png'
image = cv2.imread(file_name, cv2.IMREAD_GRAYSCALE) # read image in gray scale
_, image = cv2.threshold(image, 128, 255, cv2.THRESH_OTSU + cv2.THRESH_BINARY_INV)

# y, x = np.where(np.array(image) == 255)
# x = x[::600]
# y = y[::600]
# # plt.scatter(x, y)
# x = x.reshape(-1,1)
# y = y.reshape(-1,1)
# print(x.shape, y.shape)

contours, _ = cv2.findContours(image, cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE) # tuple
plt.imshow(image, aspect="auto", cmap="gray")

# l = max(contours, key=lambda coll: len(coll)) # find longest contour
# x = [i[:,0] for i in l]
# y = [i[:,1] for i in l]
# x, y = self.sampling(x,y)

# for i in range(len(x)):
#     plt.scatter(x[i], y[i])
#     plt.pause(0.01)
i = 0
for contour in contours:
    print('coucou')
    x = [i[:,0] for i in contour]
    y = [i[:,1] for i in contour]

    # x = x[::200]
    # y = y[::200]
    if i == 0:
        plt.plot(x,y, color='blue')
    if i == 1:
        plt.plot(x,y, color='red')
    if i == 2:
        plt.plot(x,y, color='green')
    i = i+1
    plt.pause(0.1)

    # for i in range(len(x)):
    #     plt.scatter(x[i], y[i])
    #     plt.pause(0.01)

# distance_matrix_ = distance_matrix(x, y, p=2)


# import networkx as nx
# g = nx.Graph()

# plt.imshow(image, aspect="auto", cmap="gray")
# for i in range(len(distance_matrix_)):
#     source = i
#     curr_pt_dist = distance_matrix_[i]
#     for j in range(len(curr_pt_dist)):
#         dest = j 
#         eucl = curr_pt_dist[j]   
#         g.add_edge(source, dest, weight = eucl)
# solved_path = nx.approximation.traveling_salesman_problem(g, weight='weight', cycle=False)

# # path = []
# plt.imshow(image, aspect="auto", cmap="gray")
# for item in solved_path:
#     plt.scatter(x[item], y[item])
#     plt.pause(0.01)



plt.show()