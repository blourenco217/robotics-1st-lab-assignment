############################################################################
    # ROBOTICS 22-23: actions.py
    # It contanis all the actions needed to connect with the robot
############################################################################

import serial 
import time
import numpy as np
import re

# This function listens the serial port for wait_time seconds
# waiting for ASCII characters to be sent by the robot
# It returns the string of characters
def read_and_wait(ser, wait_time):
    time.sleep(0.4)
    output = ""
    flag = True
    start_time = time.time()
    while flag:
        # Wait until there is data waiting in the serial buffer
        if ser.in_waiting > 0:
            # Read data out of the buffer until a carriage return / new line is found
            serString = ser.readline()
            # Print the contents of the serial data
            try:
                output = serString.decode("Ascii")
                print(serString.decode("Ascii"))
            except:
                pass
        else:
            deltat = time.time() - start_time
            if deltat>wait_time:
                flag = False

    return output

class action(object):
    """ class for the high-level actions to be executed by the robot """

    # Open the serial port NAME_PORT  to communicate with the robot
    def __init__(self):
        self.ser = serial.Serial('COM3', baudrate=9600, bytesize=8, timeout=2, parity='N', xonxoff=0, stopbits=serial.STOPBITS_ONE)
        # erase memory
        # home position
    
    # When all of the points have been processed
    # set the pen's z position to write in the paper
    def lift_pen(self, z_lift):
        #z_lift = 1400
        self.ser.write(bytes("DEFP LIFT\r", "Ascii")), read_and_wait(self.ser,2)
        self.ser.write(bytes("HERE LIFT\r", "Ascii")), read_and_wait(self.ser,2)
        self.ser.write(bytes("SETPVC LIFT Z " + str(z_lift) + "\r", "Ascii")), read_and_wait(self.ser,2)
        self.ser.write(bytes("SPEED 10\r", "Ascii")), read_and_wait(self.ser,2)
        self.ser.write(bytes("MOVE LIFT \r", "Ascii")), read_and_wait(self.ser,2)  

    # Adjust points to robot's referencial
    def init_points(self,origin,path):
        _,coord = path.shape
        for i in range(coord):
            path[:,i] = path[:,i] + origin[i] 

       # Create vector with all the points to draw
    def create_path (self,path):
        points,_ = path.shape
        self.ser.write(bytes("DIMP PATH[" + str(points) + "]\r", "Ascii")), read_and_wait(self.ser,2)

    # Initialize the robot
    def initialize(self):
        self.ser.write(bytes("HOME\r", "Ascii")), read_and_wait(self.ser,2)
        time.sleep(120)
        #1: 2441    2: 2153    3:-10311   4:-14394   5: 189
        #X: 5007    Y: 483     Z: 1351    P:-859     R:-184
        self.ser.write(bytes("DEFP INIT\r", "Ascii")), read_and_wait(self.ser,2)
        self.ser.write(bytes("HERE INIT\r", "Ascii")), read_and_wait(self.ser,2)
        self.ser.write(bytes("SETPV INIT 1 2441\r", "Ascii")), read_and_wait(self.ser,2)
        self.ser.write(bytes("SETPV INIT 2 2153\r", "Ascii")), read_and_wait(self.ser,2)
        self.ser.write(bytes("SETPV INIT 3 -10311\r", "Ascii")), read_and_wait(self.ser,2)
        self.ser.write(bytes("SETPV INIT 4 -14394\r", "Ascii")), read_and_wait(self.ser,2)
        self.ser.write(bytes("SETPV INIT 5 189\r", "Ascii")), read_and_wait(self.ser,2)
        self.ser.write(bytes("SPEED 10\r", "Ascii")), read_and_wait(self.ser,2)
        self.ser.write(bytes("MOVE INIT\r", "Ascii")), read_and_wait(self.ser,2)

    # sets values to the coordinates of a point
    def add_waypoint(self,path, coord, point,z_rest):
        self.ser.write(bytes("HERE PATH[" + str(point+1) + "]\r", "Ascii")), read_and_wait(self.ser,2)
        for i in range(len(coord)): #Only X and Y
            self.ser.write(bytes("SETPVC PATH[" + str(point+1) + "] " + str(coord[i]) + " " + str(path[point][i]) + "\r", "Ascii")), read_and_wait(self.ser,2)
        self.ser.write(bytes("SETPVC PATH[" + str(point+1) + "] Z " + str(z_rest) + "\r", "Ascii")), read_and_wait(self.ser,2)

    # Sets values to the coordinates of a point
    def move_path (self, points):
        time = points * 0.7 * 100
        time = np.ceil(time)
        time_ = time.astype(np.int32)
        self.ser.write(bytes("MOVES PATH 1 " + str(points) + " " + str(time_) + "\r","Ascii")), read_and_wait(self.ser,2)
        
        ser.sleep(time + 1)
        
    # Calibrate the robot by 
    # reading the original position of the pen
    # transform into cartesian coordiantes
    def manual_calibrate(self):
        position = self.ser.write(bytes("LISTPV POSITION\r", "Ascii"))
        self.ser.readline() # discard
        self.ser.readline() # discard
        position_string = self.ser.readline() # read cartesian coordinates
        output = position_string.decode("Ascii")
        print(output)
        ref = []

        coordinates = re.findall(r"[-+]?(?:\d*\.*\d+)", output)        
        for ii in range(len(coordinates)):
            ref.append(int(coordinates[ii]))

        return ref