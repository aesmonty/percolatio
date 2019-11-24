from enum import Enum


class GrantState(Enum):
    RAISING = 1
    RECEIVING_APPLICATIONS = 2
    REVIEWING = 3
    COMPLETE = 4
    STALE = 5
