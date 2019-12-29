import sys
from importlib import import_module


class DataMapperRegistry:
    def get(self, cls):
        class_name = cls.__name__
        data_mapper_module_name = f"{class_name.lower()}_data_mapper"

        if "pytest" in sys.modules:
            data_mapper_class_name = f"InMemory{class_name}DataMapper"
        else:
            data_mapper_class_name = f"{class_name}DataMapper"

        data_mapper = import_module(f"data_mappers.{data_mapper_module_name}")
        data_mapper_class = getattr(data_mapper, data_mapper_class_name)
        return data_mapper_class()
