import os.path

from lib.PyWireDI.inject_decorator import inject

# I don't belong in the service package, where should I live?


class LogWatcher:
    def __init__(self):
        self.exception_tree_controller = None

        self.filePath = None
        self.lastModified = None
        self.lastLine = None

    @inject
    def set_exception_tree_controller(self, exception_tree_controller):
        self.exception_tree_controller = exception_tree_controller

    def set_file_path(self, file_path):
        self.filePath = file_path
        self.lastModified = self._system_lookup_modified_time(file_path)
        self.lastLine = ""

    def is_modified(self):
        new_last_modified = self._system_lookup_modified_time(self.filePath)
        is_file_modified = new_last_modified > self.lastModified
        self.lastModified = new_last_modified
        return is_file_modified

    def get_file_path(self):
        return self.filePath

    def scan_for_exceptions(self):
        exception_found = False

        f = open(self.filePath)
        text = f.read()

        if len(self.lastLine) is not 0:
            text = text[text.index(self.lastLine) + len(self.lastLine):]

        in_exception_mode = False
        for line in text.split("\n"):
            if len(line) is 0:
                continue

            if in_exception_mode:
                if line[0] is "\t":
                    print(line)
                    continue
                else:
                    in_exception_mode = False

            if "Exception" in line:
                print(line)
                self.exception_tree_controller.push_exception_for_file(line, self.filePath)
                exception_found = True
                in_exception_mode = True
            elif not line[0:1].isdigit():
                print(line)
                self.exception_tree_controller.push_exception_for_file(line, self.filePath)
                exception_found = True
                in_exception_mode = True

            # Only track the last line if it contains a timestamp.
            if line[0:1].isdigit():
                self.lastLine = line

        f.close()

        return exception_found

    @staticmethod
    def _system_lookup_modified_time(file_path):
        return os.path.getmtime(file_path)
