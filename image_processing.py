import cv2
import matplotlib.pyplot as plt
import numpy as np

class processing(object):
    def __init__(self, file_name = 'images/test_draw_1.png'):
        self.image = cv2.imread(file_name)
	
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
    
    def edge_detector(self):
        self.image = cv2.cvtColor(self.image, cv2.COLOR_BGR2GRAY)

        self.image= cv2.blur(self.image,(5,5))

        _, self.image = cv2.threshold(self.image, 150, 255, cv2.THRESH_BINARY)

        corners = cv2.goodFeaturesToTrack(self.image, 40,0.0005,50)
        corners = np.int0(corners)

        for i in corners:
            x, y = i.ravel()
            plt.scatter(x,y)
            # cv2.circle(self.image, (x, y), 3, 255, -1)

        plt.imshow(self.image, aspect="auto", cmap="gray")
        plt.show()
    
    def hough_lines(self):
        # _, self.image = cv2.threshold(self.image, 150, 255, cv2.THRESH_BINARY)
        self.image = cv2.cvtColor(self.image,cv2.COLOR_BGR2GRAY)
        # self.image= cv2.blur(self.image,(5,5))
        # self.image = cv2.Laplacian(self.image,cv2.CV_64F)

        # scale_percent = 30 # percent of original size
        # width = int(self.image.shape[1] * scale_percent / 100)
        # height = int(self.image.shape[0] * scale_percent / 100)
        # dim = (width, height)

        # self.image = cv2.resize(self.image, dim, interpolation = cv2.INTER_AREA)

        _, self.image = cv2.threshold(self.image, 150, 255, cv2.THRESH_BINARY)

        edges = cv2.Canny(self.image,50,150,apertureSize=3)

        lines_list =[]
        lines = cv2.HoughLinesP(
        			edges, # Input edge image
        			1, # Distance resolution in pixels
        			np.pi/180, # Angle resolution in radians
        			threshold=100, # Min number of votes for valid line
        			minLineLength=5, # Min allowed length of line
        			maxLineGap=10 # Max allowed gap between line for joining them
        			)

        for points in lines:
            x1,y1,x2,y2 = points[0]
            plt.scatter(x1,y1)
            plt.scatter(x2,y2)
            cv2.line(self.image,(x1,y1),(x2,y2),(0,255,0),2)
            lines_list.append([(x1,y1),(x2,y2)])
        
        plt.imshow(self.image, aspect="auto", cmap="gray")
        plt.show()




p = processing()
p.hough_lines()