
from enum import Enum

#GENERAL PARAMETERS
AREA_TO_TARGET_FACTOR = 0.05
MIN_DAMAGE_THRESHOLD = 0.

#NODE PARAMETERS
CAST_RATE = 0.2
CAST_POWER = 1.0


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