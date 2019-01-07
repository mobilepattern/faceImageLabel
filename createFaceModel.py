'''
Build the facial recognition model.

Based on:
https://linuxhint.com/opencv-face-recognition/
'''

import re

import pickle

import cv2, os
import numpy as np
from PIL import Image

class modelBuilder:

    def __init__(self):
        self.recognizer = cv2.face.LBPHFaceRecognizer_create()
        self.detector = cv2.CascadeClassifier("haarcascade_frontalface_default.xml");
        self.idsToNames = []


    def lookupID(self, name):
        try:
            i = self.idsToNames.index(name) + 1
        except ValueError:
            self.idsToNames.append(name)
            return len(self.idsToNames)
        return i


    def readIds(self, filename):
        with open(filename, 'rb') as f:
            self.idsToNames = pickle.load(f)


    def writeIds(self, filename):
        with open(filename, 'wb') as f:
            pickle.dump(self.idsToNames, f)


    def getIdFromFileName(self, filename):
        trainingFilePattern = re.compile(r'User.([a-zA-Z_]+).[0-9]+.jpg')
        patt = trainingFilePattern.match(filename)
        if (patt is not None and patt.group(1)):
            name = patt.group(1)
            return self.lookupID(name)
        return -1


    def getImagesAndLabels(self, path):
        imagePaths = [os.path.join(path,f) for f in os.listdir(path) if f.endswith('jpg')] 
        faceSamples=[]
        ids = []
        for imagePath in imagePaths:
            PIL_img = Image.open(imagePath).convert('L')
            img_numpy = np.array(PIL_img,'uint8')
            id = self.getIdFromFileName(imagePath)
            faces = self.detector.detectMultiScale(img_numpy)
            for (x,y,w,h) in faces:
                faceSamples.append(img_numpy[y:y+h,x:x+w])
                ids.append(id)
                return faceSamples,ids


    def buildAndSaveModel(self, trainingDir):
        faces,ids = mb.getImagesAndLabels(trainingDir)
        self.recognizer.train(faces, np.array(ids))
        self.recognizer.save(os.path.join(trainingDir, 'trainer.yml'))     
        self.writeIds(os.path.join(trainingDir, 'names'))  

mb = modelBuilder()

trainingDir = '.training'

mb.buildAndSaveModel(trainingDir)

