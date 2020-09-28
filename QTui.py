
import sys
import numpy as np
import imutils
import time
import cv2
from PyQt5 import QtCore
from PyQt5 import QtWidgets
from PyQt5 import QtGui
from PyQt5.QtCore import QTimer
from PyQt5.QtCore import pyqtSlot
from PyQt5.QtCore import pyqtSignal
from PyQt5.QtCore import *
from PyQt5.QtGui import QImage, QPixmap, QFont
from PyQt5.QtGui import *
from PyQt5.QtWidgets import QDialog, QApplication, QLineEdit
from PyQt5.uic import loadUi


start_detect=None
class CameraAlert(QDialog):
    def __init__(self):
        super(CameraAlert,self).__init__()
        loadUi('CameraAlert.ui',self)

class lineeditfunc(QLineEdit):
    clicked=pyqtSignal()
    def __init__(self,widget):
        super(lineeditfunc,self).__init__(widget)
    def mousePressEvent(self,QMouseEvent):
        self.clicked.emit()
class Vickers(QDialog):


    def __init__(self):
        super(Vickers,self).__init__()
        loadUi('VickersMainWindow.ui',self)
##        self.cap=cv2.VideoCapture(1)
        self.capture=cv2.VideoCapture(0)

        
        self.start_webcam()
##        mousePressed=pyqtProperty(QMouseEvent)
        self.MainText1=lineeditfunc(self)
        self.MainText2=lineeditfunc(self)
        self.MainText1.setFixedWidth(100)
        self.MainText1.move(125,125)
        self.MainText2.setFixedWidth(100)
        self.MainText2.move(350,125)
        self.MainText1.clicked.connect(self.numpadwindow1)
        self.MainText2.clicked.connect(self.numpadwindow2)
        
        self.CloseButton.clicked.connect(self.close_allwindow)
        self.ExecuteButton.clicked.connect(self.ExecuteCommand)
##        except:
##            self.Alertbox0=CameraAlert()
##            self.Alertbox0.show()
            
    def start_webcam(self):            
        self.VideoSignal=QtCore.pyqtSignal(QtGui.QImage)
        self.capture.set(cv2.CAP_PROP_FRAME_HEIGHT, 290)
        self.capture.set(cv2.CAP_PROP_FRAME_WIDTH, 210)
        self.timer=QTimer(self)
        
        self.timer.timeout.connect(self.update_frame)
        self.timer.start(5)
    def update_frame(self):
        
        ret,self.image=self.capture.read()
##        self.image=cv2.flip(self.image,1)
        
        self.displayImage(self.image)
        
##        self.StartButton.clicked.connect(self.start_webcam)

    def displayImage(self,img):
               
        qformat=QImage.Format_Indexed8
        
        if len(img.shape)==3:
            if (img.shape[2])==4:
                qformat=QImage.Format_RGBA8888
            else:
                qformat=QImage.Format_RGB888
##        self.outImage=QImage(self.image,self.image.shape[1],self.image.shape[0],self.image.strides[0],QtGui.QImage.Format_RGB888)
        self.outImage=QImage(img,img.shape[1],img.shape[0],img.strides[0],qformat)
        self.outImage=self.outImage.rgbSwapped()
##        self.VideoSignal.emit(outImage)
        
        self.maskLabel.setStyleSheet("border: 3px solid yellow")
        
        self.imgLabel.setPixmap(QPixmap.fromImage(self.outImage))
        self.imgLabel.setScaledContents(True)
##        selRect=self.imgLabel.getSelectionPos()
##        widgsize=self.imgLabel.contentsRect()
##        origwidgscale=widgsize.width() / self.image.width()
##
##    ##        x1=selRect.topLeft().x() / origwidgscale
##        y1=selRect.topLeft().y() / origwidgscale
##        x2=selRect.bottomRight().x() / widgsize.bottomRight().x() * self.image.width()
##        y2=selRect.bottomRight().y() / widgsize.bottomRight().y() * self.image.width()
##        wid2rect=QtCore.QRect(x1, y1, x2, y2)
##        self.image=self.image.copy(wid2rect)
##        cv2.imshow('img',self.image)
##        pm=QPixmap(ui.self.maskLabel.pixmap())
##        image=QImage(pm.toImage())
##        
##        currentimg=QPixmap.grabWidget()
##        self.maskLabel.setScaledContents(True)    
##        self.image=self.maskLabel.pixmap()
##        print (self.image) 
##        cv2.imshow("currentimggg",currentimg)    
##        self.start_detect.DisplayCombo.setText(combovalue)
##        c1=Numpad1()
##        c2=c1.okay1()
        
##        number_exp=" "
        

##        self.equation=StringVar()
##        self.equation.set('enter your expression')
    def ExecuteCommand(self):
        try:
            #time.sleep(5)
##            p=QPixmap.grabWindow(self.maskLabel.winId())
##            cv2.imshow('pixmap',p)
            diamond=self.image[90:210,110:250]
            img=diamond
            cv2.imshow('diamond',diamond)
            self.combo1value=str(mainwindow.comboBox1.currentText())
    ##        ret, img=self.capture.read()
            
    ##        cv2.imshow('img',img)
            #k=cv2.waitKey(30)& 0xff
    ##            if k%256 ==115:
                
            ##img=cv2.imread('img4.png'
            ##img.set(cv2.CAP_PROP_FRAME_WIDTH,width)
            ##img.set(cv2.CAP_PROP_FRAME_HEIGHT,height)
            img=cv2.GaussianBlur(img,(3,3),20)
            img=cv2.medianBlur(img,3)
            img=cv2.bilateralFilter(img,5,75,75)
    ##        img=cv2.fastNlMeansDenoisingColored(img,None,10,10,7,21)
            gray= cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
            #cv2.imshow('gray',gray)
            thresh=cv2.threshold(gray,120,255,cv2.THRESH_BINARY_INV)[1]
            kernel=np.ones((1,1),np.uint8)
            thresh=cv2.erode(thresh,kernel,iterations=2)
            thresh=cv2.dilate(thresh,kernel,iterations=2)
            cv2.imshow('thresh',thresh)
            img2, cnt,hierarchy=cv2.findContours(thresh.copy(),cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
            print("cnt=",cnt)
            cv2.drawContours(img, cnt, -1, (0,255,0), 3)
            cv2.imshow('cnt',img)
            cnt=sorted(cnt, key=cv2.contourArea,reverse=True)[:10]
            screenCnt=None
            c=cnt[0]
            ##for c in cnt:
            peri=cv2.arcLength(c,True)
            print ("peri=",peri)
            approx=cv2.approxPolyDP(c,0.02*peri,True)
            print("approx=",approx)

            if len(approx)==4:
                screenCnt=approx
            
                print (screenCnt)
            
                vertice1=(screenCnt[0][0][0],screenCnt[0][0][1])
                vertice2=(screenCnt[1][0][0],screenCnt[1][0][1])
                vertice3=(screenCnt[2][0][0],screenCnt[2][0][1])
                vertice4=(screenCnt[3][0][0],screenCnt[3][0][1])
                cv2.circle(img,vertice1,2, (255,0,0), -1)
                cv2.circle(img,vertice2,2, (255,0,0), -1)
                cv2.circle(img,vertice3,2, (255,0,0), -1)
                cv2.circle(img,vertice4,2, (255,0,0), -1)     
                dist_dia1=np.sqrt((vertice3[0]-vertice1[0])**2+(vertice3[1]-vertice1[1])**2)
                dist_dia2=np.sqrt((vertice4[0]-vertice2[0])**2+(vertice4[1]-vertice2[1])**2)
                MMdist_dia1=dist_dia1*0.0118
                MMdist_dia2=dist_dia2*0.0118
                print ("diagonal1 length =",MMdist_dia1)
                print ("diagonal2 length =",MMdist_dia2)
                print ("Mean diagonal=",(MMdist_dia1+MMdist_dia2)/2)
                self.Mean_diagonal=round(((MMdist_dia1+MMdist_dia2)/2),2)
                print (self.combo1value)
                self.HV_value=round((1.854*int(self.combo1value))/((self.Mean_diagonal)**2),2)
                print (self.Mean_diagonal)
                print (self.HV_value)
                self.meandiagDist.setText(str(self.Mean_diagonal))
                self.HVLabel.setText(str(self.HV_value))
                minvalVar=mainwindow.MainText1.text()
                print (minvalVar)
                maxvalVar=mainwindow.MainText2.text()
                print (maxvalVar)
                
                if ((int(self.HV_value)<=int(minvalVar)) or (int(self.HV_value)>=int(maxvalVar))):
                    self.resultImage.setText("Fail")
                    PF_result=self.resultImage.text()
                    self.resultImage.setStyleSheet('color: red')
                elif ((int(self.HV_value)>int(minvalVar)) and (int(self.HV_value)<int(maxvalVar))):
                    self.resultImage.setText("Pass")
                    PF_result=self.resultImage.text()
                    self.resultImage.setStyleSheet('color: green')
                with open('Result.txt','a+') as f:
                    print('Mean Distance=',self.Mean_diagonal,file=f)
                    print('HV=',self.HV_value,file=f)
                    print('Result=',PF_result,file=f)
##                for i in range(1):
##                    f.write("Mean Distance=%d\r\n"% (self.Mean_diagonal))
##                    i+1
                
                

        except:
##            print (mainwindow.MainText1.text())
##            if ((mainwindow.MainText1.text()==None) or (mainwindow.MainText2.text()==None)):
                
                
            if (self.combo1value=="Select"):
                self.Alertbox2=AlertLD()
                self.Alertbox2.show()
            else: 
                self.Alertbox1=Alert()
                self.Alertbox1.show()
    ##        conto=cv2.imshow('rhomb',img)
    
    def numpadwindow1(self):
        self.firstNumpad=Numpad1()
        self.firstNumpad.show()
        
        
    def numpadwindow2(self):
        self.secondNumpad=Numpad2()
        self.secondNumpad.show()    

    def start_spotdetect(self):
        self.start_detect=Spotdetection()        
        self.start_detect.show()
        
##    def showtex(self,number_exp):
##        self.MainText1.clear()
##        self.MainText1.setText(str(number_exp))
##        print (str(number_exp))
##        self.MainText2.setText(number_exp)    
    
    def close_allwindow(self):
        sys.exit(0)
        
class Alert(QDialog):
    def __init__(self):
        super(Alert,self).__init__()
        loadUi('AlertBox.ui',self)
        self.OkButton.clicked.connect(self.okay)
    def okay(self):
        self.close()
class AlertLD(QDialog):
    def __init__(self):
        super(AlertLD,self).__init__()
        loadUi('AlertLDBox.ui',self)
        self.OkButton.clicked.connect(self.okay)
    def okay(self):
        self.close()
        
class Numpad1(QDialog):    
    
    def __init__(self):
        super(Numpad1,self).__init__()
        loadUi('Numpad1.ui',self)
    
        
        
##        self.number_exp=StringVar()
        
##        self.numpad1=loadUi('Numpad1.ui')
##        self.numpad1.show()
        
##        self.equation=StringVar()
##        self.equation.set('enter your expression')
##        layout=QHBoxLayout()
##        lineEdit=QLineEdit()
##        
##        self.lineEdit.setText("enter your expression")
##        layout.addWidget(lineEdit)
        self.No1.clicked.connect(lambda:self.press(1))
        self.No2.clicked.connect(lambda:self.press(2))
        self.No3.clicked.connect(lambda:self.press(3))
        self.No4.clicked.connect(lambda:self.press(4))
        self.No5.clicked.connect(lambda:self.press(5))
        self.No6.clicked.connect(lambda:self.press(6))
        self.No7.clicked.connect(lambda:self.press(7))
        self.No8.clicked.connect(lambda:self.press(8))
        self.No9.clicked.connect(lambda:self.press(9))
        self.No0.clicked.connect(lambda:self.press(0))
        self.OkayButton.clicked.connect(self.okay1)
        self.ClrButton.clicked.connect(self.clear)
##        self.winnum1=Vickers()

    def press(self,num):
##        self.number_exp=StringVar()
##        print (num)       
        self.numbertext=str(num)
##        self.equation.set(self.number_exp)
        self.lineEdit.setText(self.lineEdit.text()+self.numbertext)
    def clear(self):
        
        self.lineEdit.setText(" ")
    def okay1(self):
        
        number_exp1=self.lineEdit.text()
        mainwindow.MainText1.setText(number_exp1)
        self.clear()
        self.close()
         
        
##        destroy()
class Numpad2(QDialog):
        
    def __init__(self):
        super(Numpad2,self).__init__()
        loadUi('Numpad2.ui',self)
        
##        self.numpad2=loadUi('Numpad2.ui')
        
##        self.equation=StringVar()
##        self.equation.set('enter your expression')
##        self.lineEdit.setText(self.equation)
        self.No1.clicked.connect(lambda:self.press(1))
        self.No2.clicked.connect(lambda:self.press(2))
        self.No3.clicked.connect(lambda:self.press(3))
        self.No4.clicked.connect(lambda:self.press(4))
        self.No5.clicked.connect(lambda:self.press(5))
        self.No6.clicked.connect(lambda:self.press(6))
        self.No7.clicked.connect(lambda:self.press(7))
        self.No8.clicked.connect(lambda:self.press(8))
        self.No9.clicked.connect(lambda:self.press(9))
        self.No0.clicked.connect(lambda:self.press(0))
        self.OkayButton.clicked.connect(self.okay2)
        self.ClrButton.clicked.connect(self.clear)

    def press(self,num):
        self.numbertext=str(num)

        self.lineEdit.setText(self.lineEdit.text()+self.numbertext)    
    
        
    def clear(self):
        self.lineEdit.setText(" ")        

    def okay2(self):
        number_exp2=self.lineEdit.text()
##        self.MainText2.setText(self.lineEdit.text())
        mainwindow.MainText2.setText(number_exp2)
        self.close()        
        self.clear()
##        self.secondNumpad.destroy()
        

##    def okay2(self):
##        
##
##        self.max_value=self.number_exp
##        self.lineEdit2.set(self.number_exp)
##        
##        self.clear()
##        self.numpad2.destroy()

    
##class Spotdetection(QDialog):
####    global capture
##    
##    def __init__(self):
##        super(Spotdetection,self).__init__()
##        loadUi('SpotDetection.ui',self)
##        self.BackButton.clicked.connect(self.back)
####        self.playing=True
####        self.capture=cv2.VideoCapture(0)
####            self.capture.set(cv2.CAP_PROP_FRAME_HEIGHT, 290)
####            self.capture.set(cv2.CAP_PROP_FRAME_WIDTH, 210)
####            self.timer=QTimer(self)
####            
######            self.timer.timeout.connect(self.update_frame)
####            self.timer.start(5)
####            
##    ##        self.start_webcam()
##    ##        self.combo1value=str(mainwindow.comboBox1.currentText())       
##    ####        self.combo2value=str(mainwindow.comboBox2.currentText())
##    ##        combovalue=str(self.combo1value)
##    ##        self.maskLabel.setStyleSheet("border: 5px red")
##        
##    ##        self.DisplayCombo.setText(str(combovalue))
##    ##        self.ExecuteButton.clicked.connect(self.ExecuteCommand)
##    ##        self.CameraButton.setDefault(True)
##    ##        self.CameraButton.setCheckable(False)
##    ##        self.CameraButton.clicked.emit(False)
##    ##        self.CameraButton.clicked.connect(self.start_webcam)
##            
##            
##            
##
##            
##            
##            
##    def back(self):
##        
##        
##        self.close()
##
##     
####        self.close()
####        mainwindow.show()
##        
####        self.VideoSignal.emit(self.capture)
####        self.timer.start(5)
    
    
        


               
                   
mainwindow=None
if __name__=='__main__':

    app=QApplication(sys.argv)
    mainwindow=Vickers()
    mainwindow.setWindowTitle('Vickers ')



    #window.setGeometry(100,100,400,200)
    mainwindow.show()
    sys.exit(app.exec_())
##    except:
##        Alertbox5=Alert()
##        Alertbox5.show()
        
