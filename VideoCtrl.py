import dearpygui.dearpygui as dpg
import cv2
import Capture
import time

m_Capture = Capture.Capture()

class DrawControl():
    texture_data = None
    InitVideoPath = ""

    def __init__(self):
        self.texture_data = m_Capture.InitTextureData()
        self.InitVideoPath = m_Capture.GetVideoPath()

    def SwitchVideoImg(self):
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

        if ret == True:
            dpg.set_value("texture_tag", m_Capture.ChgMatImage(img))
            time.sleep(1/m_Capture.frame_rate)
        else:
            m_Capture.VideoCount = 0
            m_Capture.vid.release()
            m_Capture.vid = cv2.VideoCapture(m_Capture.VideoFile)
    
    def SelectVideo(self,sender, app_data):
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

    def selectMovieFlie(self):
        dpg.add_button(label="Directory Selector", callback=lambda: dpg.show_item("file_dialog_id"))

    def DrawVideoCtrl(self):
        dpg.set_value("texture_tag", self.texture_data)
    
    def GetTextureData(self):
        return self.texture_data
    
    def SwitchStopAndStart(self):
        m_Capture.IsStartStop()

    def GetVideoStopFlg(self):
        return m_Capture.Is_videoStop
    
    def SetVideoType(self,type):
        m_Capture.Is_Color = type

    def GetVideoType(self):
        return m_Capture.Is_Color