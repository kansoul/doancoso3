import cv2
import numpy as np
from PIL import Image
import os
import sqlite3

#tranning hinh anh nhan dien vs Thu vien nhan dien khuon mat
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")
recognizer = cv2.face.LBPHFaceRecognizer_create()

#read file tranning
recognizer.read('recognizer/trainningData.yml')

# get profile by id from datatbase
def getProfile(id, lop):
    db = "database/"+str(lop)+".db"
    conn = sqlite3.connect(db)
    query = "SELECT * FROM sinhvien WHERE ID="+str(id)
    cursor = conn.execute(query)

    profile = None
    for row in cursor:
        profile = row
    conn.close()
    return profile

def check(id, ngay, lop):
    db = "database/"+str(lop)+".db"
    conn = sqlite3.connect(db)

    #query="UPDATE sinhvien SET DD='1' WHERE ID="+str(id)
    #cursor = conn.execute(query)    
    #conn.commit()
    #print(str(id), str(ngay))
    sql = "UPDATE '"+str(ngay)+"' SET DD = 1 WHERE ID ="+str(id)
    #print(sql)
    cur = conn.cursor()
    cur.execute(sql)
    conn.commit()

def taobangngay(ngay, lop):
    db = "database/"+str(lop)+".db"
    conn = sqlite3.connect(db)
    print(str(ngay))
    sql = "CREATE TABLE '"+str(ngay)+"' (ID INTEGER NOT NULL, TEN TEXT NOT NULL, DD INTEGER, PRIMARY KEY(ID) )"
    sql2 = "INSERT INTO '"+str(ngay)+"' SELECT * FROM sinhvien"
    cur = conn.cursor()
    cur.execute(sql)
    cur.execute(sql2)
    conn.commit()
lop = input("Nhap lop: ")
ngay = input("Nhap ngay(dd-mm-yyyy): ")
taobangngay(ngay, lop)

#use webcam


#set text style
fontface = cv2.FONT_HERSHEY_SIMPLEX

cap = cv2.VideoCapture(0)
while(True):
    ret, frame = cap.read()
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray,1.3,5)

    for (x,y,w,h) in faces:
        #rectangle: hinh chu nhat
        cv2.rectangle(frame, (x,y),( x+w, y+h ), (0,255,0),2)
        roi_gray = gray[y:y+h, x:x+w] # cut anh xam de so sanh voi dataTrain
        #roi_color = frame[y:y+h, x:x+w]

        nbr_predicted,confidence = recognizer.predict(roi_gray) # du doan anh voi data exists
        if confidence < 40:
            profile= getProfile(nbr_predicted, lop)
            if(profile!= None):
                cv2.putText(frame, ""+str(profile[1]), (x + 10, y + h + 30), fontface, 1, (0,255,0), 2)
                check(str(profile[0]), str(ngay), lop)
           
        else:
            cv2.putText(frame, "Unknown", (x + 10, y + h + 30), fontface, 1, (0, 0, 255), 2);

    cv2.imshow('photograph', frame)
    if(cv2.waitKey(1) == ord('q')):
        break

cap.release()
cv2.destroyAllWindows()




        

    


    




