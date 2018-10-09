import random


class Item():
    PERCENT_CHANCE = 0.85

    def __init__(self, approved):
        self.__mValid = self.set_validity()
        self.__mApproved = approved

    def set_validity(self):
        if random.random() < 0.85:
            return True
        return False

    def is_valid(self):
        return self.__mValid

    def is_approved(self):
        return self.__mApproved
