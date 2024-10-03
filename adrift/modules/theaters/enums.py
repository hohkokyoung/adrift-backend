from enum import Enum

class Screen(Enum):
    IMAX = 'IMAX'
    _3D = '3D'
    STANDARD = 'Standard'
    _4DX = '4DX'

    def __str__(self):
        return self.name

class Seat(Enum):
    NORMAL = 'Normal'
    COUPLE = 'Couple'
    DISABLED = 'Disabled'

    def __str__(self):
        return self.name
