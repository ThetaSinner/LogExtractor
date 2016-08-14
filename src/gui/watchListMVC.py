import tkinter
from tkinter import ttk, filedialog

from lib.PyWireDI.inject_decorator import inject
from lib.PyWireDI.post_construct_decorator import post_construct


class WatchListModel:
    pass


class WatchListView:
    def __init__(self):
        self.controller = None

        self.app_controller = None
        self.watched_locations_list_box = None

    @inject
    def set_app_controller(self, app_controller):
        self.app_controller = app_controller

    @inject
    def set_watch_list_controller(self, watch_list_controller):
        self.controller = watch_list_controller

    @post_construct
    def setup(self):
        parent_container = self.app_controller.get_app_main_frame()

        watch_list_parent_frame = tkinter.Frame(parent_container)
        watch_list_parent_frame.grid(row=0, column=0)

        label = ttk.Label(watch_list_parent_frame, text="Watched files")
        label.grid(row=0, column=0, sticky=tkinter.W)

        watch_list_frame = tkinter.Frame(watch_list_parent_frame)
        watch_list_frame.grid(row=1, column=0)

        self._create_watch_list_listbox(watch_list_frame)
        self._create_remove_selected_button(watch_list_parent_frame)

    def _create_watch_list_listbox(self, watch_list_parent_frame):
        watched_locations_frame = ttk.Frame(watch_list_parent_frame)
        watched_locations_frame.pack()

        self.watched_locations_list_box = tkinter.Listbox(watched_locations_frame, selectmode=tkinter.EXTENDED,
                                                          width=100, activestyle="none")
        self.watched_locations_list_box.pack(side=tkinter.LEFT, fill=tkinter.Y)

        watched_locations_list_box_scrollbar = tkinter.Scrollbar(watched_locations_frame)
        watched_locations_list_box_scrollbar.pack(side=tkinter.RIGHT, fill=tkinter.Y)
        watched_locations_list_box_scrollbar.config(command=self.watched_locations_list_box.yview)

        self.watched_locations_list_box.config(yscrollcommand=watched_locations_list_box_scrollbar.set)

    def _create_remove_selected_button(self, watch_list_parent_frame):
        remove_selected_button = ttk.Button(watch_list_parent_frame, text="Remove selected.",
                                            command=self.controller.remove_selected)
        remove_selected_button.grid(row=1, column=1, sticky=tkinter.N)

    def get_watched_locations_list_box(self):
        return self.watched_locations_list_box


class WatchListController:
    """ Split this into model and controller rather than just controller """

    def __init__(self):
        self.model = None
        self.view = None

        self.isUpdated = False

    @inject
    def set_watch_list_model(self, watch_list_model):
        self.model = watch_list_model

    @inject
    def set_watch_list_view(self, watch_list_view):
        self.view = watch_list_view

    def add_folder(self):
        folder = filedialog.askdirectory(title="Choose folders to watch")

        if folder is not "":
            self.view.get_watched_locations_list_box().insert(tkinter.END, folder)
            self.view.get_watched_locations_list_box().see(tkinter.END)
            self._trigger_update()

    def add_file(self):
        files = filedialog.askopenfilename(multiple=True, title="Choose files to watch")

        if len(files) is not 0:
            for file in files:
                self.view.get_watched_locations_list_box().insert(tkinter.END, file)

            self.view.get_watched_locations_list_box().see(tkinter.END)
            self._trigger_update()

    def remove_selected(self):
        is_update = False
        if len(self.view.get_watched_locations_list_box().curselection()) is not 0:
            is_update = True

        for thing in self.view.get_watched_locations_list_box().curselection()[::-1]:
            self.view.get_watched_locations_list_box().delete(thing)

        if is_update:
            self._trigger_update()

    def is_watch_locations_updated(self):
        updated = self.isUpdated
        self.isUpdated = False
        return updated

    def get_watch_locations(self):
        return self.watchLocations

    def _trigger_update(self):
        self.watchLocations = self.view.get_watched_locations_list_box().get(0, tkinter.END)
        self.isUpdated = True
