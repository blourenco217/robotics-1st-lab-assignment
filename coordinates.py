# """ convert image pixels into xy-coordinates """
import cv2
import matplotlib.pyplot as plt
import numpy as np

class processing(object):
    def __init__(self, file_name = 'images/test_draw_1.png'):
        self.image = cv2.imread(file_name)
	
	def image2plot(self):
		pass 

    	# scale_percent = 10 # percent of original size
		# width = int(image.shape[1] * scale_percent / 100)
		# height = int(image.shape[0] * scale_percent / 100)
		# dim = (width, height)

		# image = cv2.resize(image, dim, interpolation = cv2.INTER_AREA)
		# # plt.imshow(image, aspect="auto", cmap="gray")
		# # image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
		# # image = cv2.GaussianBlur(image, (3,3), 0)

		# image = cv2.Laplacian(image,cv2.CV_64F)

		# scharrx = cv2.Scharr(image, cv2.CV_64F,1,0)
		# scharry = cv2.Scharr(image, cv2.CV_64F,0,1)


		# _, image = cv2.threshold(image, 150, 255, cv2.THRESH_BINARY)
		# # plt.imshow(image)

		# # # plt.imshow(i, aspect="auto", cmap="gray")

		# print(image)
		# print(np.unique(image))
		# x, y = np.where(np.array(image) == 255)
		# plt.scatter(x[::10], y[::10])

		# plt.show()


# import cv2
# import matplotlib.pyplot as plt
# import numpy as np

# filename = 'images/test_draw_2.png'
# image = cv2.imread(filename, 0)

# scale_percent = 10 # percent of original size
# width = int(image.shape[1] * scale_percent / 100)
# height = int(image.shape[0] * scale_percent / 100)
# dim = (width, height)

# image = cv2.resize(image, dim, interpolation = cv2.INTER_AREA)
# # plt.imshow(image, aspect="auto", cmap="gray")
# # image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
# # image = cv2.GaussianBlur(image, (3,3), 0)

# image = cv2.Laplacian(image,cv2.CV_64F)

# scharrx = cv2.Scharr(image, cv2.CV_64F,1,0)
# scharry = cv2.Scharr(image, cv2.CV_64F,0,1)


# _, image = cv2.threshold(image, 150, 255, cv2.THRESH_BINARY)
# # plt.imshow(image)

# # # plt.imshow(i, aspect="auto", cmap="gray")

# print(image)
# print(np.unique(image))
# x, y = np.where(np.array(image) == 255)
# plt.scatter(x[::10], y[::10])

# plt.show()




# """ find corners """
# import cv2
# import numpy as np
# import matplotlib.pyplot as plt

# filename = 'images/test_draw_1.png'
# image = cv2.imread(filename)

# image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

# image= cv2.blur(image,(5,5))

# _, image = cv2.threshold(image, 150, 255, cv2.THRESH_BINARY)

# corners = cv2.goodFeaturesToTrack(image, 40,0.0005,50)
# corners = np.int0(corners)

# for i in corners:
#     x, y = i.ravel()
#     plt.scatter(x,y)
#     # cv2.circle(image, (x, y), 3, 255, -1)

# plt.imshow(image, aspect="auto", cmap="gray")
# plt.show()



# """ find straight lines """

# import cv2
# import numpy as np
# import matplotlib.pyplot as plt

# filename = 'images/test_draw_1.png'
# image = cv2.imread(filename)

# gray = cv2.cvtColor(image,cv2.COLOR_BGR2GRAY)

# edges = cv2.Canny(gray,50,150,apertureSize=3)

# # Apply HoughLinesP method to
# # to directly obtain line end points
# lines_list =[]
# lines = cv2.HoughLinesP(
# 			edges, # Input edge image
# 			1, # Distance resolution in pixels
# 			np.pi/180, # Angle resolution in radians
# 			threshold=100, # Min number of votes for valid line
# 			minLineLength=5, # Min allowed length of line
# 			maxLineGap=10 # Max allowed gap between line for joining them
# 			)

# # Iterate over points
# for points in lines:
#     x1,y1,x2,y2 = points[0]
#     plt.scatter(x1,y1)
#     plt.scatter(x2,y2)
#     cv2.line(image,(x1,y1),(x2,y2),(0,255,0),2)
#     lines_list.append([(x1,y1),(x2,y2)])
	

# circles = cv2.HoughCircles(image,cv2.HOUGH_GRADIENT,1,20,
#                             param1=50,param2=30,minRadius=0,maxRadius=0)
# circles = np.uint16(np.around(circles))

# for i in circles[0,:]:
#     plt.Circle((i[0],i[1]),i[2])
#     # # draw the outer circle
#     # cv2.circle(image,(i[0],i[1]),i[2],(0,255,0),2)
#     # # draw the center of the circle
#     # cv2.circle(image,(i[0],i[1]),2,(0,0,255),3)


plt.imshow(image)
plt.show()
# cv2.imwrite('detectedLines.png',image)

def fiberLen(image, calibration, plot = True):
    
    #read img
    fiber = MyImage(image)
    
    #store filename
    filename = str(image)
    
    #invert background to get white pixels on black background
    fiber = 255 - fiber.image
    
    #dilate then erode to connect disconnected pixels
    fiber = cv2.dilate(fiber, None, iterations = 1)
    fiber = cv2.erode(fiber, None, iterations = 1)
    
    #threshold image
    _, fiber_bin = cv2.threshold(fiber, 40, 255, cv2.THRESH_BINARY)

    #binarize img transforming pixel values to 0s and 1s
    height, width = fiber_bin.shape
    for i in range(height):
        for j in range(width):
            fiber_bin[i][j] = 1 if fiber_bin[i][j] == 255 else 0

    #skeletonize img
    fiber_skel = pcv2.morphology.skeletonize(fiber_bin) #pcv skeletonize returns 0 and 1 img / skimage skel returns True and False values
    
    #get contours
    contours, hierarchy = cv2.findContours(fiber_skel, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    
    #get only contours of fibers (which usually will be greater than 200)
    fiber_contours = [c for c in contours if cv2.arcLength(c, False) > 200]
    
    #initialize lists to store variables
    measurement = []
    label_coord_x = []
    label_coord_y = []

    #get contour perimeter, divide it by 2 and multiply by calibration factor
    for i, cnt in enumerate(fiber_contours):
        measurement.append(float(cv2.arcLength(fiber_contours[i], False) / 2) * calibration)
        #get coordinates if plot is True
        if plot is True:
            label_coord_x.append(fiber_contours[i][0][0][0]) #get first pixel of contours
            label_coord_y.append(fiber_contours[i][0][0][1]) #get second pixel of contours
        
    #plot fiber measurements if plot is True
    if plot is True:
        fiber_copy = fiber.copy()
        #loop through measurement values
        for i, value in enumerate(measurement):
            text = "{:.2f}".format(value)
            x = label_coord_x[i]
            y = label_coord_y[i]
            #put measurement labels in image
            cv2.putText(fiber_copy, text = text, org = (x, y), 
                       fontFace = cv2.FONT_HERSHEY_SIMPLEX, 
                       fontScale = 1,
                       color = (150, 150, 150),
                       thickness = 2)
        plt.imshow(fiber_copy)

        
    return [filename, measurement]