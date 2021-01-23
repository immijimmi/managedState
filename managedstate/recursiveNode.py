from copy import deepcopy
from typing import Sequence, Any

from .keyQuery import KeyQuery
from .propertyName import PropertyName


class RecursiveNode:
    def __init__(self, value: Any, path_keys: Sequence[Any] = (), defaults: Sequence[Any] = ()):
        self.__value = try_copy(value)
        self.__path_keys = path_keys
        self.__defaults = defaults

        self.__child = None if not path_keys else RecursiveNode(
            self.__get_child_value(),
            self.__path_keys[1:],
            self.__defaults[1:]
        )

    @property
    def value(self) -> Any:
        return self.__value

    def get(self) -> Any:
        return self.__child.get() if self.__child else self.__value

    def set(self, value: Any) -> None:
        if self.__child:
            self.__child.set(value)
            self.__update_value()

        else:
            self.__value = try_copy(value)

    def __get_working_key(self) -> Any:
        working_key = self.__path_keys[0]

        if type(working_key) is KeyQuery:
            working_key = working_key(try_copy(self.__value))

        return try_copy(working_key)

    def __get_child_value(self) -> Any:
        try:
            working_key = self.__get_working_key()

            child_value = (
                getattr(self.__value, working_key.name)
                if type(working_key) is PropertyName
                else self.__value[working_key]
            )

        except:  # This includes exceptions raised by passed in queries
            if not self.__defaults:
                raise ValueError("No value found and no default provided for the key: {}".format(self.__path_keys[0]))

            child_value = self.__defaults[0]

        return child_value

    def __update_value(self) -> None:
        working_key = self.__get_working_key()

        if type(working_key) is PropertyName:
            setattr(self.__value, working_key.name, self.__child.value)

        else:
            self.__value[working_key] = self.__child.value


def try_copy(item: Any) -> Any:
    """
    A failsafe deepcopy wrapper
    """

    try:
        return deepcopy(item)

    except:
        return item
