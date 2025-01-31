
from enum import Enum

#GENERAL PARAMETERS
AREA_TO_TARGET_FACTOR = 0.1
MIN_POWER_THRESHOLD = 0.1
POWER_TO_DAMAGE = 10


class enum_NodeType(Enum):
    ENERGY= 1,
    MOD = 2,
    DMG = 3,
    STATIC = 4

class enum_ElementalType(Enum):
    FIRE = 1,
    WATER = 2,
    EARTH = 3,
    AIR = 4