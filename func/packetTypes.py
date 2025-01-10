from  .configAndEnums import *

class EnergyPacket():
    def __init__(self, power: float, elemental_tendency = None):
        self._power = power
        if elemental_tendency == None:
            self._fireTendency = 1.0
            self._waterTendency = 1.0
            self._airTendency = 1.0
            self._earthTendency = 1.0
        else:
            self._fireTendency = elemental_tendency[0]
            self._waterTendency = elemental_tendency[1]
            self._airTendency = elemental_tendency[2]
            self._earthTendency = elemental_tendency[3]


    def changePower(self, mod):
        self._power = self._power * mod

    def changeTendency(self, type, mod):
        
        self._fireTendency -= (mod/3)
        self._waterTendency -= (mod/3)
        self._airTendency -= (mod/3)
        self._earthTendency -= (mod/3)
        if(type == enum_ElementalType.FIRE):
            self._fireTendency += (mod+(mod/3))
        elif(type == enum_ElementalType.WATER):
            self._waterTendency += (mod+(mod/3))
        elif(type == enum_ElementalType.AIR):
            self._airTendency += (mod+(mod/3))
        elif(type == enum_ElementalType.EARTH):
            self._earthTendency += (mod+(mod/3))

    def getPower(self):
        return self._power

    def getElementalTendency(self):
        return [self._fireTendency, self._waterTendency, self._airTendency, self._earthTendency]
    
    def getSpecificElementalTendency(self, type: enum_ElementalType):
        if(type == enum_ElementalType.FIRE):
            return self._fireTendency
        elif(type == enum_ElementalType.WATER):
            return self._waterTendency
        elif(type == enum_ElementalType.AIR):
            return self._airTendency
        else:
            return self._earthTendency
    
    def printDetails(self):
        print("Energy pulse with power: " + str(self._power) + " and elemental tendency: " + str(self._fireTendency) + ", "  + str(self._waterTendency)  + ", "  + str(self._airTendency)   + ", "  + str(self._earthTendency))

class SpellInfoPacket():
    def __init__(self, directDamage: float, max_targets: int):
        self._directDamage = directDamage
        self._max_targets = max_targets
        #print("Spell packet created: " + str(self._directDamage) + "," + str(self._multiTargDamage))

    @property
    def directDamage(self) -> float:
        return self._directDamage

    @property
    def max_targets(self) -> float:
        return self._max_targets

class SpellSimData():
    def __init__(self, timePeriod, maxTargets, oneTargDamage ):
        self._timePeriod = timePeriod
        self._maxTargets = maxTargets
        self._oneTargDamage = oneTargDamage    
        
    @property
    def timePeriod(self) -> float:
        return self._timePeriod

    @property
    def maxTargets(self) -> float:
        return self._maxTargets    
    
    @property
    def oneTargDamage(self) -> float:
        return self._oneTargDamage
