from importlib import import_module


class DataMapperRegistry:
    def get(self, cls):
        class_name = cls.__name__
        data_mapper = import_module(f"data_mappers.{class_name.lower()}_data_mapper")
        data_mapper_class = getattr(data_mapper, f"{class_name}DataMapper")
        return data_mapper_class()
