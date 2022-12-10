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
        return x[::100], y[::100]
    
    def image2plot(self):
        _, self.image = cv2.threshold(self.image, 110, 255, cv2.THRESH_BINARY)
        contours, _ = cv2.findContours(self.image, cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
        plt.imshow(self.image, aspect="auto", cmap="gray")
        for contour in contours:
            x = [i[:,0] for i in contour]
            y = [i[:,1] for i in contour]

            x = x[::100]
            y = y[::100]

            # print(len(x))
            for i in range(len(x)):
                plt.scatter(x[i], y[i])
                plt.pause(0.000001)

        plt.show()
    
    def another(self):
        self.image = cv2.cvtColor(self.image, cv2.COLOR_BGR2GRAY)
        # self.image = cv2.bilateralFilter(self.image, 50, 50, 10)
        edged = cv2.Canny(self.image, 70, 250)

        # a = plt.contour(edged)
        # print(len(a.collections[0].get_paths()))
        # plt.close()
        # lines = list(dict.fromkeys(a.collections[0].get_paths()))
        # for line in lines:
        #     x = line.vertices[:,0]
        #     y = line.vertices[:,1]
        #     plt.scatter(x, y)
        #     plt.pause(1)



        #plot separated contour
        # plt.subplot(1,3,3)
        # plt.imshow(self.image, aspect="auto", cmap="gray")

        # for i in range(1,len(a.allsegs[0]), 2):
        #     x = a.allsegs[0][i][:,0]
        #     y = a.allsegs[0][i][:,1]
        #     x = x[::300]
        #     y = y[::300]

        #     for j in range(len(x)):
        #         plt.scatter(x[j], y[j])
        #         plt.pause(0.000001)
            
            # plt.plot(x,y)

        a = plt.contour(edged)
        plt.close()
        plt.imshow(self.image, aspect="auto", cmap="gray")
        x = a.allsegs[0][2][:,0]
        y = a.allsegs[0][2][:,1]
        x = x[::300]
        y = y[::300]

        for j in range(len(x)):
            plt.scatter(x[j], y[j])
            plt.pause(0.000001)
        
        x = a.allsegs[0][3][:,0]
        y = a.allsegs[0][3][:,1]
        x = x[::300]
        y = y[::300]

        for j in range(len(x)):
            plt.scatter(x[j], y[j])
            plt.pause(0.000001)

        plt.show()
        
        # a = plt.contour(edged)
        # plt.close()
        # plt.imshow(self.image, aspect="auto", cmap="gray")
        

        # l = longest(a.allsegs[0])
        # print(a.allsegs[0])
        # x = l[:,0]
        # y = l[:,0]
        # x = x[::300]
        # y = y[::300]

        # for j in range(len(x)):
        #     plt.scatter(x[j], y[j])
        #     plt.pause(0.000001)
        

        # plt.show()

    def anoother(self):
        self.image = cv2.cvtColor(self.image, cv2.COLOR_BGR2GRAY)
        edged = cv2.Canny(self.image, 70, 250)

        a = plt.contour(edged, levels=[1])
        print(len(a.allsegs[0]))
        # plt.close()
        # plt.imshow(self.image, aspect="auto", cmap="gray")
        # x = a.allsegs[0][2][:,0]
        # y = a.allsegs[0][2][:,1]
        # x = x[::300]
        # y = y[::300]

        # for j in range(len(x)):
        #     plt.scatter(x[j], y[j])
        #     plt.pause(0.000001)
        
        n_contour = 1

        x = a.allsegs[0][n_contour][:,0]
        y = a.allsegs[0][n_contour][:,1]
        x = x[::300]
        y = y[::300]

        for j in range(len(x)):
            plt.scatter(x[j], y[j])
            plt.pause(0.000001)

        plt.show()




p = processing()
# p.image2plot()
p.anoother()