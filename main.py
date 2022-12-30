############################################################################
    # ROBOTICS 22-23: main.py
    # Lab1 main programm calling the image processing and actions related to robot
############################################################################
import serial
import time
import datetime
import numpy as np
import argparse
from trajectory_planning import reference
from actions import action


def main():

    """ arguments on command line """
    parser = argparse.ArgumentParser(description = 'Read in a a file drawing.')
    parser.add_argument('-i', '--imgpath', help = 'image path')
    # parser.add_argument('-m', '--manual', help = 'calibration') #can be manual or automatic
    args = vars(parser.parse_args())

   
    print("Starting")
    serString = "" # Used to hold data coming over UART
    coord = np.array(["X","Y"], dtype = str)

    """" create the path by trajectory planning """
    ref = reference(args['imgpath'])
    path_x,path_y, path_roll = ref.features2track() 
    path = np.array([path_x,path_y]) 
    path = np.transpose(path)

    n_points,_= path.shape 

    """ defined the z-positions of rest and lift, and roll based on laboratory measurements """
    z_rest = 1154
    z_lift = 1400
    roll_curr = -201
    point_robot = 1 # robot's coordinates starte at index 1

    """ arguments for defining the connection with the robot """
    robot = 1 # robot -> if 0 does only image processing
    manual = 1 # manual mode -> move teach pendant to initial position
    roll = 0   # roll's coordinates -> 0 not used, 1 used


    act = action()

    """ pick an initialization between manual calibration (with pen lifted from the paper) and automatic preset position """
    if manual == 1:
        origin = act.manual_calibrate()
    else: 
        origin = act.initialize() # goes to safe position

    act.init_points(origin,path)
    act.create_path(path,roll)

    """" specific movement functions for roll activated """
    if roll:
        act.add_waypoint_roll(path,coord,0,point_robot,roll_curr,z_rest) # 1st point of the robot -> setting the current roll
        point_robot = point_robot + 1
        path_roll[0] = path_roll[0] + roll_curr
        act.add_waypoint_roll(path,coord,0,point_robot, path_roll[0], z_rest) # 2nd point of the robot -> move to the next point with the current roll
        for i in range(1,n_points): 
            point_robot = point_robot + 1 
            act.add_waypoint_roll(path,coord,i, point_robot, path_roll[i-1],z_rest) # set the new roll's coordinate
            path_roll[i] = path_roll[i] + path_roll[i-1]
            point_robot = point_robot + 1
            act.add_waypoint_roll(path,coord,i,point_robot,path_roll[i],z_rest) # moving with the previous roll's coordindate defined
        
        point_robot = point_robot + 1
        act.add_lift_pen_roll(path,coord,n_points,point_robot,z_lift) 
        act.move_path_roll(n_points)

        """" specific movement functions for normal functioning without roll """
    else:
        for i in range(n_points): 
            act.add_waypoint(path,coord,i,z_rest)
        
        act.add_lift_pen(path,coord,n_points,z_lift) 
        act.move_path(n_points)

        act.disconnect()
    
if __name__ == '__main__':
    main()