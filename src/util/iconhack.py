import ctypes


def run_icon_hack():
    appid = 'uk.thetasinner.logextractor.0.0.1'
    ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(appid)
