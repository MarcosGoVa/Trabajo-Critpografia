"""This module contains information for date"""
from data.attribute import Attribute
from datetime import datetime

class Date(Attribute):
    """This class contains date information"""
    def __init__(self, date: str):
        super().__init__()
        self._error_message = "date is not valid"
        self._attr_value = self._validate(date)
    
    def _validate(self, value):
        format = "%d/%m/%Y"
        try:
            datetime.strptime(value, format)
        except ValueError:
            raise ValueError("Incorrect data format, should be DD-MM-YYYY")
    
        return value