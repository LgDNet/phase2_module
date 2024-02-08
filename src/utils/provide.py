class classproperty:  # noqa
    def __init__(self, method):
        self.func = method

    def __get__(self, instance, cls):
        return self.func(cls)
