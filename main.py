############################################################################
    # ROBOTICS 22-23: main.py
    # Lab1 serial communications with the Scorbot example
############################################################################
import serial
import time
import datetime
import numpy as np
from trajectory_planning import reference
from actions import action

# def read_and_wait(ser, wait_time):
#     output = ""
#     flag = True
#     start_time = time.time()
#     while flag:
#         # Wait until there is data waiting in the serial buffer
#         if ser.in_waiting > 0:
#             # Read data out of the buffer until a carriage return / new line is found
#             serString = ser.readline()
#             # Print the contents of the serial data
#             try:
#                 output = serString.decode("Ascii")
#                 print(serString.decode("Ascii"))
#             except:
#                 pass
#         else:
#             deltat = time.time() - start_time
#             if deltat>wait_time:
#                 flag = False

#     return output

def main():
    ############################################################################
    # ATTENTION: Each point used was previously recorded with DEFP instruction
    #(from a terminal console - you can use, for example, putty or hyperterminal
    # as terminal console)
    ############################################################################
   
    print("Starting")
    serString = "" # Used to hold data coming over UART
    coord = np.array(["X","Y"], dtype = str)

    # create the path by trajectory planning
    ref = reference()
    path_x,path_y = ref.features2track() 
    path = np.array([path_x,path_y]) 
    path = np.transpose(path) 
    path = path[0:10]
    points,_= path.shape

    # defined the z-positions of rest and lift
    # based on laboratory measurements
    z_rest = 1000
    z_lift = 1400

    # connection with the robot
    robot = 1
    if robot == 1:
        act = action()
        origin = act.initialize()
        origin = act.manual_calibrate()
        act.init_points(origin,path)
        act.create_path(path)
        #act.rest_pen()
        for i in range(points):
            act.add_waypoint(path,coord,i,z_rest)
        act.move_path(points)
        act.lift_pen(z_lift)

    #draw based on the values of the vectors related with x and y
    usesaved = 0
    if usesaved == 1:
        with open('path_x.npy', 'rb') as f:
            path_x = np.load(f)
        
        with open('path_y.npy', 'rb') as f:
            path_y = np.load(f)
        
        path_x = path_x[0:50]
        path_y = path_y[0:50]

        path = np.zeros((len(path_x), 5))

        for ii in range(len(path_x)):
            path[ii][0] = path_x[ii]
            path[ii][1] = path_y[ii]
    
        path = path.astype(np.int32)
    
    print('housekeeping completed - exiting')
    
########################################################################
if __name__ == '__main__':
    main()