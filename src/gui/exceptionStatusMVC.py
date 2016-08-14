import tkinter
from tkinter import ttk

from lib.PyWireDI.inject_decorator import inject
from lib.PyWireDI.post_construct_decorator import post_construct


class ExceptionStatusModel:
    pass


class ExceptionStatusView:
    def __init__(self):
        self.controller = None
        self.app_controller = None

        self.status_canvas = None
        self.status_light = None

    @inject
    def set_exception_status_controller(self, exception_status_controller):
        self.controller = exception_status_controller

    @inject
    def set_app_controller(self, app_controller):
        self.app_controller = app_controller

    @post_construct
    def setup(self):
        size = 30
        parent_element = self.app_controller.get_app_main_frame()

        exception_status_frame = tkinter.Frame(parent_element)
        # background="green"
        exception_status_frame.grid(row=1, column=1, padx=5, sticky=tkinter.W)
        # pack side=tkinter.RIGHT, anchor=tkinter.N, fill=tkinter.BOTH, expand=tkinter.YES

        self.status_canvas = tkinter.Canvas(exception_status_frame, width=size, height=size)
        self.status_canvas.pack()

        self.status_light = self.status_canvas.create_oval(2, 2, size, size, fill="green")

        acknowledge_button = ttk.Button(exception_status_frame, text="acknowledge",
                                        command=self.controller.acknowledge_exception)
        acknowledge_button.pack()

    def set_green_light(self):
        self.status_canvas.itemconfig(self.status_light, fill="green")

    def set_red_light(self):
        self.status_canvas.itemconfig(self.status_light, fill="red")


class ExceptionStatusController:
    def __init__(self):
        self.model = None
        self.view = None
        self.exception_tree_controller = None

    @inject
    def set_exception_status_model(self, exception_status_model):
        self.model = exception_status_model

    @inject
    def set_exception_status_view(self, exception_status_view):
        self.view = exception_status_view

    @inject
    def set_exception_tree_controller(self, exception_tree_controller):
        self.exception_tree_controller = exception_tree_controller

    def exception_occurred(self):
        self.view.set_red_light()

    def acknowledge_exception(self):
        self.exception_tree_controller.mark_all_as_old()
        self.view.set_green_light()
