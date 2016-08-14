from tkinter import Menu

from lib.PyWireDI.inject_decorator import inject
from lib.PyWireDI.post_construct_decorator import post_construct


class MenuBarModel:
    pass


class MenuBarView:
    def __init__(self):
        self.watch_list_controller = None
        self.version_popup_controller = None
        self.app_controller = None
        self.app_service = None

        self.controller = None

    @inject
    def set_app_service(self, app_service):
        self.app_service = app_service

    @inject
    def set_app_controller(self, app_controller):
        self.app_controller = app_controller

    @inject
    def set_menu_bar_controller(self, menu_bar_controller):
        self.controller = menu_bar_controller

    @inject
    def set_watch_list_controller(self, watch_list_controller):
        self.watch_list_controller = watch_list_controller

    @inject
    def set_version_popup_controller(self, version_popup_controller):
        self.version_popup_controller = version_popup_controller

    @post_construct
    def setup(self):
        menu_bar = Menu(self.app_controller.get_app_main_frame())

        menu_bar_file_menu = Menu(menu_bar, tearoff=0)
        menu_bar_file_menu.add_command(label="Add watch folder", command=self.watch_list_controller.add_folder)
        menu_bar_file_menu.add_command(label="Add watch file", command=self.watch_list_controller.add_file)
        menu_bar_file_menu.add_separator()
        menu_bar_file_menu.add_command(label="Quit", command=self.app_service.shutdown)
        menu_bar.add_cascade(label="Actions", menu=menu_bar_file_menu)

        menu_bar_about_menu = Menu(menu_bar, tearoff=0)
        menu_bar_about_menu.add_command(label="Version", command=self.version_popup_controller.open_popup)
        menu_bar.add_cascade(label="About", menu=menu_bar_about_menu)

        self.app_controller.get_app_window().config(menu=menu_bar)


class MenuBarController:
    pass
