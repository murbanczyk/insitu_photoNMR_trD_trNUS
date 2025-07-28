import sys
import os

# Path to the Python3 interpreter outside of TopSpin
pythonpath = "/home/murb/anaconda3/bin/python3"
# Path to the script to be called from outside of TopSpin
#scriptpath = "/home/murb/wef_illumination/wef_arduino_sys_py.py"
scriptpath = "/opt/topspin3.2/exp/stan/nmr/py/user/wef_arduino_sys_py.py"
sysstring = pythonpath + ' ' + scriptpath
# Light-logfile will be in what getcwd prints
# print(os.getcwd())

### Here you can freely retrieve and handle TopSpin specific commandds, read vars etc.
arg1 = GETPAR2("CNST 60")
arg2 = GETPAR2("CNST 61")

# C:\Users\LocalAdmin\AppData\Local\Programs\Python\Python310\

#os.system("C:/Users/LocalAdmin/AppData/Local/Programs/Python/Python310/python C:/wef/Arduino_controller_python/main/arduino_serial.py " + arg1 + ' ' + arg2)

os.system(sysstring + " " + arg1 + ' ' + arg2)
