# Robotics 22-23, Lab1 serial communications with the Scorbot example
import serial
import time
import datetime
import numpy as np
from image_processing import reference_tracking

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


    # print('going to point P1')
    # ser.write(b'MOVE P1\r')
    # time.sleep(0.5)
    # read_and_wait(ser,2)

    # print('going to point P2')
    # ser.write(b'MOVE P2\r')
    # time.sleep(0.5)
    # read_and_wait(ser,2)

# X: 4853    Y: 887     Z: 1110    P:-747     R:-191


    #origin = np.array([4853, 887, 1110, -747, -191])
    coord = np.array(["X","Y","Z","P","R"], dtype = str)
    z_offset = -283

    #path = np.array ([[0,-500,0,0,0],[500,-500,0,0,0],[500,0,0,0,0],[0,0,0,0,0]])
    path_ = reference_tracking()
    path_x,path_y = path_.features2track()
    path_x, path_y = path_.image_normalization(path_x,path_y)
    path = np.zeros((len(path_x), 5))
    for ii in range(len(path_x)):
        path[ii][0] = path_x[ii]
        path[ii][1] = path_y[ii]
        # path[ii][2] = 0
        # path[ii][3] = 0
        # path[ii][4] = 0
  

    act = action()

    new = 1
    if new == 0:
        origin = act.manual_calibrate()
        act.old_move(path,origin)
    else:
        origin = act.manual_calibrate()
        #act.moveto_origin(origin,coord)
        act.init_points(origin,path)
        act.create_path(path)
        points,_= path.shape
        for i in range(points):
            act.add_waypoint(path,coord,i)
        act.move_path(points)

    


    # closing and housekeeping
    # ser.close()

    print('housekeeping completed - exiting')
    

########################################################################
if __name__ == '__main__':
    main()
