class Plugin:
    def __init__(self, *args, **kwargs):
        print('Plugin init("sampletask2");', args, kwargs)

    def execute(self, a, b):
        return a-b