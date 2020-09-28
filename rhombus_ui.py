import cv2
import numpy as np
import imutils
import time

cap=cv2.VideoCapture(1)
while True:
    #time.sleep(5)
    ret, img=cap.read()
    cv2.imshow('img',img)
    k=cv2.waitKey(30)& 0xff
    if k%256 ==115:
        
    ##img=cv2.imread('img4.png')
    ##img.set(cv2.CAP_PROP_FRAME_WIDTH,width)
    ##img.set(cv2.CAP_PROP_FRAME_HEIGHT,height)
        img=cv2.GaussianBlur(img,(3,3),0)
##        img=cv2.medianBlur(img,3)
        img=cv2.bilateralFilter(img,10,75,75)
##        img=cv2.fastNlMeansDenoisingColored(img,None,10,10,7,21)
        gray= cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
        #cv2.imshow('gray',gray)
        thresh=cv2.threshold(gray,125,255,cv2.THRESH_BINARY_INV)[1]
        kernel=np.ones((1,1),np.uint8)
        thresh=cv2.erode(thresh,kernel,iterations=2)
        thresh=cv2.dilate(thresh,kernel,iterations=2)
        cv2.imshow('thresh',thresh)
        img2, cnt,hierarchy=cv2.findContours(thresh.copy(),cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        cnt=sorted(cnt, key=cv2.contourArea,reverse=True)[:10]
        screenCnt=None
        c=cnt[0]
        ##extLeft=None
        ##extRight=None
        ##extTop=None
        ##extBottom=None
        extLeft=None
        extRight=None
        extTop=None
        extBottom=None
        ##for c in cnt:
        peri=cv2.arcLength(c,True)
        approx=cv2.approxPolyDP(c,0.02*peri,True)


        if len(approx)==4:
            screenCnt=approx
        ##    extLeft =tuple(c[c[:,:,0].argmin()][0])
        ##    extRight =tuple(c[c[:,:,0].argmax()][0])
        ##    extTop =tuple(c[c[:,:,1].argmax()][0])
        ##    extBottom =tuple(c[c[:,:,1].argmin()][0])
        ##    print (extLeft)
        ##    print (extRight)
        ##    print (extTop)
        ##    print (extBottom)
        ##        extLeft=extL
        ##        extRight=extR
        ##        extTop=extT
        ##        extBottom=extB
        ##    extLeft =screenCnt[0]
        ##    extRight =screenCnt[1]
        ##    extTop =screenCnt[2]
        ##    extBottom =screenCnt[3]
        ##    cv2.circle(img,extLeft,6, (255,0,0), -1)
        ##    cv2.circle(img,extRight,6, (255,0,0), -1)
        ##    cv2.circle(img,extTop,6, (255,0,0), -1)
        ##    cv2.circle(img,extBottom,6, (255,0,0), -1)     
            print (screenCnt)
        ##    print (screenCnt[2][0])
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
            print ("diagonal1 length =",dist_dia1)
            print ("diagonal2 length =",dist_dia2)
            print ("Mean diagonal=",(dist_dia1+dist_dia2)/2)

        ##    print (screenCnt[2])
        ##    print (screenCnt[3])
        ##    print (vertice1)
        ##    print (vertice2)
        ##    print (vertice3)
        ##    print (vertice4)
            
        ##font=cv2.FONT_HERSHEY_SIMPLEX
        ##cv2.putText(img,"IMAGE: TempImage_11",(100,40),font,0.8,(0,0,255),2,cv2.LINE_AA)       
        ##cv2.drawContours(img, screenCnt, -1, (0,255,0), 2)
        conto=cv2.imshow('rhomb',img)
    
    if k==27:
        break
cap.release()
cv2.destroyAllWindows()
