"""Module for the Attribute class"""
# pylint: disable=too-few-public-methods
import re

class Attribute():
    """This class contains attributes information"""
    def __init__(self):
        self._attr_value = ""
        """regex validation pattern"""
        self._validation_pattern = r""
        """Default error message"""
        self._error_message = ""

    def _validate(self, value):
        """This method validates the introduced value"""
        myregex = re.compile(self._validation_pattern)
        regex_matches = myregex.fullmatch(value)
        if not regex_matches:
            raise ValueError(self._error_message)
        return value
    @property
    def value(self):
        """This method returns the introduced value"""
        return self._attr_value

    @value.setter
    def value(self, attr_value):
        self._attr_value = self._validate(attr_value)