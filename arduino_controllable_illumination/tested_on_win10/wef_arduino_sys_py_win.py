# FWest 20.07.2023 Python3
# Script to send commands to Arduino via serial communication
# and receive an answer if sending worked properly
#
# It can run as standalone in the commandline:
# python3 wef_arduino_sys_py.py arg1 arg2
# But intended use is to be called from a script inside of Bruker TopSpin
# to control the power output of a lightsource in in-situ illuminated NMR-experiments
# All arguments can be integers between 0 and 255,
# which represent the command to be executed and parameters passed with it.
# Arduino can read up to 10 such arguments at a Baud-rate of 115200 (recommended)
# After sending to Arduino, the program will try to receive a confirmation from Arduino
# If an answer is received it will be printed on the console and looks like:
# 18/05/2023, 09:20:33 ::: Received: 0:3, 1:58, 
# This message is also saved in a wef_logfile.txt in the current working directory
# of the program.

import serial
import io
import sys
import time
import datetime

# To be set by the user!
# On Windows serial ports are named COM followed by a number, it can be found by connecting the Arduino to the Computer via USB
# and opening the device manager at 'Connections (COM & LPT)
# On Linux systems the port usually is 'dev/ttyACM0' to work properly, the user has to be a member of the 'dialout' group
# usermod -a -G dialout <username>

port_location = 'COM7' 
# The baudrate has to match the one set and uploaded to Arduino (use 115200 or 9600)

baud_rate = 115200


# with serial.Serial('COM7', 115200, timeout=1) as ser:
#     #time.sleep(1)   # Give the program a second to set up the port, missing information otherwise
#                      # Not Needed anymore if Arduino RESET EN is cut ;)
#     # Do not forget to add '\n' character! for line termination
#     ser.write((sendstring+'\n').encode())
#     #print(sendstring)
#     #print((sendstring+'\n').encode())
#     time.sleep(0.1)
#     # Arduino reprints what was sent to the serial monitor
#     if (ser.in_waiting > 0):
#         time.sleep(0.2)
#         receivestring = b""
#         while (ser.in_waiting > 0):
#             receivestring += ser.read(size=1)
#         receivestring = receivestring.decode("ascii")
#         print (datetime.datetime.now().strftime("%d/%m/%Y, %H:%M:%S") + " ::: " +receivestring,end = '')
#     ser.flush()
# with open("light_logfile.txt", "a") as logfile:
#     logfile.write(datetime.datetime.now().strftime("%d/%m/%Y, %H:%M:%S") + " ::: ")
#     logfile.write(str(receivestring) + '\n')


sendstring = ""
receivestring = b"" # Receivestring has to be bytestring
for arg in sys.argv[1::]:
        sendstring += (str(arg)+" ")
    
with serial.Serial(port_location, baud_rate, timeout=1) as ser:
    # Do not forget to add '\n' character! for line termination
    ser.write((sendstring+'\r\n').encode())
    time.sleep(0.5)
    # Arduino reprints what was sent to the serial monitor
    if (ser.in_waiting > 0):
        #time.sleep(0.5)
        receivestring = b""
        while (ser.in_waiting > 0):
            receivestring += ser.read(size=1)
        receivestring = receivestring.decode("ascii")
        
        print (datetime.datetime.now().strftime("%d/%m/%Y, %H:%M:%S") + " ::: " +str(receivestring).strip('\r\n'))
    ser.flush()
with open("wef_logfile.txt", "a") as logfile:
    logfile.write(datetime.datetime.now().strftime("%d/%m/%Y, %H:%M:%S") + " ::: ")
    logfile.write(str(receivestring).strip('\r\n') + '\n')
