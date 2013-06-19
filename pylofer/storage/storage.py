class Container(object):
    def __init__(self, namespace="", config={}):
        self.config = config
        self.namespace = namespace

    def save(self, obj):
        raise NotImplementedError("Do not know how to save.")

class Storage(object):
    def __init__(self):
        raise NotImplementedError("No instance of this class allowed.")

    def save(self, obj):
        raise NotImplementedError("Abstract class")

    def _get_container(self, typ, obj):
        container = getattr(self.container, typ.__class__, None)
        if not container:
            container = FileContainer(obj.typ, self.config)
            self.container[typ.__class__] = {}
            self.container[typ.__class__][obj.typ] = container

        if obj.typ not in container:
            container = FileContainer(obj.typ, self.config)
            container[obj.typ] = container

        return container[obj.typ]

