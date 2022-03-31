from Baumanagement.models.abstract import BaseModel


def get_base_models():
    result = {}
    for cls in BaseModel.__subclasses__():
        result[cls.__name__.lower()] = cls
    return result
