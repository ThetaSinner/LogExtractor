import os
import queue
import time

from lib.PyWireDI.inject_decorator import inject


class LogWatcherService:
    def __init__(self):
        self.auto_wire = None
        self.exception_status_controller = None

        self.eventQueue = None
        self.fileWatchers = {}
        self.filePathListQueue = queue.Queue()
        self.isShutdownRequested = False

    @inject
    def set_exception_status_controller(self, exception_status_controller):
        self.exception_status_controller = exception_status_controller

    @inject
    def set_auto_wire(self, auto_wire):
        self.auto_wire = auto_wire

    def push_watch_locations(self, location_data):
        file_path_list = []

        for location in location_data:
            if os.path.isfile(location) and self._is_log_file(location):
                file_path_list.append(location)
            elif os.path.isdir(location):
                files_in_folder = [location + "/" + i for i in os.listdir(location) if self._is_log_file(i)]
                file_path_list.extend(files_in_folder)

        self.filePathListQueue.put(file_path_list)

    def request_shutdown(self):
        self.isShutdownRequested = True

    def run_in_background(self, event_queue):
        self.eventQueue = event_queue

        while True:
            if self.isShutdownRequested:
                break

            print("run in background")
            while not self.filePathListQueue.empty():
                self._update_watchers(self.filePathListQueue.get())

            self._update()

            time.sleep(1)

    def _update_watchers(self, file_path_list):
        # remove watchers for files which are no longer being watched.
        for filePath in self.fileWatchers:
            if filePath not in file_path_list:
                del self.fileWatchers[filePath]

        # add watchers for files are not already being watched.
        for filePath in file_path_list:
            if filePath not in self.fileWatchers:
                self.fileWatchers[filePath] = self.auto_wire.get("LogWatcher")
                self.fileWatchers[filePath].set_file_path(filePath)

    def _update(self):
        for filePath in self.fileWatchers:
            if self.fileWatchers[filePath].is_modified():
                exception_occurred = self.fileWatchers[filePath].scan_for_exceptions()

                if exception_occurred:
                    self.exception_status_controller.exception_occurred()

    @staticmethod
    def _is_log_file(file_name):
        return ".log" in file_name

