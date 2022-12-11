import cv2
import matplotlib.pyplot as plt
import numpy as np

def find_nearest(array, value):
    array = np.asarray(array)
    idx = (np.abs(array - value)).argmin()
    return array[idx]

def longest(list1):
    longest_list = max(len(elem) for elem in list1)
    return longest_list

class processing(object):
    def __init__(self, file_name = 'images/test_draw_2.png'):
        try:
            self.image = cv2.imread(file_name)
        except:
            print(ValueError + 'CANNOT READ IMAGE FILE\n')
    
    def sampling(self, x, y):
        return x[::400], y[::400]
    
    def image2plot(self):
        self.image = cv2.cvtColor(self.image, cv2.COLOR_BGR2GRAY)
        _, self.image = cv2.threshold(self.image, 110, 255, cv2.THRESH_BINARY)
        contours, _ = cv2.findContours(self.image, cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE) # tuple
        plt.imshow(self.image, aspect="auto", cmap="gray")

        # l = max(contours, key=lambda coll: len(coll)) # find longest contour
        # x = [i[:,0] for i in l]
        # y = [i[:,1] for i in l]
        # x, y = self.sampling(x,y)

        # for i in range(len(x)):
        #     plt.scatter(x[i], y[i])
        #     plt.pause(0.01)
        


        for contour in contours:
            print('coucou')
            x = [i[:,0] for i in contour]
            y = [i[:,1] for i in contour]

            x, y = self.sampling(x,y)

            for i in range(len(x)):
                plt.scatter(x[i], y[i])
                plt.pause(0.01)

        plt.show()
    
    def another(self):
        self.image = cv2.cvtColor(self.image, cv2.COLOR_BGR2GRAY)
        # self.image = cv2.bilateralFilter(self.image, 50, 50, 10)
        edged = cv2.Canny(self.image, 70, 250)

        a = plt.contour(edged)
        print(len(a.collections[0].get_paths()))
        plt.close()
        lines = list(dict.fromkeys(a.collections[0].get_paths()))
        for line in lines:
            x = line.vertices[:,0]
            y = line.vertices[:,1]
            plt.scatter(x, y)
            plt.pause(1)
        
        plt.show()

    def contours_detector(self):
        self.image = cv2.cvtColor(self.image, cv2.COLOR_BGR2GRAY)
        _, self.image = cv2.threshold(self.image, 110, 255, cv2.THRESH_BINARY)
        plt.imshow(self.image, aspect="auto", cmap="gray")
        edged = cv2.Canny(self.image, 70, 250)

        a = plt.contour(edged, levels=[1])
        print(len(a.allsegs[0]))

        contours = a.allsegs[0]
        
        # l = max(contours, key=lambda coll: len(coll)) # find longest contour
        # x = l[:,0]
        # y = l[:,1]
        # x, y = self.sampling(x,y)
        # for j in range(len(x)):
        #     plt.scatter(x[j], y[j])
        #     plt.pause(0.01)


        plt.close()
        contours.sort()
        for i in range(len(contours)):
            x = contours[i][:,0]
            y = contours[i][:,1]
            x, y = self.sampling(x,y)

            for j in range(len(x)):
                plt.scatter(x[j], y[j])
                plt.pause(0.01)

        plt.show()




p = processing()
# p.image2plot()
p.contours_detector()