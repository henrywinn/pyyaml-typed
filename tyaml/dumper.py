from yaml import Dumper

from tyaml.types import get_mappings

from typing import get_type_hints


class OutputOptionalNullsDumper(Dumper):  # pylint: disable=too-many-ancestors
    """Dumper overriding standard `represent_object` method"""

    def represent_object(self, data):
        mappings = get_mappings(type(data))  # find yaml fields mappings
        if not mappings:
            return super().represent_object(data)
        result_dict = {}
        for attribute, field_name in mappings.items():
            result_dict[field_name] = getattr(data, attribute)
        return self.represent_dict(result_dict)


OutputOptionalNullsDumper.add_multi_representer(object, OutputOptionalNullsDumper.represent_object)

class NoOutputOptionalNullsDumper(Dumper):  # pylint: disable=too-many-ancestors
    """Dumper overriding standard `represent_object` method"""

    def represent_object(self, data):
        mappings = get_mappings(type(data))  # find yaml fields mappings
        if not mappings:
            _data = data
            try:
                _data = vars(data)
                for key in _data.keys():
                    if self._is_optional(data, key):
                        del _data[key]
            except TypeError:
                pass
            data = _data
            return super().represent_object(data)
        result_dict = {}
        for attribute, field_name in mappings.items():
            result_dict[field_name] = getattr(data, attribute)
        return self.represent_dict(result_dict)
    
    def _is_optional(self, data, attr):
        return False
        # TODO: Figure out how to determine if an object is Optional
        
        ## Test 1: From https://stackoverflow.com/questions/56832881/check-if-a-field-is-typing-optional
        # return hasattr(getattr(data, attr).type, "__args__") \
        #     and len(getattr(data, attr).type.__args__) == 2 \
        #     and getattr(data, attr).type.__args__[-1] is type(None)

        ## Test 2
        # type_hint = get_type_hints(data)[attr]
        # return type_hint is Optional # Always returns False
        ## there are various iterations of `type_hint is` that we could use, but none are very elegant


NoOutputOptionalNullsDumper.add_multi_representer(object, NoOutputOptionalNullsDumper.represent_object)
