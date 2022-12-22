
import serial 
import time
import numpy as np
import re

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

    def __init__(self):
        self.ser = serial.Serial('COM3', baudrate=9600, bytesize=8, timeout=2, parity='N', xonxoff=0, stopbits=serial.STOPBITS_ONE)
        #self.ser = serial.Serial('/dev/tty.usbserial-1410', baudrate=9600, bytesize=8, timeout=2, parity='N', xonxoff=0, stopbits=serial.STOPBITS_ONE)

        # erase memory
        # home position
    
    def lift_pen(self, z_lift):
        #z_lift = 1400
        self.ser.write(bytes("DEFP LIFT\r", "Ascii")), read_and_wait(self.ser,2)
        self.ser.write(bytes("HERE LIFT\r", "Ascii")), read_and_wait(self.ser,2)
        self.ser.write(bytes("SETPVC LIFT Z " + str(z_lift) + "\r", "Ascii")), read_and_wait(self.ser,2)
        self.ser.write(bytes("SPEED 10\r", "Ascii")), read_and_wait(self.ser,2)
        self.ser.write(bytes("MOVE LIFT \r", "Ascii")), read_and_wait(self.ser,2)


        

    def init_points(self,origin,path):
        """ adjust points to robot's referencial """
        _,coord = path.shape
        for i in range(coord):
            path[:,i] = path[:,i] + origin[i] 
        
    def create_path (self,path):
        """ create position vector """
        points,_ = path.shape
        self.ser.write(bytes("DIMP PATH[" + str(points) + "]\r", "Ascii")), read_and_wait(self.ser,2)

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





    def add_waypoint(self,path, coord, point,z_rest):
        """ sets values to the coordinates of a point """
        # path -> position vector
        # coord -> vector containing coordinates
        #point -> current point
        #print(point)
        self.ser.write(bytes("HERE PATH[" + str(point+1) + "]\r", "Ascii")), read_and_wait(self.ser,2)
        for i in range(len(coord)): #ONLY X AND Y
            self.ser.write(bytes("SETPVC PATH[" + str(point+1) + "] " + str(coord[i]) + " " + str(path[point][i]) + "\r", "Ascii")), read_and_wait(self.ser,2)
        self.ser.write(bytes("SETPVC PATH[" + str(point+1) + "] Z " + str(z_rest) + "\r", "Ascii")), read_and_wait(self.ser,2)

    def move_path (self, points):
        """ teach, move and assign point """
        #self.ser.write(bytes("MOVE PATH[1] \r","Ascii")), read_and_wait(self.ser,2)
        time = points * 0.7 * 100
        time = np.ceil(time)
        time_ = time.astype(np.int32)

        self.ser.write(bytes("MOVES PATH 1 " + str(points) + " " + str(time_) + "\r","Ascii")), read_and_wait(self.ser,2)
        
        ser.sleep(time + 1)

        #final
        #self.ser.write(bytes("DELP PATH\r","Ascii")), read_and_wait(self.ser,2)
        #self.ser.write(bytes("YES\r", "Ascii")), read_and_wait(self.ser,2)
        #self.ser.write(bytes("DELP LIFT\r", "Ascii")), read_and_wait(self.ser,2)
        #self.ser.write(bytes("YES\r", "Ascii")), read_and_wait(self.ser,2)


        



    def manual_calibrate(self):

        position = self.ser.write(bytes("LISTPV POSITION\r", "Ascii"))
        #read_and_wait(self.ser,2)
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





