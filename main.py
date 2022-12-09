# Robotics 22-23, Lab1 serial communications with the Scorbot example
import serial
import time
import datetime

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


    origin = (5386, 963, 1499, -845, -201)
    path = action()

    path.calibrate(origin)
    z_offset = -100
    #pvect = ([500,-500,][-500,500])
    #path.move_path(pvect)
    #pathpygame.examples.vgrade.main()
    pvect = ((500,500,-283),(500,-500,0),(-500,-500,0),(-500,500,0))
    path.move_path(pvect, origin)    # path.add_waypoint(b'SQ1', b'ORI', position) # add waypoint ISA from a distance (0,0,0,0,0) from ORI
    # path.moveto_waypoint(b'SQ1')
    # position = (-500,500,-270,0,0)
    # path.add_waypoint(b'SQ2', b'ORI', position) 
    # path.moveto_waypoint(b'SQ2')
    # position = (-500,-500,-270,0,0)
    # path.add_waypoint(b'SQ3', b'ORI', position)
    # path.moveto_waypoint(b'SQ3')
    # position = (500,-500,-270,0,0)
    # path.add_waypoint(b'SQ4', b'ORI', position) 
    # path.moveto_waypoint(b'SQ4')


    # closing and housekeeping
    # ser.close()

    print('housekeeping completed - exiting')
    

########################################################################
if __name__ == '__main__':
    main()
