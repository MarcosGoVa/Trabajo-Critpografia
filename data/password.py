"""This module contains information for password"""
from data.attribute import Attribute

class Password(Attribute):
    """This class contains password information"""
    def __init__(self, password: str):
        super().__init__()
        # These are the minimum requirements for a password according to FDA
        self._validation_pattern = r"^(?=.*[A-Z])(?=.*[a-z])(?=.*[~!@#$%^*()_\-+={}[\]|:;?])(?=.*\d).{8,32}$"
        self._error_message = "password is not valid"
        self._attr_value = self._validate(password)