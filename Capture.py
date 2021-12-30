import numpy as np
import cv2

class Capture:
    Is_Color = 0
    Is_videoStop = False
    VideoFile = "X:\StudyCode\python\Clouds - 35573.mp4"
    VideoCount = 0
    vid = None
    texture_data = None
    frame_rate = 0
    def __init__(self):
        self.vid = cv2.VideoCapture(self.VideoFile)
        ret,img = self.vid.read()
        self.frame_rate = int(self.vid.get(cv2.CAP_PROP_FPS))
        img = cv2.resize(img , (480, 270))

        data = np.flip(img, 2) 
        data = data.ravel()
        data = np.asfarray(data, dtype='f')
        self.texture_data = np.true_divide(data, 255.0)

    def IsStartStop(self):
        if self.Is_videoStop == False:
            self.Is_videoStop = True
        else:
            self.Is_videoStop = False
    
    def ChgGrayImage(self,img):
        img_gry = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        return img_gry

    def ChgBinaryImage(self,img):
        threshold = 100
        ret, img_th = cv2.threshold(self.ChgGrayImage(img), threshold, 255, cv2.THRESH_BINARY)
        return img_th

    def ChgEdgeImage(self,img):
        img_canny = cv2.Canny(self.ChgGrayImage(img), 100, 100)
        return img_canny

    def DrawContours(self,img):
        contours,hierarchy = cv2.findContours(self.ChgBinaryImage(img), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
        img = cv2.drawContours ( img , contours , -1 , ( 0 , 0 , 255 ) , 3 )
        img = cv2.resize(img , (480, 270))
        return img

    def ChgFormatForDearPy(self,img):
        img = cv2.merge((img, img, img))
        img = cv2.resize(img , (480, 270))
        return img        

    def ChgMatImage(self, img):
        if self.Is_Color == 1:
            img_gry = self.ChgFormatForDearPy(self.ChgGrayImage(img))
            data = np.flip(img_gry, 2)
        elif self.Is_Color == 2:
            img_th = self.ChgFormatForDearPy(self.ChgBinaryImage(img))
            data = np.flip(img_th, 2)
        elif self.Is_Color == 3:
            img_canny = self.ChgFormatForDearPy(self.ChgEdgeImage(img))
            data = np.flip(img_canny, 2)
        elif self.Is_Color == 4:
            img = self.DrawContours(img)
            data = np.flip(img, 2)
        else:
            img = img
            img = cv2.resize(img , (480, 270))
            data = np.flip(img, 2)
        data = data.ravel()
        data = np.asfarray(data, dtype='f')
        self.texture_data = np.true_divide(data, 255.0)
        
        return self.texture_data
    
    def InitTextureData(self):
        return self.texture_data
    
    def GetVideoPath(self):
        return self.VideoFile