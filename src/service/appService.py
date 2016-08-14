import queue
import threading

from lib.PyWireDI.inject_decorator import inject


class AppService:
    def __init__(self):
        self.watch_list_model = None
        self.watch_list_controller = None
        self.exception_status_controller = None
        self.exception_status_model = None
        self.app_controller = None

        self.log_watcher_service = None

        self.exceptionOutputQueue = queue.Queue()

    @inject
    def set_watch_list_model(self, watch_list_model):
        self.watch_list_model = watch_list_model

    @inject
    def set_watch_list_controller(self, watch_list_controller):
        self.watch_list_controller = watch_list_controller

    @inject
    def set_log_watcher_service(self, log_watcher_service):
        self.log_watcher_service = log_watcher_service

    @inject
    def set_exception_status_controller(self, exception_status_controller):
        self.exception_status_controller = exception_status_controller

    @inject
    def set_app_controller(self, app_controller):
        self.app_controller = app_controller

    def shutdown(self):
        print("shutdown")
        self.log_watcher_service.request_shutdown()
        self.app_controller.shutdown()

    def _run_in_foreground(self):
        # Move data from front end to back end.
        if self.watch_list_controller.is_watch_locations_updated():
            self.log_watcher_service.push_watch_locations(self.watch_list_controller.get_watch_locations())

        # Move data from back end to here.
        while not self.exceptionOutputQueue.empty():
            print(self.exceptionOutputQueue.get())

        self.app_controller.get_app_window().after(500, self._run_in_foreground)

    def start(self):
        threading.Thread(
            target=lambda: self.log_watcher_service.run_in_background(self.exceptionOutputQueue)).start()
        self._run_in_foreground()

        self.app_controller.launch()