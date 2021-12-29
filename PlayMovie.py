import dearpygui.dearpygui as dpg
import numpy as np
import cv2
import time

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
        #img_gry = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        ret, img_th = cv2.threshold(self.ChgGrayImage(img), threshold, 255, cv2.THRESH_BINARY)
        return img_th

    def ChgEdgeImage(self,img):
        img_canny = cv2.Canny(self.ChgGrayImage(img), 100, 100)
        return img_canny

    def ChgFormatForDearPy(self,img):
        img = cv2.merge((img, img, img))
        img = cv2.resize(img , (480, 270))
        return img        

    def ChgMatImage(self, img):
        if m_Capture.Is_Color == 1:
            img_gry = self.ChgFormatForDearPy(self.ChgGrayImage(img))
            #img_gry = cv2.resize(self.ChgGrayImage(img) , (480, 270))
            data = np.flip(img_gry, 2)
        elif m_Capture.Is_Color == 2:
            img_th = self.ChgFormatForDearPy(self.ChgBinaryImage(img))
            #img_th = cv2.resize(self.ChgBinaryImage(img) , (480, 270))
            data = np.flip(img_th, 2)
        elif m_Capture.Is_Color == 3:
            img_canny = self.ChgFormatForDearPy(self.ChgEdgeImage(img))
            '''
            img_gry = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            img_canny = cv2.Canny(img_gry, 100, 100)
            img_canny = cv2.merge((img_canny, img_canny, img_canny))
            img_canny = cv2.resize(img_canny , (480, 270))
            '''
            data = np.flip(img_canny, 2)
        elif m_Capture.Is_Color == 4:
            img_gry = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            ret, img_th = cv2.threshold(img_gry, threshold, 255, cv2.THRESH_BINARY)
            contours,hierarchy = cv2.findContours(img_th, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
            img = cv2.drawContours ( img , contours , -1 , ( 0 , 0 , 255 ) , 3 )
            img = cv2.resize(img , (480, 270))
            data = np.flip(img, 2)
        else:
            img = img
            img = cv2.resize(img , (480, 270))
            data = np.flip(img, 2)
        data = data.ravel()
        data = np.asfarray(data, dtype='f')
        m_Capture.texture_data = np.true_divide(data, 255.0)
            
        dpg.set_value("texture_tag", m_Capture.texture_data)

m_Capture = Capture()

def callback(sender, app_data):
    print("Sender: ", sender)
    print("App Data: ", app_data)
    print(app_data["file_path_name"])
    m_Capture.Is_videoStop = False
    m_Capture.VideoFile = app_data["file_path_name"]
    m_Capture.vid.release()
    m_Capture.vid = cv2.VideoCapture(m_Capture.VideoFile)
    time.sleep(0.3)
    m_Capture.Is_videoStop = True
    dpg.set_value("Main Title", app_data["file_path_name"])

def selectMovieFlie():
    dpg.add_button(label="Directory Selector", callback=lambda: dpg.show_item("file_dialog_id"))

def MakeSubWindow():
    with dpg.menu(label="select movie type"):

        def _selection(sender, app_data, user_data):
            for item in user_data:
                if item == sender:
                    m_Capture.Is_Color = int(item) - 27
                    print(m_Capture.Is_Color)
                    
        items = (
            dpg.add_selectable(label="Color"),
            dpg.add_selectable(label="Gray"),
            dpg.add_selectable(label="Binary"),
            dpg.add_selectable(label="Edge"),
            dpg.add_selectable(label="Contour extraction"),
            )

        for item in items:
            dpg.configure_item(item, callback=_selection, user_data=items)

if __name__=='__main__':

    dpg.create_context()
    dpg.create_viewport(max_width=800, max_height=800)
    dpg.setup_dearpygui()

    with dpg.texture_registry(show=False):
        dpg.add_raw_texture(480, 270, m_Capture.texture_data, tag="texture_tag", format=dpg.mvFormat_Float_rgb, use_internal_label=False)

    with dpg.window(label="Main window",pos=[100,100]):
        dpg.add_text(tag="Main Title",default_value="Hello, world")
        selectMovieFlie()
        MakeSubWindow()

        dpg.add_image("texture_tag")
        dpg.add_progress_bar(tag="slider",pos=[10,320])
        dpg.add_text(tag="Time",default_value="0",pos=[350,320])
        dpg.add_button(label="Save", callback=m_Capture.IsStartStop, pos=[10,350])
        
    with dpg.file_dialog(directory_selector=False, show=False, callback=callback, tag="file_dialog_id"):
        dpg.add_file_extension(".mp4")
        dpg.add_file_extension("", color=(150, 255, 150, 255))

    dpg.show_metrics()
    dpg.show_viewport()

    while dpg.is_dearpygui_running():
        if m_Capture.Is_videoStop == True:
            ret, img = m_Capture.vid.read()
            Timer = 0
            timeString = "0/0"
            if m_Capture.vid.get(cv2.CAP_PROP_FRAME_COUNT) == 0:
                m_Capture.VideoCount = 0
            else:
                m_Capture.VideoCount = (1 / m_Capture.vid.get(cv2.CAP_PROP_FRAME_COUNT)) + m_Capture.VideoCount
                Timer = m_Capture.vid.get(cv2.CAP_PROP_POS_FRAMES) / m_Capture.vid.get(cv2.CAP_PROP_FPS)
            if m_Capture.vid.get(cv2.CAP_PROP_FPS) == 0:
                timeString = "0/0"
            else:    
                timeString = str(round(Timer)) + "/" + str(round(m_Capture.vid.get(cv2.CAP_PROP_FRAME_COUNT) / m_Capture.vid.get(cv2.CAP_PROP_FPS)))
            
            dpg.set_value("slider", m_Capture.VideoCount)
            dpg.set_value("Time", timeString)

            threshold = 100
            if ret == True:
                m_Capture.ChgMatImage(img)
                time.sleep(1/m_Capture.frame_rate)
            else:
                m_Capture.VideoCount = 0
                m_Capture.vid.release()
                m_Capture.vid = cv2.VideoCapture(m_Capture.VideoFile)

        dpg.render_dearpygui_frame()

    dpg.destroy_context()