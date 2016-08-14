import copy
import tkinter
from tkinter import ttk

from lib.PyWireDI.inject_decorator import inject
from lib.PyWireDI.post_construct_decorator import post_construct


class ExceptionTreeModel:
    def __init__(self):
        self.exceptions_by_file = {}

    def push_exception_for_file(self, exception, file):
        if file not in self.exceptions_by_file:
            self.exceptions_by_file[file] = []

        self.exceptions_by_file[file].append(self.to_model(exception))

    def get_exceptions_by_file(self):
        current_exceptions_by_file = copy.deepcopy(self.exceptions_by_file)
        return current_exceptions_by_file

    def mark_all_as_old(self):
        for file_key in self.exceptions_by_file:
            for exception_data in self.exceptions_by_file[file_key]:
                exception_data["new"] = False

    def clear(self):
        self.exceptions_by_file = {}

    @staticmethod
    def to_model(exception):
        return {"exception": exception, "new": True}


class ExceptionTreeView:
    def __init__(self):
        self.app_controller = None
        self.exception_list_list_box = None
        self.exception_tree_controller = None

    @inject
    def set_app_controller(self, app_controller):
        self.app_controller = app_controller

    @inject
    def set_exception_tree_controller(self, exception_tree_controller):
        self.exception_tree_controller = exception_tree_controller

    @post_construct
    def setup(self):
        parent_frame = self.app_controller.get_app_main_frame()

        exception_tree_parent_frame = tkinter.Frame(parent_frame)
        exception_tree_parent_frame.grid(row=1, column=0, sticky=tkinter.W+tkinter.E)

        label = ttk.Label(exception_tree_parent_frame, text="Exceptions by file")
        label.grid(row=0, column=0, sticky=tkinter.W)

        exception_list_frame = tkinter.Frame(exception_tree_parent_frame)
        exception_list_frame.grid(row=1, column=0, sticky=tkinter.W)

        self.exception_list_list_box = ttk.Treeview(exception_list_frame, selectmode='none')
        self.exception_list_list_box.column('#0', width=600)
        self.exception_list_list_box.pack(side=tkinter.LEFT, fill=tkinter.Y)

        exception_list_list_box_scrollbar = tkinter.Scrollbar(exception_list_frame)
        exception_list_list_box_scrollbar.pack(side=tkinter.RIGHT, fill=tkinter.Y)
        exception_list_list_box_scrollbar.config(command=self.exception_list_list_box.yview)

        self.exception_list_list_box.config(yscrollcommand=exception_list_list_box_scrollbar.set)

        exception_tree_clear_button = ttk.Button(exception_tree_parent_frame, text="Clear",
                                                 command=self.exception_tree_controller.clear)
        exception_tree_clear_button.grid(row=1, column=1, sticky=tkinter.W+tkinter.E+tkinter.N)

        exception_tree_parent_frame.columnconfigure(1, weight=1)

    def refresh(self, exceptions_by_file):
        for i in self.exception_list_list_box.get_children():
            self.exception_list_list_box.delete(i)

        for file_key in exceptions_by_file:
            for exception_data in exceptions_by_file[file_key]:
                self.push_exception_data_for_file(exception_data, file_key)

    def push_exception_data_for_file(self, exception_data, file_key):
        if not self.exception_list_list_box.exists(file_key):
            self.exception_list_list_box.insert('', 'end', file_key, text=file_key)

        self.exception_list_list_box.item(file_key, tags="new")

        if exception_data["new"]:
            self.exception_list_list_box.insert(file_key, 'end', text=exception_data["exception"], tags="new")
        else:
            self.exception_list_list_box.insert(file_key, 'end', text=exception_data["exception"])

        self.exception_list_list_box.tag_configure("new", foreground="red")

    def strip_new_tags(self):
        for file_key in self.exception_list_list_box.get_children():
            self.exception_list_list_box.item(file_key, tags=())

            for exception in self.exception_list_list_box.get_children(file_key):
                self.exception_list_list_box.item(exception, tags=())


class ExceptionTreeController:
    def __init__(self):
        self.model = None
        self.view = None

    @inject
    def set_exception_tree_model(self, model):
        self.model = model

    @inject
    def set_exception_tree_view(self, view):
        self.view = view

    def push_exception_for_file(self, exception, file):
        self.model.push_exception_for_file(exception, file)

        exception_data = self.model.to_model(exception)
        self.view.push_exception_data_for_file(exception_data, file)

    def refresh(self):
        exceptions_by_file = self.model.get_exceptions_by_file()
        self.view.refresh(exceptions_by_file)

    def mark_all_as_old(self):
        self.model.mark_all_as_old()
        self.view.strip_new_tags()

    def clear(self):
        self.model.clear()
        self.view.refresh({})
