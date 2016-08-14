import random

from PyWireDI.inject_decorator import inject
from PyWireDI.scope import Scope

from archive.injectorv1 import Injector
from gui.watchListMVC import WatchListModel, WatchListController
from lib.PyWireDI.autoWire import AutoWire
from service.logWatcherService import LogWatcherService

injector = Injector()

injector.provide("logWatcherService", LogWatcherService())
injector.provide("watchListModel", WatchListModel)
injector.provide("watchListController", WatchListController)


def test():
    class UrlBuilder:
        def __init__(self):
            self.x = random.randint(1, 10)

        def build(self, val):
            print("a url: " + val + str(self.x))

    class P:
        def __init__(self):
            self.k = None
            self.url_builder = None

        @inject
        def set_k(self, k):
            self.k = k

        @inject
        def set_url_builder(self, url_builder):
            self.url_builder = url_builder

        def test(self):
            self.url_builder.build("p")
            print(self.k.do_test())

        def do_test(self):
            return "i'm p"

    class K:
        def __init__(self):
            self.p = None
            self.url_builder = None

        @inject
        def set_p(self, p):
            self.p = p

        @inject
        def set_url_builder(self, url_builder):
            self.url_builder = url_builder

        def test(self):
            self.url_builder.build("k")
            print(self.p.do_test())

        def do_test(self):
            return "i'm k"

    class Wurzle:
        def __init__(self):
            self.x = random.randint(20, 30)
            self.url_builder = None

        @inject
        def set_url_builder(self, url_builder):
            self.url_builder = url_builder

        def test(self):
            print(self.x)
            self.url_builder.build("wurzle")

    auto = AutoWire()
    auto.provide(P)
    auto.provide(K)
    auto.provide(UrlBuilder, scope=Scope.Prototype)
    auto.provide(Wurzle, scope=Scope.Prototype)

    auto.wire()

    auto.get("P").test()
    auto.get("K").test()
    auto.get("P").test()
    auto.get("K").test()

    auto.get("Wurzle").test()
    auto.get("Wurzle").test()
    auto.get("Wurzle").test()
    auto.get("UrlBuilder").build("after")
    auto.get("UrlBuilder").build("after")
    auto.get("UrlBuilder").build("after")
