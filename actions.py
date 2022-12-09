
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
    

    def calibrate(self, origin):
        """ center pen position in referencial origin """
        self.ser.write(b'DEFP ORI\r'), time.sleep(0.5)
        self.ser.write(b'SETP ORI = P1\r'), time.sleep(0.5)
        self.ser.write(b'SETPVC ORI X ' + (origin[0]).to_bytes(1, byteorder='big') + b'\r'), time.sleep(0.5)
        self.ser.write(b'SETPVC ORI Y ' + (origin[1]).to_bytes(1, byteorder='big') + b'\r'), time.sleep(0.5)
        self.ser.write(b'SETPVC ORI Z ' + (origin[2]).to_bytes(1, byteorder='big') + b'\r'), time.sleep(0.5)
        self.ser.write(b'SETPVC ORI P ' + (origin[3]).to_bytes(1, byteorder='big') + b'\r'), time.sleep(0.5)
        self.ser.write(b'SETPVC ORI R ' + (origin[4]).to_bytes(1, byteorder='big') + b'\r'), time.sleep(0.5)
        self.ser.write (b'MOVE ORI\r')
        #   self.ser.write(b'LISTPV PATH[1]\r'), time.sleep(0.5)
        #   read_and_wait(self.ser,2)
        time.sleep(0.5), read_and_wait(self.ser,2)

    def move_path(self, path, origin):
        path[:][0] = origin[0] + path[:][0]
        path[:][1] = origin[1] + path[:][1]
        path[:][2] = origin[2] + path[:][2]

        self.ser.write(b'DIMP PATH[4]\r'), time.sleep(0.5)
        #1
        self.ser.write(b'HERE PATH[1]\r'), time.sleep(0.5)

        self.ser.write(b'SETPVC PATH[1] X ' + (path[0][0]).to_bytes(1, byteorder='big') + b'\r'), time.sleep(0.5)
        self.ser.write(b'SETPVC PATH[1] Y ' + (path[0][1]).to_bytes(1, byteorder='big') + b'\r'), time.sleep(0.5)
        self.ser.write(b'SETPVC PATH[1] Z ' + (path[0][2]).to_bytes(1, byteorder='big') + b'\r'), time.sleep(0.5)

        self.ser.write(b'TEACH PATH[1]'), time.sleep(0.5)
        self.ser.write(b'MOVE PATH[1]'), time.sleep(0.5)
        self.ser.write(b'HERE PATH[1]'), time.sleep(0.5)

        #2
        self.ser.write(b'HERE PATH[2]'), time.sleep(0.5)

        self.ser.write(b'SETPVC PATH[2] X ' + (path[1][0]).to_bytes(1, byteorder='big') + b'\r'), time.sleep(0.5)
        self.ser.write(b'SETPVC PATH[2] Y ' + (path[1][1]).to_bytes(1, byteorder='big') + b'\r'), time.sleep(0.5)

        self.ser.write(b'TEACH PATH[2]'), time.sleep(0.5)
        self.ser.write(b'MOVE PATH[2]'), time.sleep(0.5)
        self.ser.write(b'HERE PATH[2]'), time.sleep(0.5)

        #3
        self.ser.write(b'HERE PATH[3]'), time.sleep(0.5)

        self.ser.write(b'SETPVC PATH[3] X ' + (path[2][0]).to_bytes(1, byteorder='big') + b'\r'), time.sleep(0.5)
        self.ser.write(b'SETPVC PATH[3] Y ' + (path[2][1]).to_bytes(1, byteorder='big') + b'\r'), time.sleep(0.5)

        self.ser.write(b'TEACH PATH[3]'), time.sleep(0.5)
        self.ser.write(b'MOVE PATH[3]'), time.sleep(0.5)
        self.ser.write(b'HERE PATH[3]'), time.sleep(0.5)

        #4
        self.ser.write(b'HERE PATH[4]'), time.sleep(0.5)

        self.ser.write(b'SETPVC PATH[4] X ' + (path[3][0]).to_bytes(1, byteorder='big') + b'\r'), time.sleep(0.5)
        self.ser.write(b'SETPVC PATH[4] Y ' + (path[3][1]).to_bytes(1, byteorder='big') + b'\r'), time.sleep(0.5)

        self.ser.write(b'TEACH PATH[4]'), time.sleep(0.5)
        self.ser.write(b'MOVE PATH[4]'), time.sleep(0.5)
        self.ser.write(b'HERE PATH[4]'), time.sleep(0.5)

        self.ser.write(b'MOVES PATH 1 4 10000'), time.sleep(0.5) 

    def add_waypoint(self, waypoint, reference, position):
        """ find first point in paper to start drawing """
        self.ser.write(b'DEFP ' + waypoint + b'\r'), time.sleep(0.5)
        self.ser.write(b'TEACHR ' + waypoint + b' ' + reference + b'\r'), time.sleep(0.5) 
        self.ser.write(int.to_bytes(position[0]) + b'\r'), time.sleep(0.5) # x relative
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




