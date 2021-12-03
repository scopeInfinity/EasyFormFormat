from abc import ABC, abstractmethod
from typing import Optional


class Serializable(ABC):

    @abstractmethod
    def unmarshal(self, data):
        pass

    @abstractmethod
    def marshal(self):
        pass

    def unmarshal_get_value(self, data, key, _type: Optional[type] = None):
        value = data[key]
        return self.unmarshal_value(value)

    def unmarshal_value(self, value, _type: Optional[type] = None):
        if _type is not None and not isinstance(value, _type):
            raise ValueError(
                f"unmarshal value is of type {type(value)} want {_type}")
        return value
