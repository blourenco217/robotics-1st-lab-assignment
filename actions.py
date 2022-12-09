
import serial
import time
import numpy as np

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
        self.ser = serial.Serial('COM4', baudrate=9600, bytesize=8, timeout=2, parity='N', xonxoff=0, stopbits=serial.STOPBITS_ONE)
        #self.ser = serial.Serial('/dev/tty.usbserial-1410', baudrate=9600, bytesize=8, timeout=2, parity='N', xonxoff=0, stopbits=serial.STOPBITS_ONE)

        # erase memory
        # home position
    

    def calibrate(self, origin):
        """ center pen position in referencial origin """
        #self.ser.write(b'DELP ORI\r'), time.sleep(0.5)
        self.ser.write(b'DEFP ORI\r'), time.sleep(0.5)
        self.ser.write(b'SETP ORI = P1\r'), time.sleep(0.5)
        #dim =4
        #coord = np.array(["X","Y","Z","P","R"])
        #for i in range(dim):  
        #    setpvc = f"SETPVC ORI X {origin[0]}\r"
        #self.ser.write(bytes(setpvc, "Ascii")), time.sleep(0.5) also works
        self.ser.write(bytes("SETPVC ORI X " + str(origin[0]) + "\r", "Ascii")), time.sleep(0.5)
        self.ser.write(bytes("SETPVC ORI Y " + str(origin[1]) + "\r", "Ascii")), time.sleep(0.5)
        self.ser.write(bytes("SETPVC ORI Z " + str(origin[2]) + "\r", "Ascii")), time.sleep(0.5)
        self.ser.write(bytes("SETPVC ORI P " + str(origin[3]) + "\r", "Ascii")), time.sleep(0.5)
        self.ser.write(bytes("SETPVC ORI R " + str(origin[4]) + "\r", "Ascii")), time.sleep(0.5)
        self.ser.write (bytes("MOVE ORI\r","Ascii"))
        #   self.ser.write(b'LISTPV PATH[1]\r'), time.sleep(0.5)
        #   read_and_wait(self.ser,2)
        time.sleep(0.5), read_and_wait(self.ser,2)

    def move_path(self, path, origin):
        path[:,0] = path[:,0]+origin[0]
        path[:,1] = path[:,1]+origin[1]
        path[:,2] = path[:,2]+origin[2]

        self.ser.write(b'DIMP PATH[4]\r'), time.sleep(0.5)
        #1
        self.ser.write(b'HERE PATH[1]\r'), time.sleep(0.5)

        self.ser.write(bytes("SETPVC PATH[1] X " + str(path[0][0]) + "\r", "Ascii")), time.sleep(0.5)
        self.ser.write(bytes("SETPVC PATH[1] Y " + str(path[0][1]) + "\r", "Ascii")), time.sleep(0.5)
        self.ser.write(bytes("SETPVC PATH[1] Z " + str(path[0][2]) + "\r", "Ascii")), time.sleep(0.5)

        self.ser.write(b'TEACH PATH[1]'), time.sleep(0.5)
        self.ser.write(b'MOVE PATH[1]'), time.sleep(0.5)
        self.ser.write(b'HERE PATH[1]'), time.sleep(0.5)

        #2
        self.ser.write(b'HERE PATH[1]\r'), time.sleep(0.5)

        self.ser.write(bytes("SETPVC PATH[2] X " + str(path[1][0]) + "\r", "Ascii")), time.sleep(0.5)
        self.ser.write(bytes("SETPVC PATH[2] Y " + str(path[1][1]) + "\r", "Ascii")), time.sleep(0.5)
        self.ser.write(bytes("SETPVC PATH[2] Z " + str(path[1][2]) + "\r", "Ascii")), time.sleep(0.5)

        self.ser.write(b'TEACH PATH[2]'), time.sleep(0.5)
        self.ser.write(b'MOVE PATH[2]'), time.sleep(0.5)
        self.ser.write(b'HERE PATH[2]'), time.sleep(0.5)   

        #3
        self.ser.write(b'HERE PATH[3]\r'), time.sleep(0.5)

        self.ser.write(bytes("SETPVC PATH[3] X " + str(path[2][0]) + "\r", "Ascii")), time.sleep(0.5)
        self.ser.write(bytes("SETPVC PATH[3] Y " + str(path[2][1]) + "\r", "Ascii")), time.sleep(0.5)
        self.ser.write(bytes("SETPVC PATH[3] Z " + str(path[2][2]) + "\r", "Ascii")), time.sleep(0.5)

        self.ser.write(b'TEACH PATH[3]'), time.sleep(0.5)
        self.ser.write(b'MOVE PATH[3]'), time.sleep(0.5)
        self.ser.write(b'HERE PATH[3]'), time.sleep(0.5)        
        #4
        self.ser.write(b'HERE PATH[4]\r'), time.sleep(0.5)

        self.ser.write(bytes("SETPVC PATH[4] X " + str(path[3][0]) + "\r", "Ascii")), time.sleep(0.5)
        self.ser.write(bytes("SETPVC PATH[4] Y " + str(path[3][1]) + "\r", "Ascii")), time.sleep(0.5)
        self.ser.write(bytes("SETPVC PATH[4] Z " + str(path[3][2]) + "\r", "Ascii")), time.sleep(0.5)

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




