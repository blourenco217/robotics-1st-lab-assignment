############################################################################
    # ROBOTICS 22-23: actions.py
    # It contanis all the actions needed to connect with the robot
############################################################################

import serial 
import time
import numpy as np
import re


""" this function listens the serial port for wait_time seconds waiting for ASCII characters to be sent by the robot 
    it returns a string of characters """
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

""" class for the high-level actions to be executed by the robot """
class action(object):
    """ open the serial port NAME_PORT  to communicate with the robot """
    def __init__(self):
        self.ser = serial.Serial('COM4', baudrate=9600, bytesize=8, timeout=2, parity='N', xonxoff=0, stopbits=serial.STOPBITS_ONE)
        self.ser.flush()


    """ calibrate the robot by reading the original position of the pen and saving its coordinates """
    def manual_calibrate(self):
        position = self.ser.write(bytes("LISTPV POSITION\r", "Ascii"))
        self.ser.readline() # discard
        self.ser.readline() # discard
        position_string = self.ser.readline() # read cartesian coordinates
        output = position_string.decode("Ascii")
        ref = []

        coordinates = re.findall(r"[-+]?(?:\d*\.*\d+)", output) # finds int variables
        for ii in range(len(coordinates)):
            ref.append(int(coordinates[ii]))

        return ref

    """ initialize the robot - from home to a safe position """
    def initialize(self, home = False):
        if home:
            self.ser.write(bytes("HOME\r", "Ascii")), read_and_wait(self.ser,2)
            time.sleep(150)

        origin = np.array([5007, 483, 1351, -859, -184])
        # safe position defined based on laboratory measurements as
        # 1: 2441    2: 2153    3:-10311   4:-14394   5: 189
        # X: 5007    Y: 483     Z: 1351    P:-859     R:-184
        self.ser.write(bytes("DEFP INIT\r", "Ascii")), read_and_wait(self.ser,2)
        self.ser.write(bytes("HERE INIT\r", "Ascii")), read_and_wait(self.ser,2)
        self.ser.write(bytes("SETPV INIT 1 2441\r", "Ascii")), read_and_wait(self.ser,2)
        self.ser.write(bytes("SETPV INIT 2 2153\r", "Ascii")), read_and_wait(self.ser,2)
        self.ser.write(bytes("SETPV INIT 3 -10311\r", "Ascii")), read_and_wait(self.ser,2)
        self.ser.write(bytes("SETPV INIT 4 -14394\r", "Ascii")), read_and_wait(self.ser,2)
        self.ser.write(bytes("SETPV INIT 5 189\r", "Ascii")), read_and_wait(self.ser,2)
        self.ser.write(bytes("SPEED 10\r", "Ascii")), read_and_wait(self.ser,2)
        self.ser.write(bytes("MOVE INIT\r", "Ascii")), read_and_wait(self.ser,2)

        return origin

    """ adjust points to robot's origin """
    def init_points(self,origin,path):
        _,coord = path.shape
        for i in range(coord):
            path[:,i] = path[:,i] + origin[i] 

    """ create vector with all the points to draw """
    def create_path (self,path,roll):
        n_points,_ = path.shape
        if roll:
            n_points = n_points*2 + 1 # for roll coordinates has double the points plus one for lifting pen
        else: 
            n_points = n_points + 1 # plus one for lifting pen

        self.ser.write(bytes("DIMP PATH[" + str(n_points) + "]\r", "Ascii")), read_and_wait(self.ser,2) # defines vector
  
    """ sets values to the coordinates of a point """
    """ without roll's coordinates"""
    def add_waypoint(self,path, coord, point,z_rest):
        self.ser.write(bytes("HERE PATH[" + str(point+1) + "]\r", "Ascii")), read_and_wait(self.ser,2)
        for i in range(len(coord)): #Only X and Y
            self.ser.write(bytes("SETPVC PATH[" + str(point+1) + "] " + str(coord[i]) + " " + str(path[point][i]) + "\r", "Ascii")), read_and_wait(self.ser,2)
        self.ser.write(bytes("SETPVC PATH[" + str(point+1) + "] Z " + str(z_rest) + "\r", "Ascii")), read_and_wait(self.ser,2)

    """ with roll's coordinates"""
    def add_waypoint_roll(self,path, coord, point, point_robot,  roll, z_rest):
        self.ser.write(bytes("HERE PATH[" + str(point_robot) + "]\r", "Ascii")), read_and_wait(self.ser,2)
        for i in range(len(coord)): #Only X and Y
            self.ser.write(bytes("SETPVC PATH[" + str(point_robot) + "] " + str(coord[i]) + " " + str(path[point][i]) + "\r", "Ascii")), read_and_wait(self.ser,2)
        self.ser.write(bytes("SETPVC PATH[" + str(point_robot) + "] Z " + str(z_rest) + "\r", "Ascii")), read_and_wait(self.ser,2)
        self.ser.write(bytes("SETPVC PATH[" + str(point_robot) + "] R " + str(roll) + "\r", "Ascii")), read_and_wait(self.ser,2) 


    """ add the lift pen as the last point to be sent to the robot """
    """ without roll's coordinates"""
    def add_lift_pen(self,path, coord, point,z_lift): 
        self.ser.write(bytes("HERE PATH[" + str(point+1) + "]\r", "Ascii")), read_and_wait(self.ser,2)
        for i in range(len(coord)): #Only X and Y
            self.ser.write(bytes("SETPVC PATH[" + str(point+1) + "] " + str(coord[i]) + " " + str(path[point-1][i]) + "\r", "Ascii")), read_and_wait(self.ser,2)
        self.ser.write(bytes("SETPVC PATH[" + str(point+1) + "] Z " + str(z_lift) + "\r", "Ascii")), read_and_wait(self.ser,2)

    """ with roll's coordinates """
    def add_lift_pen_roll(self,path, coord, point, point_robot, z_lift): 
        self.ser.write(bytes("HERE PATH[" + str(point_robot) + "]\r", "Ascii")), read_and_wait(self.ser,2)
        for i in range(len(coord)): #Only X and Y
            self.ser.write(bytes("SETPVC PATH[" + str(point_robot) + "] " + str(coord[i]) + " " + str(path[point-1][i]) + "\r", "Ascii")), read_and_wait(self.ser,2)
        self.ser.write(bytes("SETPVC PATH[" + str(point_robot) + "] Z " + str(z_lift) + "\r", "Ascii")), read_and_wait(self.ser,2)

    """ set values to the coordinates of a point """
    """ without roll's coordinates"""
    def move_path (self, points):
        points = points + 1 # all the points + lift pen
        exc_time = points * 0.8 * 100 # average time per point
        exc_time = np.ceil(exc_time)
        exc_time_int = exc_time.astype(np.int32)
        self.ser.write(bytes("MOVES PATH 1 " + str(points) + " " + str(exc_time_int) + "\r","Ascii")), read_and_wait(self.ser,2)
        exc_time = exc_time / 100
        time.sleep(exc_time)

    """ with roll's coordinates """
    def move_path_roll (self, points):
        points = points*2 + 1 # all the points x 2 (bc first set the roll and then move) + lift pen
        exc_time = points * 0.8 * 100 # average time per point
        exc_time = np.ceil(exc_time)
        for i in range(1, points): # move to point one by one
            self.ser.write(bytes("MOVE PATH [" + str(i) + "]\r","Ascii")), read_and_wait(self.ser,2)
        exc_time = exc_time / 100
        time.sleep(exc_time)

    """ disconnect the robot and delete the used variables """
    def disconnect(self):
        # delete used variables
        self.ser.write(bytes("DELP PATH\r","Ascii")), read_and_wait(self.ser,2)
        self.ser.write(bytes("YES\r", "Ascii")), read_and_wait(self.ser,2)
        self.ser.write(bytes("DELP INIT\r", "Ascii")), read_and_wait(self.ser,2)
        self.ser.write(bytes("YES\r", "Ascii")), read_and_wait(self.ser,2)

        # closed connection
        self.ser.close()