import matplotlib.pyplot as plt
import numpy as np
import cv2
from scipy.spatial.distance import cdist
import imageio
import os
import math
import scipy.ndimage as ndi
from scipy.stats import gaussian_kde


file_name = 'images/test_draw_2.png'
image = cv2.imread(file_name, cv2.IMREAD_GRAYSCALE) # read image in gray scale
_, image = cv2.threshold(image, 128, 255, cv2.THRESH_OTSU + cv2.THRESH_BINARY_INV)
#[contours, hierarchy] = cv2.findContours(image, cv2.RetrievalModes, cv2.ContourApproximationModes[, contours[, hierarchy[, offset]]]	) ->	

contours, hierarchy = cv2.findContours(image, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
cv2.drawContours(image, contours, -1, (0,255,0), 3)
x,y = np.where(np.array(image) == 255)
#xy = np.vstack([x,y])
#z = gaussian_kde(xy)(xy)
#plt.scatter(x, y, c=z)


plt.imshow(image)
