import cv2
import matplotlib.pyplot as plt
import numpy as np
import time
import math
import scipy.spatial.distance as distance

class processing(object):
    def __init__(self, file_name = 'images/test_draw_1.png'):
        try:
            self.image = cv2.imread(file_name)
        except:
            print(ValueError + 'CANNOT READ IMAGE FILE\n')

	
    def image2plot(self):
        scale_percent = 10 # percent of original size
        width = int(self.image.shape[1] * scale_percent / 100)
        height = int(self.image.shape[0] * scale_percent / 100)
        dim = (width, height)

        self.image = cv2.resize(self.image, dim, interpolation = cv2.INTER_AREA)
        # plt.imshow(self.image, aspect="auto", cmap="gray")
        # self.image = cv2.cvtColor(self.image, cv2.COLOR_BGR2GRAY)
        # self.image = cv2.GaussianBlur(self.image, (3,3), 0)

        self.image = cv2.Laplacian(self.image,cv2.CV_64F)

        scharrx = cv2.Scharr(self.image, cv2.CV_64F,1,0)
        scharry = cv2.Scharr(self.image, cv2.CV_64F,0,1)


        _, self.image = cv2.threshold(self.image, 150, 255, cv2.THRESH_BINARY)

        # # plt.imshow(i, aspect="auto", cmap="gray")
        x, y = np.where(np.array(self.image) == 255)
        plt.scatter(x[::10], y[::10])

        plt.show()
    
    def corner_detector(self):
        self.image = cv2.cvtColor(self.image, cv2.COLOR_BGR2GRAY)

        self.image= cv2.blur(self.image,(5,5))

        scale_percent = 100 # percent of original size
        width = int(self.image.shape[1] * scale_percent / 100)
        height = int(self.image.shape[0] * scale_percent / 100)
        dim = (width, height)

        self.image = cv2.resize(self.image, dim, interpolation = cv2.INTER_AREA)

        _, self.image = cv2.threshold(self.image, 150, 255, cv2.THRESH_BINARY)
        self.image = cv2.bitwise_not(self.image)
        self.image = cv2.ximgproc.thinning(self.image)

        corners = cv2.goodFeaturesToTrack(self.image, 10,0.005,50)
        corners = np.int0(corners)

        for i in corners:
            x, y = i.ravel()
            plt.scatter(x,y)
            # cv2.circle(self.image, (x, y), 3, 255, -1)

        plt.imshow(self.image, aspect="auto", cmap="gray")
        plt.show()

        return corners
    
    def hough_lines(self):
        # _, self.image = cv2.threshold(self.image, 150, 255, cv2.THRESH_BINARY)
        self.image = cv2.cvtColor(self.image,cv2.COLOR_BGR2GRAY)
        self.image= cv2.blur(self.image,(5,5))
        # self.image = cv2.Laplacian(self.image,cv2.CV_64F)

        scale_percent = 10 # percent of original size
        width = int(self.image.shape[1] * scale_percent / 100)
        height = int(self.image.shape[0] * scale_percent / 100)
        dim = (width, height)

        self.image = cv2.resize(self.image, dim, interpolation = cv2.INTER_AREA)

        _, self.image = cv2.threshold(self.image, 150, 255, cv2.THRESH_BINARY)

        self.image = cv2.ximgproc.thinning(self.image)

        edges = cv2.Canny(self.image,50,150,apertureSize=3)

        lines_list =[]
        lines = cv2.HoughLinesP(
        			edges, # Input edge image
        			1, # Distance resolution in pixels
        			np.pi/180, # Angle resolution in radians
        			threshold=20, # Min number of votes for valid line
        			minLineLength=5, # Min allowed length of line
        			maxLineGap=10 # Max allowed gap between line for joining them
        			)

        for points in lines:
            x1,y1,x2,y2 = points[0]
            plt.scatter(x1,y1)
            plt.scatter(x2,y2)
            # cv2.line(self.image,(x1,y1),(x2,y2),(0,255,0),2)
            lines_list.append([(x1,y1),(x2,y2)])
        
        plt.imshow(self.image, aspect="auto", cmap="gray")
        plt.show()
    
    def hough_corner_detector(self):
        self.image = cv2.cvtColor(self.image,cv2.COLOR_BGR2GRAY)
        self.image= cv2.blur(self.image,(5,5))

        _, self.image = cv2.threshold(self.image, 150, 255, cv2.THRESH_BINARY)

        corners = cv2.goodFeaturesToTrack(self.image, 5,0.005,50)
        corners = np.int0(corners)

        for i in corners:
            x, y = i.ravel()
            plt.scatter(x,y, c='black')
            # cv2.circle(self.image, (x, y), 3, 255, -1)

        scale_percent = 20 # percent of original size
        width = int(self.image.shape[1] * scale_percent / 100)
        height = int(self.image.shape[0] * scale_percent / 100)
        dim = (width, height)

        self.image = cv2.resize(self.image, dim, interpolation = cv2.INTER_AREA)
        
        edges = cv2.Canny(self.image,50,150,apertureSize=3)

        lines_list =[]
        lines = cv2.HoughLinesP(
        			edges, # Input edge image
        			1, # Distance resolution in pixels
        			np.pi/180, # Angle resolution in radians
        			threshold=20, # Min number of votes for valid line
        			minLineLength=5, # Min allowed length of line
        			maxLineGap=10 # Max allowed gap between line for joining them
        			)

        for points in lines:
            x1,y1,x2,y2 = points[0]
            plt.scatter(x1,y1)
            plt.scatter(x2,y2)
            # cv2.line(self.image,(x1,y1),(x2,y2),(0,255,0),2)
            lines_list.append([(x1,y1),(x2,y2)])
        
        plt.imshow(self.image, aspect="auto", cmap="gray")
        plt.show()
    
    def get_end_pnts(self, pnts, img):
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
    
    def detect_loose_end(self):
        # self.image = cv2.threshold(self.image, 128, 255, cv2.THRESH_OTSU + cv2.THRESH_BINARY_INV)
        # self.image = cv2.threshold(self.image, 128, 255, cv2.THRESH_OTSU + cv2.THRESH_BINARY_INV)
        # self.image= cv2.blur(self.image,(5,5))
        self.image = cv2.cvtColor(self.image,cv2.COLOR_BGR2GRAY)
        # self.image= cv2.blur(self.image,(5,5))
        _, self.image = cv2.threshold(self.image, 128, 255, cv2.THRESH_BINARY)
        self.image = cv2.bitwise_not(self.image)
        self.image = cv2.ximgproc.thinning(self.image)
        pnts = cv2.findNonZero(self.image)
        pnts = np.squeeze(pnts)
        ext = self.get_end_pnts(pnts, self.image)
        for p in ext:
            plt.scatter(p[0], p[1])
            # cv2.circle(img, (p[0], p[1]), 5, 128)
        
        plt.imshow(self.image, aspect="auto", cmap="gray")
        plt.show()
    
    def order_points(self, x, y):
        points = x, y
        dists =distance.pdist(points)
        m=np.argsort(distance.squareform(dists))[:,1:]
        order = [0,m[0,0]]
        next_point = order[-1]
        while len(order)<len(points):
            row = m[next_point]
            i = 0
            while row[i] in order:
                i += 1
            order.append(row[i])
            next_point = order[-1]
        order.append(0)
        ordered = points[order]

        return x, y



    def image_sampling(self):

        self.image = cv2.cvtColor(self.image, cv2.COLOR_BGR2GRAY)
        _, self.image = cv2.threshold(self.image, 128, 255, cv2.THRESH_BINARY)
        self.image = cv2.bitwise_not(self.image)
        self.image = cv2.ximgproc.thinning(self.image)

        y, x = np.where(np.array(self.image) == 255)
        # print(np.array(sampling).shape)
        x_sample = x[::200]
        y_sample = y[::200]
        x, y = self.order_points(x, y)
        plt.imshow(self.image, aspect="auto", cmap="gray")
        for i in range(np.size(x_sample)):
            plt.scatter(x_sample[i], y_sample[i])
            plt.pause(0.001)


        
        # for idx in sampling:
        #     i, j = idx.ravel()
        #     plt.scatter(i,j)
        #     time.sleep(0.5)

        plt.show()
        








p = processing()
p.image_sampling()





# corners = p.corner_detector()
# file_name = 'images/square.png'
# image = cv2.imread(file_name)
# y_center, x_center = image.shape[0]/2, image.shape[1]/2

# x_r = []
# y_r = []

# for i in corners:
#     x, y = i.ravel()
#     x_r.append(x-x_center), y_r.append(y-y_center) 

# print(x_r, y_r)
