# FWest 20.07.2023 Jython in Bruker TopSpin
# Script for sending commands to Arduino from inside of TopSpin
# This script retrieves spectral parameters by the TopSpin specific syntax
# 

import sys
import os

# Path to the Python3 interpreter outside of TopSpin
pythonpath = "C:/Users/LocalAdmin/AppData/Local/Programs/Python/Python310/python.exe"
# Path to the script to be called from outside of TopSpin
scriptpath = "C:/Bruker/TopSpin4.2.0/exp/stan/nmr/py/user/wef_arduino_sys_py_win.py"

# Light-logfile will be in what getcwd prints
# print(os.getcwd())
sysstring = pythonpath + ' ' + scriptpath
### Here you can freely retrieve and handle TopSpin specific commandds, read vars etc.
arglist = [GETPAR2("CNST 60"), GETPAR2("CNST 61")]
argstring = ''
for arg in arglist:
    argstring += str(arg) + ' '
os.system(sysstring + ' ' + argstring)