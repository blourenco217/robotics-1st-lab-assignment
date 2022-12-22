# Robotics 22-23, Lab1 serial communications with the Scorbot example
import serial
import time
import datetime
import numpy as np
from trajectory_planning import reference
from actions import action

# This function listens the serial port for wait_time seconds
# waiting for ASCII characters to be sent by the robot
# It returns the string of characters
def read_and_wait(ser, wait_time):
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

def main():
    print("Starting")

    # Open the serial port COM4 to communicate with the robot (you may have to adjust
    # this instruction in case you are using a Linux OS)
    # (you must check in your computer which ports are available are, if necessary,
    # replace COM4 with the adequate COM)
    # /dev/tty.UEBOOM2-LWACP
    # ser = serial.Serial('/dev/tty.usbserial-1410', baudrate=9600, bytesize=8, timeout=2, parity='N', xonxoff=0, stopbits=serial.STOPBITS_ONE)
    # print("COM port in use: {0}".format(ser.name))

    # print("Homing the robot (if necessary)")
    #ser.write(b'home\r')
    #time.sleep(180) # homing takes a few minutes ...

    serString = "" # Used to hold data coming over UART

    ############################################################################
    # ATTENTION: Each point used was previously recorded with DEFP instruction
    #(from a terminal console - you can use, for example, putty or hyperterminal
    # as terminal console)
    ############################################################################
# [[   0,   33,   67,   90,   81,   64,   33, -135, -168, -183, -152,
#    -128,  -94,  107,  174,  201,  212,  211,  200,  178,  112, -156,
#    -257, -289, -301, -111, -102,  -68,   -1,   39,   39,   33,   11,
#     -22,  -89, -125, -191, -291, -108, -102,   32, -104, -104],
#  [   0,   -5,  -23,  -57, -157, -191, -218, -199, -181, -149,  -14,
#      19,   39,    3,  -40,  -74, -107, -141, -174, -208, -256, -258,
#    -219, -190, -157,  245,  261,  271,  369,  603,  619,  652,  686,
#     711,  731,  678,  633,  613,  478,  476,  610,  473,  272]]

    #coord = np.array(["X","Y","Z","P","R"], dtype = str)
    coord = np.array(["X","Y"], dtype = str)

    #z_offset = -283

    ref = reference()
    path_x,path_y = ref.features2track()
    #path = np.concatenate((path_x,path_y))
    path = np.array([path_x,path_y])
    #path = path.transpose
    #print("act")

    path = np.transpose(path)
    path = path[0:10]
    print(path)
    points,_= path.shape

    z_rest = 1000
    z_lift = 1400






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

    # closing and housekeeping
    # ser.close()

    usesaved = 0 #uses what is on the x and y
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
