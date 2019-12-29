from data_mappers.registry import DataMapperRegistry


class BaseEntity:
    __initialized = False

    def __init__(self):
        self.__initialized = True

    def __setattr__(self, name, value):
        super(BaseEntity, self).__setattr__(name, value)
        if self.__initialized:
            data_mapper = DataMapperRegistry().get(self.__class__)
            data_mapper.update(self)

