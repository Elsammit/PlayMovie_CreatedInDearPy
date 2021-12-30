import dearpygui.dearpygui as dpg
import VideoCtrl

m_DrawControl = VideoCtrl.DrawControl()

class DrawWindow():
    def __init__(self):
        dpg.create_context()
        dpg.create_viewport(max_width=800, max_height=800)
        dpg.setup_dearpygui()

    def MainWindow(self):
        with dpg.texture_registry(show=False):
            dpg.add_raw_texture(480, 270, m_DrawControl.GetTextureData(), tag="texture_tag", format=dpg.mvFormat_Float_rgb, use_internal_label=False)

        with dpg.window(label="Main window",pos=[100,100]):
            dpg.add_text(tag="Main Title",default_value=m_DrawControl.InitVideoPath)
            m_DrawControl.selectMovieFlie()
            self.MakeSubWindow()

            dpg.add_image("texture_tag")
            dpg.add_progress_bar(tag="slider",pos=[10,320])
            dpg.add_text(tag="Time",default_value="0",pos=[350,320])
            dpg.add_button(label="Save", callback=m_DrawControl.SwitchStopAndStart, pos=[10,350])

    def DrawDialog(self):
        with dpg.file_dialog(directory_selector=False, show=False, callback=m_DrawControl.SelectVideo, tag="file_dialog_id"):
            dpg.add_file_extension(".mp4")

            dpg.add_file_extension("", color=(150, 255, 150, 255))

    def ShowWindow(self):
        dpg.show_metrics()
        dpg.show_viewport()

    def DrawMovie(self):
        while dpg.is_dearpygui_running():
            if m_DrawControl.GetVideoStopFlg() == True:
                m_DrawControl.SwitchVideoImg()

            dpg.render_dearpygui_frame()

    def MakeSubWindow(self):
        with dpg.menu(label="select movie type"):

            def _selection(sender, app_data, user_data):
                for item in user_data:
                    if item == sender:
                        m_DrawControl.SetVideoType(int(item) - 27)
                        
            items = (
                dpg.add_selectable(label="Color"),
                dpg.add_selectable(label="Gray"),
                dpg.add_selectable(label="Binary"),
                dpg.add_selectable(label="Edge"),
                dpg.add_selectable(label="Contour extraction"),
                )

            for item in items:
                dpg.configure_item(item, callback=_selection, user_data=items)

m_DrawWindow = DrawWindow()

if __name__=='__main__':
    m_DrawWindow.MainWindow()
    m_DrawWindow.DrawDialog()
    m_DrawWindow.ShowWindow()
    m_DrawWindow.DrawMovie()

    dpg.destroy_context()