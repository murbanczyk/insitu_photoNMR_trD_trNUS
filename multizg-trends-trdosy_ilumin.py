#!/usr/local/bin/jython
# -*- coding: utf-8 -*-
import os
import shutil
import threading
import time
import datetime
from java.awt import *
from javax.swing import *
from javax.swing.filechooser import FileNameExtensionFilter


class TopTReND(JFrame):
    def __init__(self):
        super(TopTReND, self).__init__()
        self.initUI()

    def initUI(self):
        stepsTXT = JLabel('Steps for IL acquisition:   ')
        Spacer1 = JLabel(' \n')
        Exp1 = JLabel('\n\n\n*******************2D exp No 1*******************\n\n\n')
        Exp2 = JLabel('\n*******************2D exp No 2*******************\n')
        Exp3 = JLabel('\n*******************2D exp No 3*******************\n')
        ExpTR = JLabel('\n*******************TR DOSY exp *******************\n')	
        self.twodimpathTR=''
        Spacer = JLabel(' \n\n ****************************************\n\n   ')
        Spacer2 = JLabel(' \n\n ****************************************\n\n   ')
        numof = JLabel('Number of 2D exp:  ')
        self.samp = JButton('Choose sampling schedule', actionPerformed=self.FileChooser)
        self.samp2 = JButton('Choose sampling schedule', actionPerformed=self.FileChooser2)
        self.samp3 = JButton('Choose sampling schedule', actionPerformed=self.FileChooser3)
        self.Patern2D = JButton('Choose experiment to be used as 2D template', actionPerformed=self.TwodimPatern)
        self.Patern2D_1 = JButton('Choose experiment to be used as 2D template', actionPerformed=self.TwodimPatern2)
        self.Patern2D_2 = JButton('Choose experiment to be used as 2D template', actionPerformed=self.TwodimPatern3)
        self.Patern2D_tr = JButton('Choose experiment to be used as TR DOSY template',
                                   actionPerformed=self.TwodimPaternTR)
        self.sampTR = JButton('Choose sampling schedule', actionPerformed=self.FileChooserTR)
        self.fileBtnIlumin = JButton('Choose  Power sampling schedule', actionPerformed=self.FileChooserIlumin)

        self.Patern1D = JButton('Choose experiment to be used as 1D template', actionPerformed=self.OnedimPatern)
        self.SaveDir = JButton('Choose Directory to save data', actionPerformed=self.DirChooser)
        self.RunBTN = JButton('Start Acquisition!', actionPerformed=self.onRunt)
        self.StopBTN = JButton('Stop Acquisition!', actionPerformed=self.onStop)
        self.StopBTN.setEnabled(False)
        spin2 = SpinnerNumberModel(100.0, 1.0, 999999.0, 1.0)
        spin = SpinnerNumberModel(1.0, 1.0, 3.0, 1.0)
        self.numofexp = JSpinner(spin)
        self.steps = JSpinner(spin2)
        self.twodionly = JCheckBox('2D acquisition only')
        self.setTitle('TReNDS  Acquisition module for TopSpin with TR-DOSY')  # create window with title
        self.setSize(600, 700)  # set window size x, y
        self.panel1 = JPanel()
        self.panel2 = JPanel()
        self.panel4 = JPanel()
        self.panel1.setAlignmentX(Component.LEFT_ALIGNMENT)
        self.panel2.setAlignmentX(Component.LEFT_ALIGNMENT)
        self.panel4.setAlignmentX(Component.LEFT_ALIGNMENT)
        layoutout1 = BoxLayout(self.panel1, BoxLayout.Y_AXIS)
        layoutout2 = BoxLayout(self.panel2, BoxLayout.X_AXIS)
        layoutout3 = BoxLayout(self.panel4, BoxLayout.X_AXIS)
        self.panel1.setLayout(layoutout1)
        self.panel2.setLayout(layoutout2)
        self.panel4.setLayout(layoutout3)
        self.setLayout(FlowLayout())  # layout manager for horizontal alignment
        self.add(self.panel1)
        self.panel1.add(self.panel2)
        self.panel1.add(JLabel('\n'))
        self.panel1.add(self.Patern1D)
        self.panel1.add(self.twodionly)
        self.panel1.add(self.fileBtnIlumin)
        self.panel1.add(JLabel('\n'))
        self.panel1.add(Exp1)
        self.panel1.add(JLabel('\n'))
        self.panel1.add(self.samp)
        self.panel1.add(self.Patern2D)
        self.panel1.add(JLabel('\n'))
        self.panel1.add(Exp2)
        self.panel1.add(JLabel('\n'))
        self.panel1.add(self.samp2)
        self.panel1.add(self.Patern2D_1)
        self.panel1.add(JLabel('\n'))
        self.panel1.add(Exp3)
        self.panel1.add(JLabel('\n'))
        self.panel1.add(self.samp3)
        self.panel1.add(self.Patern2D_2)
        self.panel1.add(JLabel('\n'))
        self.panel1.add(ExpTR)
        self.panel1.add(JLabel('\n'))
        self.panel1.add(self.sampTR)
        self.panel1.add(self.Patern2D_tr)
        self.panel1.add(JLabel('\n'))
        self.panel1.add(Spacer2)
        self.panel1.add(JLabel('\n'))
        self.panel1.add(self.SaveDir)
        self.panel1.add(Spacer1)
        self.panel1.add(Spacer)
        self.panel1.add(self.panel4)
        self.panel4.add(self.RunBTN)
        self.panel4.add(JLabel('\t'))
        self.panel4.add(self.StopBTN)
        self.panel2.add(stepsTXT)
        self.panel2.add(self.steps)
        self.panel2.add(numof)
        self.panel2.add(self.numofexp)

        self.setDefaultCloseOperation(JFrame.DISPOSE_ON_CLOSE)
        self.setVisible(True)
        self.setAlwaysOnTop(True)

    def FileChooser(self, e):
        self.setAlwaysOnTop(False)

        chooseFile = JFileChooser()
        filter1 = FileNameExtensionFilter("sampling schedule", [".sch"])
        chooseFile.addChoosableFileFilter(filter1)

        ret = chooseFile.showDialog(JPanel(), "Choose file")

        if ret == JFileChooser.APPROVE_OPTION:
            file = chooseFile.getSelectedFile()
            self.sampfile = file.getCanonicalPath()
            mes = "Sampling file: " + self.sampfile + " have been chosen"
            SHOW_STATUS(message=mes)
            self.samp.setText(mes)
        self.setAlwaysOnTop(True)

    def FileChooser2(self, e):
        self.setAlwaysOnTop(False)

        chooseFile = JFileChooser()
        filter1 = FileNameExtensionFilter("sampling schedule", [".sch"])
        chooseFile.addChoosableFileFilter(filter1)

        ret = chooseFile.showDialog(JPanel(), "Choose file")

        if ret == JFileChooser.APPROVE_OPTION:
            file = chooseFile.getSelectedFile()
            self.sampfile2 = file.getCanonicalPath()
            mes = "Sampling file: " + self.sampfile + " have been chosen"
            SHOW_STATUS(message=mes)
            self.samp2.setText(mes)
        self.setAlwaysOnTop(True)

    def FileChooser3(self, e):
        self.setAlwaysOnTop(False)

        chooseFile = JFileChooser()
        filter1 = FileNameExtensionFilter("sampling schedule", [".sch"])
        chooseFile.addChoosableFileFilter(filter1)

        ret = chooseFile.showDialog(JPanel(), "Choose file")

        if ret == JFileChooser.APPROVE_OPTION:
            file = chooseFile.getSelectedFile()
            self.sampfile3 = file.getCanonicalPath()
            mes = "Sampling file: " + self.sampfile + " have been chosen"
            SHOW_STATUS(message=mes)
            self.samp3.setText(mes)
        self.setAlwaysOnTop(True)

    def FileChooserTR(self, e):
        self.setAlwaysOnTop(False)

        chooseFile = JFileChooser()
        filter1 = FileNameExtensionFilter("gradient schedule", [".txt"])
        chooseFile.addChoosableFileFilter(filter1)

        ret = chooseFile.showDialog(JPanel(), "Choose file")

        if ret == JFileChooser.APPROVE_OPTION:
            file = chooseFile.getSelectedFile()
            self.sampfileTR = file.getCanonicalPath()
            mes = "Sampling file: " + self.sampfileTR + " have been chosen"
            SHOW_STATUS(message=mes)
            self.sampTR.setText(mes)
        self.setAlwaysOnTop(True)

    def FileChooserIlumin(self,e):
        self.setAlwaysOnTop(False)

        chooseFile = JFileChooser()
        filter1 = FileNameExtensionFilter("gradient schedule", [".txt"])
        chooseFile.addChoosableFileFilter(filter1)

        ret = chooseFile.showDialog(JPanel(), "Choose file")

        if ret == JFileChooser.APPROVE_OPTION:
            file = chooseFile.getSelectedFile()
            self.sampfileIlumin = file.getCanonicalPath()
            mes = "Sampling file: " + self.sampfileIlumin + " have been chosen"
            SHOW_STATUS(message=mes)
            self.fileBtnIlumin.setText(mes)
        
    def DirChooser(self, e):
        self.setAlwaysOnTop(False)

        chooseFile = JFileChooser()
        chooseFile.setFileSelectionMode(JFileChooser.DIRECTORIES_ONLY)
        filter1 = FileNameExtensionFilter("sampling schedule", [".sch"])
        chooseFile.addChoosableFileFilter(filter1)

        ret = chooseFile.showDialog(JPanel(), "Choose file")

        if ret == JFileChooser.APPROVE_OPTION:
            file = chooseFile.getSelectedFile()

            self.dirsave = file.getCanonicalPath()
            mes = "Acquired data will be saved in : " + self.dirsave + " directory"
            SHOW_STATUS(message=mes)
            self.SaveDir.setText(mes)
            self.setAlwaysOnTop(True)

            # def TwoDimTemp(e):
            # def TwoDimTemp(e):

    def TwodimPatern(self, e):
        self.setAlwaysOnTop(False)

        self.twodimpath = DATASET_DIALOG(
            "Choose 2D experiment pattern (DO NOT USE FIND OPTION!)")  # PROBLEM WITH FIND BUTTON!!!
        mes = '2D template is: ' + self.twodimpath[3] + '/' + self.twodimpath[0] + '/' + self.twodimpath[1] + '/' + \
              self.twodimpath[2]
        SHOW_STATUS(message=mes)
        # DATASET_DIALOG("Choose 1D experiment pattern", CURDATA())
        self.Patern2D.setText(mes)
        self.setAlwaysOnTop(True)

    def TwodimPatern2(self, e):
        self.setAlwaysOnTop(False)

        self.twodimpath2 = DATASET_DIALOG(
            "Choose 2D experiment pattern (DO NOT USE FIND OPTION!)")  # PROBLEM WITH FIND BUTTON!!!
        mes = '2D template is: ' + self.twodimpath2[3] + '/' + self.twodimpath2[0] + '/' + self.twodimpath2[1] + '/' + \
              self.twodimpath2[2]
        SHOW_STATUS(message=mes)
        # DATASET_DIALOG("Choose 1D experiment pattern", CURDATA())
        self.Patern2D_1.setText(mes)
        self.setAlwaysOnTop(True)

    def TwodimPaternTR(self, e):
        self.setAlwaysOnTop(False)

        self.twodimpathTR = DATASET_DIALOG(
            "Choose 2D experiment pattern (DO NOT USE FIND OPTION!)")  # PROBLEM WITH FIND BUTTON!!!
        mes = '2D template is: ' + self.twodimpathTR[3] + '/' + self.twodimpathTR[0] + '/' + self.twodimpathTR[
            1] + '/' + \
              self.twodimpathTR[2]
        SHOW_STATUS(message=mes)
        # DATASET_DIALOG("Choose 1D experiment pattern", CURDATA())
        self.Patern2D_tr.setText(mes)
        self.setAlwaysOnTop(True)

    def TwodimPatern3(self, e):
        self.setAlwaysOnTop(False)

        self.twodimpath3 = DATASET_DIALOG(
            "Choose 2D experiment pattern (DO NOT USE FIND OPTION!)")  # PROBLEM WITH FIND BUTTON!!!
        mes = '2D template is: ' + self.twodimpath3[3] + '/' + self.twodimpath3[0] + '/' + self.twodimpath3[1] + '/' + \
              self.twodimpath3[2]
        SHOW_STATUS(message=mes)
        # DATASET_DIALOG("Choose 1D experiment pattern", CURDATA())
        self.Patern2D_2.setText(mes)
        self.setAlwaysOnTop(True)

        # self.twodimpath=DATASET_DIALOG("Choose 1D experiment pattern", CURDATA())

    def OnedimPatern(self, e):
        self.setAlwaysOnTop(False)

        self.onedimpath = DATASET_DIALOG("Choose 1D experiment pattern (DO NOT USE FIND OPTION!)")
        mes = '1D template is: ' + self.onedimpath[3] + '/' + self.onedimpath[0] + '/' + self.onedimpath[1] + '/' + \
              self.onedimpath[2]
        SHOW_STATUS(message=mes)
        # DATASET_DIALOG("Choose 1D experiment pattern", CURDATA())
        # self.twodimpath=DATASET_DIALOG("Choose 1D experiment pattern", CURDATA())
        self.Patern1D.setText(mes)
        self.setAlwaysOnTop(True)

    def onStop(self, e):
        self.eventkill.set()
        self.StopBTN.setEnabled(False)
        self.RunBTN.setEnabled(True)
        self.RunBTN.setText("Start Acquisition")

    def onRunt(self, e):
        self.StopBTN.setEnabled(True)
        twoditemp = self.twodimpath
        if self.numofexp.getValue() < 3:
            self.sampfile3 = ''
            self.twodimpath3 = ''
        if self.numofexp.getValue() < 2:
            self.sampfile2 = ''
            self.twodimpath2 = ''
        if self.twodionly.isSelected():
            self.onedimpath = ''
        self.eventkill = threading.Event()
        self.first = threading.Thread(target=self.acquisitionloop,
                                      args=(self.steps.getValue(), self.sampfile, self.twodimpathTR, self.twodimpath,
                                            self.onedimpath,
                                            self.dirsave, self.twodionly.isSelected(), self.sampfile2, self.sampfile3,
                                            self.sampfileTR,
                                            self.twodimpath2, self.twodimpath3, self.numofexp.getValue(),self.sampfileIlumin,
                                            self.eventkill))
        # first.setDaemon(True)
        self.first.start()

    def acquisitionloop(self, steps, sampfile, twoditempTR, twoditemp, oneditemp, SaveDir, TwoDiOnly, sampfile2,
                        sampfile3, sampfileTR,
                        twoditemp2, twoditemp3, numofexp,sampfileIlumin, eventkill):
        self.RunBTN.setEnabled(False)
        self.create_interleave_file_structure(SaveDir, numofexp)  # creates subfolders like Acquired/1D Acquired/2D
        # with open(sampfile) as f:
        #     schedule1 = f.readlines()
        f = open(sampfileIlumin, 'r')
        schedulelight = f.readlines()
        f.close()
        f = open(sampfile, 'r')
        schedule1 = f.readlines()
        f.close()
        f = open(sampfileTR, 'r')
        scheduleTR = f.readlines()
        f.close()
        shutil.copy2(sampfileTR, SaveDir + '/gradients.txt')

        shutil.copy2(sampfile, SaveDir + '/sampling1.sch')
        if int(numofexp) == 3:
            shutil.copy2(sampfile3, SaveDir + '/sampling3.sch')
            # with open(sampfile3) as f:
            #     schedule3 = f.readlines()
            f = open(sampfile3, 'r')
            schedule3 = f.readlines()
            f.close()
        if int(numofexp) == 3 or int(numofexp) == 2:
            shutil.copy2(sampfile2, SaveDir + '/sampling2.sch')
            # with open(sampfile2) as f:
            #     schedule2 = f.readlines()
            f = open(sampfile2, 'r')
            schedule2 = f.readlines()
            f.close()
        W = 0
        itr = 0
        multizg = 1
        i3=0
        for i in xrange(2, 2 * int(steps) + 2, 2):
            if not eventkill.wait(1):
                # txtbtn = "Acq. running. Step  " + str(i / 2) + "/" + str(steps)
                # self.RunBTN.setText(txtbtn)
                for k in range(0, int(numofexp)):
                    # SHOW_STATUS(message=str(schedule[i]))

                    #time.sleep(0.2)
                    txtbtn = "Acq. running. Step  " + str(i / 2) + "/" + str(steps)
                    self.RunBTN.setText(txtbtn)
                    # start 2D
                    if k == 0:
                        schedule = schedule1
                        self.copydataTo2(twoditemp, SaveDir , multizg)
                        # self.openFolderPath(SaveDir + '/' + str(multizg) + '/pdata/' + twoditemp[2])
                        # time.sleep(5)
                        # fname = SaveDir + '/' + str(multizg) + '/nusILlist'
                        # multizg+=1
                    elif k == 1:
                        schedule = schedule2
                        self.copydataTo2(twoditemp2, SaveDir , multizg)                        
                        
                        # self.openFolderPath(SaveDir + '/Acquired/2D_1/' + str(i / 2) + '/pdata/' + twoditemp2[2])
                        # time.sleep(5)
                        # fname = SaveDir + '/Acquired/2D_1/' + str(i / 2) + '/nusILlist'
                    elif k == 2:
                        schedule = schedule3
                        self.copydataTo2(twoditemp3, SaveDir , multizg)                        
                        # self.copydataTo(twoditemp3, SaveDir + '/Acquired', '2D_2', i / 2)
                        # self.openFolderPath(SaveDir + '/Acquired/2D_2/' + str(i / 2) + '/pdata/' + twoditemp3[2])
                        # time.sleep(5)
                        # fname = SaveDir + '/Acquired/2D_2/' + str(i / 2) + '/nusILlist'
                    # self.copydataTo2(twoditemp, SaveDir, multizg)
                    self.openFolderPath(SaveDir + '/' + str(multizg) + '/pdata/' + twoditemp[2])
                    time.sleep(2)
                    fname = SaveDir + '/' + str(multizg) + '/nusILlist'
                    f = open(fname, 'w+')
                    f.write(schedule[W])
                    f.write(schedule[W + 1])  # retest it when the new generator is ready
                    f.close()
                    topspin_path = '/opt/topspin4.3.0'                    
                     
                    f = open(topspin_path + '/exp/stan/nmr/lists/vc/trendnls' + str(multizg) + '.txt', 'w+')
                    f.write(schedule[W])
                    f.write(schedule[W + 1])  # retest it when the new generator is ready
                    # self.RunBTN.setText(str(schedule[i/2]))
                    f.close()

                    self.sendcommand('cnst60 3')
                    self.sendcommand('cnst61 0')
                    time.sleep(0.1)
                                                            
                    self.sendcommand('fntype non-uniform_sampling')
                                        
                    self.sendcommand('NUSpoints 2')
                    self.sendcommand('DS 0')
                    self.putpar('NUSLIST',
                                'trendnls' + str(multizg) + '.txt')  # ON test xcmd gives error so putpar is safer
                    multizg += 1

                    time.sleep(0.7)
                    # self.sendcommand('zg')
                    # time.sleep(10)
                # if k == 0:
                #     self.acqtest(i, '2D',
                #                  SaveDir)  # KEEPS loop with sleep until audita.txt shows that acquisition is running
                # elif k == 1:
                #     self.acqtest(i, '2D_1',
                #                  SaveDir)  # KEEPS loop with sleep until audita.txt shows that acquisition is running
                # elif k == 2:
                #     self.acqtest(i, '2D_2',
                #                  SaveDir)  # KEEPS loop with sleep until
                W += 2
               
                    # self.sendcommand('zg')
                    # time.sleep(10)
                    # self.acqtest(i, '1D', SaveDir)
                # TR DOSY part
                self.copydataTo2(twoditempTR, SaveDir, multizg)
                self.openFolderPath(SaveDir + '/' + str(multizg) + '/pdata/' + twoditempTR[2])
                time.sleep(1)

                self.sendcommand('cnst60 3')
                self.sendcommand('cnst61 0')
                      
                self.sendcommand('GPZ6 ' + str(scheduleTR[itr][:-3]))
                time.sleep(1)
                itr += 1
                multizg += 1
                # self.sendcommand('zg')
                # time.sleep(10)
                if not TwoDiOnly:
                    self.copydataTo2(oneditemp, SaveDir, multizg)
                    self.openFolderPath(SaveDir + '/' + str(multizg) + '/pdata/' + oneditemp[2])
                    multizg += 1
                    time.sleep(1)
                    Lightpower=int(schedulelight[i3])
                    i3=i3+1
                    self.sendcommand('cnst60 3')
                    self.sendcommand('cnst61 ' + str(Lightpower))
                # self.acqtest(i, 'DOSY', SaveDir)

                # fname = SaveDir + '/Acquired/2D/' + str(i / 2) + '/nusILlist'

        self.RunBTN.setText("Acquisition Complete")
        self.RunBTN.setEnabled(True)

    def acqtest(self, i, Mode, SaveDir):
        AcqActive = True
        while AcqActive:
            if 'acquisition in progress' in open(SaveDir + '/Acquired/' + Mode + '/' + str(
                    i / 2) + '/audita.txt').read():
                SHOW_STATUS('Acquisition in progress')
                time.sleep(10)
            else:
                AcqActive = False
                SHOW_STATUS('Acquisition step finished. Next step')

    def openFolder(self, folderM):

        com = 'RE(["'
        for l in range(0, 3):
            com += folderM[l] + '","'
        com += folderM[l + 1] + '"],"y")'
        SHOW_STATUS(message=com)
        EXEC_PYSCRIPT(com)

    def openFolderPath(self, folderM):
        com = 'RE_PATH("' + folderM + '","y")'
        EXEC_PYSCRIPT(com)

    def savePath(self, folder):
        com = 'WR_PATH("' + folder + '","y")'
        EXEC_PYSCRIPT(com)

    def sendcommand(self, command):
        com = 'XCMD("' + command + '",1)'
        EXEC_PYSCRIPT(com)
        time.sleep(0.1)        

    def putpar(self, command, path):
        com = 'PUTPAR("' + command + '",' + '"' + path + '")'
        EXEC_PYSCRIPT(com)

    def copydataTo(self, Source, Destination, Mode, counter):  # Mode 2D vs 1D counter is from loop
        Source = Source[3] + '/' + Source[0] + '/' + Source[1] + '/'
        # SHOW_STATUS(message=Source)
        # self.openFolder(self, Source)
        Destination += '/' + Mode + '/' + str(counter)
        # SHOW_STATUS(message=Destination)
        # # time.sleep(5)
        shutil.copytree(Source, Destination)

        # self.savePath(Destination)
        # # time.sleep(5)
        if Mode == '1D':
            try:
                os.remove(Destination + '/fid')
            except:
                pass
        elif Mode == '2D':
            try:
                os.remove(Destination + '/ser')
            except:
                pass
        SHOW_STATUS(message='Acq structure created in: ' + Destination)

    def copydataTo2(self, Source, Destination, counter):  # Mode 2D vs 1D counter is from loop
        Source = Source[3] + '/' + Source[0] + '/' + Source[1] + '/'
        # SHOW_STATUS(message=Source)
        # self.openFolder(self, Source)
        Destination += '/' + str(counter)
        # SHOW_STATUS(message=Destination)
        # # time.sleep(5)
        shutil.copytree(Source, Destination)

        # self.savePath(Destination)
        # # time.sleep(5)

        SHOW_STATUS(message='Acq structure created in: ' + Destination)

    def create_interleave_file_structure(self, Directory, numofexp):
        # Directory=check_if_dir(Directory)
        # Creates the folder structure for saving the data in Directory
        if not (os.path.isdir(Directory)):
            os.makedirs(Directory)


TopTReND()
