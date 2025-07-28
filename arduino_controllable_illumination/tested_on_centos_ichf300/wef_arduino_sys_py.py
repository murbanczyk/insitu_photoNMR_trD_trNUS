# FWest May 2023 Python 3.8
# Communication script for sending Arduino Commands 
# This version was tested on CentOS 6.9 32-bit to run commands
# from the TopSpin 3.2 interface to Arduino R3 and R4 wifi
# Both Controllers work.
# Remember to adjust the Port and Baudrate to your specific system

import serial
import io
import sys
import time
import datetime



sendstring = ""

# Read command line arguments and pass them into a string to be SENT
for arg in sys.argv[1::]:
        sendstring += (str(arg)+" ")
    


receivestring = b"" # Receivestring has to be bytestring

# For some reason, other baudrates than 9600 may lead to receive errors,
# I.e. the message coming back is printed wrong. but sending works fine
with serial.Serial('/dev/ttyACM0', 115200, timeout=1) as ser:
    #time.sleep(1)   # Give the program a second to set up the port, missing information otherwise
                     # Not Needed anymore if Arduino RESET EN is cut ;)
    # Do not forget to add '\n' character! for line termination
    ser.write((sendstring+'\n').encode())
    #print(sendstring)
    #print((sendstring+'\n').encode())
    time.sleep(0.1)
    # Arduino reprints what was sent to the serial monitor
    if (ser.in_waiting > 0):
        time.sleep(0.2)
        receivestring = b""
        while (ser.in_waiting > 0):
            receivestring += ser.read(size=1)
        receivestring = receivestring.decode("ascii")
        print (datetime.datetime.now().strftime("%d/%m/%Y, %H:%M:%S") + " ::: " +receivestring,end = '')
    ser.flush()
with open("light_logfile.txt", "a") as logfile:
    logfile.write(datetime.datetime.now().strftime("%d/%m/%Y, %H:%M:%S") + " ::: ")
    logfile.write(str(receivestring) + '\n')

    
    



