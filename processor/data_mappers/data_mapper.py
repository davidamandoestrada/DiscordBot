class Singleton(object):
    _instance = None

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = object.__new__(cls, *args, **kwargs)
        return cls._instance


class DataMapper(Singleton):
    pass


class InMemoryDataMapper(DataMapper):
    def flush(self):
        print("This is the current entities", flush=True)
        print(self.entities, flush=True)
        print("About to flush", flush=True)
        self.entities = {}
        print(self.entities, flush=True)
