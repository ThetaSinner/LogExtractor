from tkinter import Toplevel, Label, Button

from lib.PyWireDI.inject_decorator import inject
from util.geometryHelper import GeometryHelper


class VersionPopupModel:
    def __init__(self):
        self._version = "0.0.1"

    def get_version(self):
        return self._version


class VersionPopupView:
    def __init__(self):
        self.controller = None
        self.app_controller = None

        self.version_label = None
        self.popup = None

    @inject
    def set_version_popup_controller(self, controller):
        self.controller = controller

    @inject
    def set_app_controller(self, app_controller):
        self.app_controller = app_controller

    def show_popup(self):
        geometry_helper = GeometryHelper(self.app_controller.get_app_window())

        popup_width = 250
        popup_height = 70
        popup_position_top = int(geometry_helper.get_y() + 0.5 * geometry_helper.get_height() - 0.5 * popup_height)
        popup_position_left = int(geometry_helper.get_x() + 0.5 * geometry_helper.get_width() - 0.5 * popup_width)

        self.popup = Toplevel(self.app_controller.get_app_window())
        self.popup.title("Version")
        self.popup.geometry(
            str(popup_width) + "x" + str(popup_height) + "+" + str(popup_position_left) + "+" + str(popup_position_top))
        self.popup.grab_set()

        self.version_label = Label(self.popup)
        self.version_label.pack()

        ok_button = Button(self.popup, width=25, height=20, text="OK", command=self.controller.close_popup)
        ok_button.pack(pady=5)

    def get_popup_window(self):
        return self.popup

    def set_version_label_text(self, version_text):
        self.version_label.config(text=version_text)


class VersionPopupController:
    def __init__(self):
        self.model = None
        self.view = None

    @inject
    def set_version_popup_model(self, version_popup_model):
        self.model = version_popup_model

    @inject
    def set_version_popup_view(self, version_popup_view):
        self.view = version_popup_view

    def open_popup(self):
        self.view.show_popup()
        self.view.set_version_label_text(self.model.get_version())

    def close_popup(self):
        self.view.get_popup_window().grab_release()
        self.view.get_popup_window().destroy()

