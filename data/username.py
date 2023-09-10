"""This module contains information for username"""
from data.attribute import Attribute

class Username(Attribute):
    """This class contains username information"""
    def __init__(self, username: str):
        super().__init__()
        self._validation_pattern = r"^[a-zA-Z0-9_]{4,32}$"
        self._error_message = "username is not valid"
        self._attr_value = self._validate(username)