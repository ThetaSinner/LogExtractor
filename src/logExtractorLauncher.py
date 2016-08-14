from gui.appMVC import AppModel, AppView, AppController
from gui.exceptionStatusMVC import ExceptionStatusController
from gui.exceptionStatusMVC import ExceptionStatusModel
from gui.exceptionStatusMVC import ExceptionStatusView
from gui.exceptionTreeMVC import ExceptionTreeModel, ExceptionTreeView, ExceptionTreeController
from gui.menuBarMVC import MenuBarModel, MenuBarView, MenuBarController
from gui.versionPopupMVC import VersionPopupModel, VersionPopupView, VersionPopupController
from gui.watchListMVC import WatchListModel, WatchListView, WatchListController
from lib.PyWireDI.autoWire import AutoWire
from lib.PyWireDI.scope import Scope
from service.appService import AppService
from service.logWatcher import LogWatcher
from service.logWatcherService import LogWatcherService
from util.iconhack import run_icon_hack

if __name__ == '__main__':
    run_icon_hack()

    wiring = AutoWire()

    wiring.provide(WatchListModel)
    wiring.provide(WatchListView)
    wiring.provide(WatchListController)

    wiring.provide(MenuBarModel)
    wiring.provide(MenuBarView)
    wiring.provide(MenuBarController)

    wiring.provide(VersionPopupModel)
    wiring.provide(VersionPopupView)
    wiring.provide(VersionPopupController)

    wiring.provide(ExceptionStatusView)
    wiring.provide(ExceptionStatusModel)
    wiring.provide(ExceptionStatusController)

    wiring.provide(ExceptionTreeModel)
    wiring.provide(ExceptionTreeView)
    wiring.provide(ExceptionTreeController)

    wiring.provide(AppModel)
    wiring.provide(AppView)
    wiring.provide(AppController)

    wiring.provide(LogWatcher, scope=Scope.Prototype)
    wiring.provide(LogWatcherService)

    wiring.provide(AppService)

    wiring.wire()

    wiring.get("AppService").start()
