def deprecated(method):
    def call_deprecated(*args):
        print("Call to deprecated method [" + method.__name__ + "]")
        return method(*args)

    return call_deprecated


class Injector:
    def __init__(self):
        self.container = {}
        self.features = {}
        self.builtFeatures = {}

    @deprecated
    def provide(self, name, value):
        self.features[name] = value

    @deprecated
    def get(self, feature):
        return self.features[feature]

    @deprecated
    def get_build(self, feature, *args):
        if feature not in self.builtFeatures:
            self.builtFeatures[feature] = self.features[feature](*args)

        return self.builtFeatures[feature]

    @deprecated
    def provide_singleton(self, name, value, *args):
        if inspect.isclass(value):
            self.container[name] = Item(Scope.Singleton, value(*args))
        else:
            self.container[name] = Item(Scope.Singleton, value)

    @deprecated
    def provide_prototype(self, name, value):
        self.container[name] = Item(Scope.Prototype, value)

    @deprecated
    def retrieve(self, name, *args):
        if self.container[name].scope is Scope.Singleton:
            return self.container[name].value
        elif self.container[name].scope is Scope.Prototype:
            return self.container[name].value(*args)

    @deprecated
    def can_retrieve(self, name):
        return name in self.container

    @deprecated
    def inject(self, method):
        def action(target):
            method_name = method.__name__
            # setattr(target, injector.retrieve())
            if method_name.find("_get_") == 0 or method_name.find("_set_") == 0:
                method_name = method_name[5:]
            elif method_name.find("get_") == 0 or method_name.find("set_") == 0:
                method_name = method_name[4:]
            elif method_name.find("get") == 0 or method_name.find("set") == 0:
                method_name = method_name[3:]

            if method_name[0].isupper():
                method_name = method_name[0].lower() + method_name[1:]

            print(method_name)
            print(self.can_retrieve(method_name))

            if self.can_retrieve(method_name):
                return self.retrieve(method_name)

        return action


class Item:
    def __init__(self, scope, value):
        self.scope = scope
        self.value = value