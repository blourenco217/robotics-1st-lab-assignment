import numpy as np
# constants

""" Denavitt-Hartenberg Parameters """
a_1 = 0



class forward_kinematics():
    def __init__():
        """ compute gripper's position coordinates (x, y, z, alpha, betha, gamma)
        from the given joint angles (theta_1, ..., theta_6) """

    def transformation(self, a, d, alpha, theta):
        R = np.array([[np.cos(theta), -np.sin(theta), 0], 
                   [np.sin(theta)*np.cos(alpha), np.cos(theta)*np.cos(alpha), -np.sin(alpha)],
                   [np.sin(theta)*np.sin(alpha), np.cos(theta)*np.sin(alpha), np.cos(alpha)]])
        T = np.array([[a], [-np.sin(alpha)*d], [np.cos(alpha)*d]])

        return np.block([[R, T], [np.zeros((1,3)), np.array([[1]])]])
    
    def transformation_01(self, theta_1):
        """ transform matrix from first joint frame to base frame """
        R01 = np.array([[np.cos(theta_1), -np.sin(theta_1), 0], 
                   [np.sin(theta_1), np.cos(theta_1), 0],
                   [0, 0, 1]])
        T01 = np.array([[0], [0], [l1]])
        self.T01 = np.block([[R01, T01], [np.zeros((1,3)), np.array([[1]])]])
    
    def transformation_12(self, theta_2):
        """ transform from first to second joint """
        R12 = np.array([[np.cos(theta_2), 0, -np.sin(theta_2)], 
                   [0, 1, 0],
                   [np.sin(theta_2), 0, np.cos(theta_2)]])
        T2 = np.array([[0], [0], [l2]])
    
    def transformation_23(self):
        """ transform from second to third joint """
    
    def transformation_34(self):
        """ transform from third to fourth joint """
    
    def transformation_45(self):
        """ transform from fifth to  """
    
    def transformation_05(self):
        """ """
        # successive multiplications performed
        self.T05 = self.T01 @ self.T12 @ self.T23 @ self.T34 @ self.T45



class inverse_kinematics():
    def __init__(self, desired_position):
        ""

        x, y, z = desired_position
        