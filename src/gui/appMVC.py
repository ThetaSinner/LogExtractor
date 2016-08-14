import tkinter
from tkinter import Tk

from lib.PyWireDI.inject_decorator import inject
from lib.PyWireDI.post_construct_decorator import post_construct


class AppModel:
    def __init__(self):
        self._title = "Log Extractor"
        self._icon_file = "res/gwenview.ico"

    def get_title(self):
        return self._title

    def get_icon_file(self):
        return self._icon_file


class AppView:
    def __init__(self):
        self.app_service = None

        # The app.
        self.app_window = Tk()
        self.app_window.geometry("820x440")

        # The main frame.
        self.app_main_frame = tkinter.Frame(self.app_window)
        self.app_main_frame.grid(padx=5, pady=5)

    @inject
    def set_app_service(self, app_service):
        self.app_service = app_service

    @post_construct
    def setup(self):
        self.app_window.bind("<Escape>", lambda event: self.app_service.shutdown())
        self.app_window.protocol("WM_DELETE_WINDOW", self.app_service.shutdown)

    def get_app_window(self):
        return self.app_window

    def get_app_main_frame(self):
        return self.app_main_frame

    def set_title(self, title_text):
        self.app_window.title(title_text)

    def set_icon(self, icon_file):
        self.app_window.iconbitmap(default=icon_file)

    def show(self):
        self.app_window.mainloop()

    def close(self):
        self.app_window.destroy()


class AppController:
    def __init__(self):
        self.model = None
        self.view = None

    @inject
    def set_app_model(self, app_model):
        self.model = app_model

    @inject
    def set_app_view(self, app_view):
        self.view = app_view

    @post_construct
    def setup(self):
        self.view.set_title(self.model.get_title())
        self.view.set_icon(self.model.get_icon_file())

    def shutdown(self):
        self.view.close()

    def launch(self):
        self.view.show()

    def get_app_window(self):
        return self.view.get_app_window()

    def get_app_main_frame(self):
        return self.view.get_app_main_frame()
