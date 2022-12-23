############################################################################
    # ROBOTICS 22-23: main.py
    # Lab1 serial communications with the Scorbot example
############################################################################
import serial
import time
import datetime
import numpy as np
import argparse
from trajectory_planning import reference
from actions import action


def main():
    ############################################################################
    # ATTENTION: Each point used was previously recorded with DEFP instruction
    #(from a terminal console - you can use, for example, putty or hyperterminal
    # as terminal console)
    ############################################################################

    parser = argparse.ArgumentParser(description = 'Read in a a file drawing.')
    parser.add_argument('-i', '--imgpath', help = 'image path')
    args = vars(parser.parse_args())

   
    print("Starting")
    serString = "" # Used to hold data coming over UART
    coord = np.array(["X","Y"], dtype = str)

    # create the path by trajectory planning
    ref = reference(args['imgpath'])
    path_x,path_y = ref.features2track() 
    path = np.array([path_x,path_y]) 
    path = np.transpose(path) 
    #path = path[0:2]
    points,_= path.shape #points = 43

    # defined the z-positions of rest and lift
    # based on laboratory measurements
    z_rest = 1154
    z_lift = 1400

    # connection with the robot
    robot = 1
    # manual mode -> move teach pendant to initial position
    manual = 0


    if robot == 1:
        act = action()
        if manual == 1:
            origin = act.manual_calibrate()
        else: 
            origin = act.initialize() # goes to safe position
        act.init_points(origin,path)
        act.create_path(path)
        #act.rest_pen()
        for i in range(points): 
            act.add_waypoint(path,coord,i,z_rest)
        act.add_lift_pen(path,coord,points,z_lift) #points = 43
        act.move_path(points)
        #act.lift_pen(z_lift)
        act.disconnect()
    
########################################################################
if __name__ == '__main__':
    main()