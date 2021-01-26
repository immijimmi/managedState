import pytest


@pytest.fixture
def res():
    class DataClass:
        def __init__(self, **attributes):
            for name, value in attributes.items():
                setattr(self, name, value)

    class StateResources:
        value = {"key_1": 4}
        value_2 = {"key_1": [{}, {"key_2": 5}, {}]}
        value_3 = {"key_1": {"key_2": [], "key_3": {"key_4": 8}}}
        value_4 = {"key_1": {}, "key_2": DataClass(attribute_1={"key_3": 7})}

    return StateResources


@pytest.fixture
def listeners_obj():
    class ExampleListenersClass:
        def __init__(self):
            self.list = []

        def add_get_path_keys_to_list(self, state_obj, path_keys=(), defaults=()):
            self.list.append(path_keys)

        def add_set_value_to_list(self, state_obj, value, path_keys=(), defaults=()):
            self.list.append(value)

    return ExampleListenersClass()
