import random


class Item():
    PERCENT_CHANCE = 0.85

    def __init__(self):
        self.__mValid = self.set_validity()
        self.__mAccepted = None

    def set_validity(self):
        return random.random() < 0.85

    def is_valid(self):
        return self.__mValid

    def set_acceptance(self, accepted):
        self.__mAccepted = accepted

    def is_accepted(self):
        return self.__mAccepted
