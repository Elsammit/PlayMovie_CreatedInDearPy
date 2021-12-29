import dearpygui.dearpygui as dpg
import numpy as np
import cv2
import time

dpg.create_context()
dpg.create_viewport(max_width=800, max_height=800)
dpg.setup_dearpygui()

Is_Color = 0
Is_videoStop = False
VideoFile = "X:\StudyCode\python\Clouds - 35573.mp4"
VideoCount = 0

vid = cv2.VideoCapture(VideoFile)
ret, img = vid.read()
frame_rate = int(vid.get(cv2.CAP_PROP_FPS))
img = cv2.resize(img , (480, 270))

data = np.flip(img, 2) 
data = data.ravel()
data = np.asfarray(data, dtype='f')
texture_data = np.true_divide(data, 255.0)

def video_callback():
    global Is_videoStop
    print("Clicked")

    if Is_videoStop == False:
        Is_videoStop = True
    else:
        Is_videoStop = False

def callback(sender, app_data):
    global vid
    global Is_videoStop
    global VideoFile
    print("Sender: ", sender)
    print("App Data: ", app_data)
    print(app_data["file_path_name"])
    Is_videoStop = False
    VideoFile = app_data["file_path_name"]
    vid.release()
    vid = cv2.VideoCapture(VideoFile)
    time.sleep(0.3)
    Is_videoStop = True
    dpg.set_value("Main Title", app_data["file_path_name"])


with dpg.texture_registry(show=False):
    dpg.add_raw_texture(480, 270, texture_data, tag="texture_tag", format=dpg.mvFormat_Float_rgb, use_internal_label=False)

def MakeSubWindow():
    dpg.add_button(label="Directory Selector", callback=lambda: dpg.show_item("file_dialog_id"))
    with dpg.menu(label="動画選択"):

        def _selection(sender, app_data, user_data):
            global Is_Color
            for item in user_data:
                if item != sender:
                    dpg.set_value(item, False)
                else:
                    Is_Color = int(item) - 35
                    print(Is_Color)
                    
        items = (
            dpg.add_checkbox(label="1. I am selectable"),
            dpg.add_checkbox(label="2. I am selectable"),
            dpg.add_checkbox(label="3. I am selectable"),
            dpg.add_checkbox(label="4. I am selectable"),
            dpg.add_checkbox(label="5. I am selectable"),
            )

        for item in items:
            dpg.configure_item(item, callback=_selection, user_data=items)

with dpg.window(label="Main window",pos=[100,100]):
    dpg.add_text(tag="Main Title",default_value="Hello, world")
    MakeSubWindow()

    dpg.add_image("texture_tag")
    dpg.add_progress_bar(tag="slider",pos=[10,320])
    dpg.add_text(tag="Time",default_value="0",pos=[350,320])
    dpg.add_button(label="Save", callback=video_callback, pos=[10,350])
    
with dpg.file_dialog(directory_selector=False, show=False, callback=callback, tag="file_dialog_id"):
    dpg.add_file_extension(".mp4")
    dpg.add_file_extension("", color=(150, 255, 150, 255))

dpg.show_metrics()
dpg.show_viewport()

while dpg.is_dearpygui_running():
    if Is_videoStop == True:
        ret, img = vid.read()
        Timer = 0
        timeString = "0/0"
        if vid.get(cv2.CAP_PROP_FRAME_COUNT) == 0:
            VideoCount = 0
        else:
            VideoCount = (1 / vid.get(cv2.CAP_PROP_FRAME_COUNT)) + VideoCount
            Timer = vid.get(cv2.CAP_PROP_POS_FRAMES) / vid.get(cv2.CAP_PROP_FPS)
        if vid.get(cv2.CAP_PROP_FPS) == 0:
            timeString = "0/0"
        else:    
            timeString = str(round(Timer)) + "/" + str(round(vid.get(cv2.CAP_PROP_FRAME_COUNT) / vid.get(cv2.CAP_PROP_FPS)))
        
        dpg.set_value("slider", VideoCount)
        dpg.set_value("Time", timeString)
        if ret == True:
            if Is_Color == 1:
                img_gry = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
                img_gry = cv2.merge((img_gry, img_gry, img_gry))
                img_gry = cv2.resize(img_gry , (480, 270))
                data = np.flip(img_gry, 2)
            elif Is_Color == 2:
                height = img.shape[0]
                width = img.shape[1]
                zeros = np.zeros((height, width), img.dtype)
                img_blue = cv2.merge((img[:,:,0], zeros, zeros))
                img_blue = cv2.resize(img_blue , (480, 270))
                data = np.flip(img_blue, 2)
            elif Is_Color == 3:
                height = img.shape[0]
                width = img.shape[1]
                zeros = np.zeros((height, width), img.dtype)
                img_blue = cv2.merge((zeros, img[:,:,1], zeros))
                img_blue = cv2.resize(img_blue , (480, 270))
                data = np.flip(img_blue, 2)
            elif Is_Color == 4:
                height = img.shape[0]
                width = img.shape[1]
                zeros = np.zeros((height, width), img.dtype)
                img_blue = cv2.merge((zeros, zeros, img[:,:,2]))
                img_blue = cv2.resize(img_blue , (480, 270))
                data = np.flip(img_blue, 2)
            else:
                img = img
                img = cv2.resize(img , (480, 270))
                data = np.flip(img, 2)
            data = data.ravel()
            data = np.asfarray(data, dtype='f')
            texture_data = np.true_divide(data, 255.0)
                
            dpg.set_value("texture_tag", texture_data)

            time.sleep(1/frame_rate)
        else:
            VideoCount = 0
            vid.release()
            vid = cv2.VideoCapture(VideoFile)

    dpg.render_dearpygui_frame()

dpg.destroy_context()