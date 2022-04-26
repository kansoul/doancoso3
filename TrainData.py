import cv2
import numpy as np
import os
import glob
from os import path
from PIL import Image

# tranning hinh anh nhan dien
recognizer = cv2.face.LBPHFaceRecognizer_create()
path= 'dataSet'
def getImageWithID(path):
    #imagePaths=[os.path.join(path, f) for f in os.listdir(path)]
    imagePaths = []
    for root, dirs, files in os.walk(path):
        #imagePaths.append(files)
        for f in files:
            imagePaths.append(os.path.join(root, f))
    #print(imagePaths) #: list url
    faces=[]
    IDs=[]

    for imagePath in imagePaths:
        #loading the image and converting it to gray scale
        faceImg = Image.open(imagePath).convert('L')
        #converting the PIL image into numpy array
        faceNp = np.array(faceImg,'uint8')
        #print(faceNp) #: list matrix pixel

        #split to get ID of the image
        ID=int(imagePath.split('\\')[2].split('-')[0])
        #print(os.path.split(imagePath)) => [dataSet, url]
        
        #add to array
        faces.append(faceNp)
        IDs.append(ID)
    
        cv2.imshow("traning",faceNp)
        cv2.waitKey(10)
        
    return IDs, faces
        
Ids, faces = getImageWithID(path)
recognizer.train(faces ,np.array(Ids))
if not os.path.exists('recognizer'):
    os.makedirs('recognizer')
recognizer.save('recognizer/trainningData.yml')
cv2.destroyAllWindows()

