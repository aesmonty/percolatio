from enum import Enum


class GrantState(Enum):
    RAISING = 1
    RECEIVING_APPLICATIONS = 2
    REVIEWING = 3
    COMPLETE = 4
    STALE = 5

    def __str__(self):
        return self.name

    def __int__(self):
        return self.value
