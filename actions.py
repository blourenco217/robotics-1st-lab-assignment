
import serial
import time

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

class action(object):
    """ class for the high-level actions to be executed by the robot """

    def __init__(self):
        self.ser = serial.Serial('/dev/tty.usbserial-1410', baudrate=9600, bytesize=8, timeout=2, parity='N', xonxoff=0, stopbits=serial.STOPBITS_ONE)
    

    def calibrate(self):
        """ center pen position in referencial origin """
        # create a position called origin

    def add_waypoint(self, waypoint):
        self.ser.write(b'TEACHR ORIGIN {}'.format(waypoint))
        time.sleep(0.5), read_and_wait(self.ser,2)
        self.ser.write(b'HERE P\r')   # rename position/ waypoint
        time.sleep(0.5), read_and_wait(self.ser,2)
        
    def moveto_waypoint(self, waypoint):
        self.ser.write(b'MOVE ' + waypoint + b'\r')
        time.sleep(0.5)
        read_and_wait(self.ser,2)

    def moveto_waypoint_linear(self, waypoint):
        self.ser.write(b'MOVEL P\r')
        time.sleep(0.5), read_and_wait(self.ser,2)

    def moveto_waypoint_circular(self, waypoint, pit_waypoint, velocity = 20):
        self.ser.write(b'SPEED {}\r'.format(velocity))
        time.sleep(0.5), read_and_wait(self.ser,2)
        self.ser.write(b'MOVEC {} {}\r'.format(waypoint, pit_waypoint))
        time.sleep(0.5), read_and_wait(self.ser,2)

        self.ser.write(b'SPEED 50') # reset speed
        time.sleep(0.5), read_and_wait(self.ser,2)




