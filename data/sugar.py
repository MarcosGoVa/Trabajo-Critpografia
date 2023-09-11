"""This module contains information for sugar_data"""
from data.attribute import Attribute

class Sugar(Attribute):
    """This class contains sugar_data information"""
    def __init__(self, sugar: int):
        super().__init__()
        self._attr_value = self._validate(sugar)

    def _validate(self, value):
        sugar_level = int(value)
        if sugar_level <= 0:
            raise ValueError("sugar data is not valid")
        
        if sugar_level >= 1000:
            raise ValueError("sugar data is not valid")
        
        return sugar_level