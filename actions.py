
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
        # erase memory
        # home position
    

    def calibrate(self):
        """ center pen position in referencial origin """
        self.ser.write(b'SETP ORI = 0\r'), time.sleep(0.5)
        self.ser.write(b'SETPVC ORI X 5208\r'), time.sleep(0.5)
        self.ser.write(b'SETPVC ORI Y 538\r'), time.sleep(0.5)
        self.ser.write(b'SETPVC ORI Z -913\r'), time.sleep(0.5)
        self.ser.write(b'SETPVC ORI P -895\r'), time.sleep(0.5)
        self.ser.write(b'SETPVC ORI R -201\r'), time.sleep(0.5)
        self.ser.write (b'MOVED ORI\r')
        time.sleep(0.5), read_and_wait(self.ser,2)

    def add_waypoint(self, waypoint, reference, position):
        """ find first point in paper to start drawing """
        self.ser.write(b'DEFP ' + waypoint + b'\r'), time.sleep(0.5)
        self.ser.write(b'TEACHR ' + waypoint + b' ' + reference + b'\r'), time.sleep(0.5) 
        self.ser.write(position[0] + b'\r'), time.sleep(0.5) # x relative
        self.ser.write(position[1] + b'\r'), time.sleep(0.5) # y relative
        self.ser.write(position[2] + b'\r'), time.sleep(0.5) # z relative
        self.ser.write(position[3] + b'\r'), time.sleep(0.5) # p relative
        self.ser.write(position[4] + b'\r'), time.sleep(0.5) # r relative

        
    def moveto_waypoint(self, waypoint):
        self.ser.write(b'MOVED ' + waypoint + b'\r')
        time.sleep(0.5), read_and_wait(self.ser,2)

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




