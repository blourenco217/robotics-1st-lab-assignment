
import serial 
import time
import numpy as np
import re

def read_and_wait(ser, wait_time):
    time.sleep(0.5)
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
        self.ser = serial.Serial('COM5', baudrate=9600, bytesize=8, timeout=2, parity='N', xonxoff=0, stopbits=serial.STOPBITS_ONE)
        #self.ser = serial.Serial('/dev/tty.usbserial-1410', baudrate=9600, bytesize=8, timeout=2, parity='N', xonxoff=0, stopbits=serial.STOPBITS_ONE)

        # erase memory
        # home position
    

    def moveto_origin(self,origin,coord):  #em principio nao se usa
        """ center pen position in referencial origin """
        self.ser.write(bytes("DELP ORI\r","Ascii")),read_and_wait(self.ser,2)
        self.ser.write(bytes("YES\r", "Ascii")), read_and_wait(self.ser,2)
        self.ser.write(bytes("DEFP ORI\r")), read_and_wait(self.ser,2)
        self.ser.write(bytes("SETP ORI = P1\r")), read_and_wait(self.ser,2)
        for i in range(len(coord)):
            #SETPVC ORI X 200
            self.ser.write(bytes("SETPVC ORI " + coord[i] + " " + str(origin[i]) + "\r", "Ascii")), read_and_wait(self.ser,2)
        self.ser.write (bytes("MOVE ORI\r","Ascii")), read_and_wait(self.ser,2)

    def init_points(self,origin,path):
        """ adjust points to robot's referencial """
        _,coord = path.shape
        print(coord)
        for i in range(coord):
            path[:,i] = path[:,i] + origin[i] 
        
    def create_path (self,path):
        """ create position vector """
        points,_ = path.shape
        self.ser.write(bytes("DELP PATH\r","Ascii")), read_and_wait(self.ser,2)
        self.ser.write(bytes("YES\r", "Ascii")), read_and_wait(self.ser,2)
        self.ser.write(bytes("DIMP PATH[" + str(points) + "]\r", "Ascii")), read_and_wait(self.ser,2)

    def add_waypoint(self,path, coord, point):
        """ sets values to the coordinates of a point """
        # path -> position vector
        # coord -> vector containing coordinates
        #point -> current point
        self.ser.write(bytes("HERE PATH[" + str(point+1) + "]\r", "Ascii")), read_and_wait(self.ser,2)
        for i in range(len(coord)):
            # SETPVC PATH[3] X 500
            self.ser.write(bytes("SETPVC PATH[" + str(point+1) + "] " + str(coord[i]) + " " + str(path[point][i]) + "\r", "Ascii")), read_and_wait(self.ser,2)

    def move_path (self, points):
        """ teach, move and assign point """

        #self.ser.write(bytes("TEACH PATH[" + str(point) + "]\r")), read_and_wait(self.ser,2)
        self.ser.write(bytes("MOVES PATH 1 " + str(points) + " 500\r","Ascii")), read_and_wait(self.ser,2)

        #self.ser.write(bytes("HERE PATH[" + str(point) + "]\r")), read_and_wait(self.ser,2)

            
# may be needed - another way to ser.write
        #setpvc = f"SETPVC ORI  {origin[0]}\r"
        #self.ser.write(bytes(setpvc, "Ascii")), time.sleep(0.5) # also works
        


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


    def old_move(self, path, origin):
        """ center pen position in referencial origin """
        self.ser.write(bytes("DELP ORI\r", "Ascii")), read_and_wait(self.ser,2)
        self.ser.write(bytes("YES\r", "Ascii")), read_and_wait(self.ser,2)
        self.ser.write(bytes("DEFP ORI\r", "Ascii")), read_and_wait(self.ser,2)
        self.ser.write(bytes("SETP ORI = P1\r","Ascii")), read_and_wait(self.ser,2)
        self.ser.write(bytes("SETPVC ORI X " + str(origin[0]) + "\r", "Ascii")), read_and_wait(self.ser,2)
        self.ser.write(bytes("SETPVC ORI Y " + str(origin[1]) + "\r", "Ascii")), read_and_wait(self.ser,2)
        self.ser.write(bytes("SETPVC ORI Z " + str(origin[2]) + "\r", "Ascii")), read_and_wait(self.ser,2)
        self.ser.write(bytes("SETPVC ORI P " + str(origin[3]) + "\r", "Ascii")), read_and_wait(self.ser,2)
        self.ser.write(bytes("SETPVC ORI R " + str(origin[4]) + "\r", "Ascii")), read_and_wait(self.ser,2)
        self.ser.write (bytes("MOVE ORI\r","Ascii")), read_and_wait(self.ser,2)

        path[:,0] = path[:,0]+origin[0]
        path[:,1] = path[:,1]+origin[1]
        path[:,2] = path[:,2]+origin[2]
        points,_= path.shape

        self.ser.write(bytes("DIMP PATH[" + str(points) + "]\r","Ascii")), time.sleep(0.5)
        #1
        for i in range(4):#0123
            print("for")
            self.ser.write(bytes("HERE PATH[" + str(i+1) + "]\r", "Ascii")), time.sleep(0.5)

            self.ser.write(bytes("SETPVC PATH[" + str(i+1) + "] X " + str(path[i][0]) + "\r", "Ascii")), time.sleep(0.5)
            self.ser.write(bytes("SETPVC PATH[" + str(i+1) + "] Y " + str(path[i][1]) + "\r", "Ascii")), time.sleep(0.5)
            self.ser.write(bytes("SETPVC PATH[" + str(i+1) + "] Z " + str(path[i][2]) + "\r", "Ascii")), time.sleep(0.5)

            #self.ser.write(bytes("TEACH PATH[" + str(i+1) + "]\r", "Ascii")), time.sleep(0.5)
            #self.ser.write(bytes("MOVE PATH[" + str(i+1) + "]\r", "Ascii")), time.sleep(0.5)
            #self.ser.write(bytes("HERE PATH[" + str(i+1) + "]\r", "Ascii")), time.sleep(0.5)
        #self.ser.write(b'SPEED 20'), time.sleep(0.5)
        velocity=15
        self.ser.write(bytes("SPEED "+ str(velocity) + "\r"))

        self.ser.write(bytes("MOVES PATH 1 4\r","Ascii")), time.sleep(0.5) 


    # def add_waypoint(self, waypoint, reference, position):
    #     """ find first point in paper to start drawing """
    #     self.ser.write(b'DEFP ' + waypoint + b'\r'), time.sleep(0.5)
    #     self.ser.write(b'TEACHR ' + waypoint + b' ' + reference + b'\r'), time.sleep(0.5) 
    #     self.ser.write(int.to_bytes(position[0]) + b'\r'), time.sleep(0.5) # x relative
    #     self.ser.write(position[1] + b'\r'), time.sleep(0.5) # y relative
    #     self.ser.write(position[2] + b'\r'), time.sleep(0.5) # z relative
    #     self.ser.write(position[3] + b'\r'), time.sleep(0.5) # p relative
    #     self.ser.write(position[4] + b'\r'), time.sleep(0.5) # r relative
    


        
    # def moveto_waypoint(self, waypoint):
    #     self.ser.write(b'MOVED ' + waypoint + b'\r')
    #     time.sleep(0.5), read_and_wait(self.ser,2)

    def moveto_waypoint_linear(self, waypoint):
        self.ser.write(b'MOVELD ' + waypoint + b'\r')
        time.sleep(0.5), read_and_wait(self.ser,2)

    def moveto_waypoint_circular(self, waypoint, pit_waypoint, velocity = 20):
        self.ser.write(b'SPEED '+ velocity + b'\r')
        time.sleep(0.5), read_and_wait(self.ser,2)
        self.ser.write(b'MOVECD ' + waypoint + pit_waypoint + b'\r')
        time.sleep(0.5), read_and_wait(self.ser,2)

        self.ser.write(b'SPEED 50') # reset speed
        time.sleep(0.5), read_and_wait(self.ser,2)




