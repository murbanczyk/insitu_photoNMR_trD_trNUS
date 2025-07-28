# Set of scripts to set-up a interleaved TR-NUS and TR-D NMR acquisition with a illumination control via Arduino



1. Instruction. Set up Arduino control using instructions in folder: arduino_controllable_illumination
2. Import multizg-trends-trdosy_ilumin.py to TopSpin Jython directory (edpy -> import script) 
3. Import script multizg_illumination to TopSpin au directory (au -> import script)
4. Launch multizg-trends-trdosy_ilumin.py.  The GUI is based on TReNDS acquisition script (trends.spektrino.com). The illumination power file should be formated as list of integers from 0 (no illumination) to 255 (full illumination).
5. When the acquisition file structure is prepared go to first experiment and launch multizg_illumination.



The Arduino control was developed by Franz F. Westermair


The multizg-trends-trdosy_ilumin.py  was developed by Mateusz Urbańczyk
