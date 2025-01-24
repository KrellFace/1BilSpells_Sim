import math
from .configAndEnums import *
#from .spell import Spell

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
    
    def getSpecificElementalTendency(self, type: enum_ElementalType, mod =1):
        val = 0
        if(type == enum_ElementalType.FIRE):
            val = self._fireTendency
        elif(type == enum_ElementalType.WATER):
            val = self._waterTendency
        elif(type == enum_ElementalType.AIR):
            val = self._airTendency
        else:
            val = self._earthTendency
        return max(1 + (val-1)*mod, 0.1)
    
    def printDetails(self):
        print("Energy pulse with power: " + str(self._power) + " and elemental tendency: " + str(self._fireTendency) + ", "  + str(self._waterTendency)  + ", "  + str(self._airTendency)   + ", "  + str(self._earthTendency))

class SpellEffectPacket():
    def __init__(self, directDamage: float, max_targets: int, triggers_on_hits: bool):
        self._directDamage = directDamage
        self._max_targets = max_targets
        self._triggers_on_hits = triggers_on_hits
        #print("Spell packet created: " + str(self._directDamage) + "," + str(self._multiTargDamage))

    @property
    def directDamage(self) -> float:
        return self._directDamage

    @property
    def max_targets(self) -> float:
        return self._max_targets
    
    @property
    def triggers_on_hits(self) -> float:
        return self._triggers_on_hits

class SpellSimData():
    def __init__(self, spell_name, timePeriod, oneTargDamage, threeTargDamage, fiveTargDamage, tenTargDamage ):
        self._spellName = spell_name
        self._timePeriod = timePeriod
        self._oneTargDamage = oneTargDamage    
        self._threeTargDamage = threeTargDamage    
        self._fiveTargDamage = fiveTargDamage    
        self._tenTargDamage = tenTargDamage    
        
    @property
    def spell_name(self) -> float:
        return self._spellName
    
    @property
    def timePeriod(self) -> float:
        return self._timePeriod
    
    @property
    def oneTargDamage(self) -> float:
        return self._oneTargDamage
    @property
    def threeTargDamage(self) -> float:
        return self._threeTargDamage
    @property
    def fiveTargDamage(self) -> float:
        return self._fiveTargDamage
    @property
    def tenTargDamage(self) -> float:
        return self._tenTargDamage

class SpellProperties():

    def __init__(self, spellName: str, spellNodeTree: str, uniqueNodeCount: int, linearity: float, oneTDps: float, threeTDps: float, fiveTDps: float  , tenTDps: float):
        self._spellName = spellName
        self._spellNodeTree = spellNodeTree
        self._uniqueNodeCount = uniqueNodeCount
        self._linearity = linearity
        self._oneTDps = oneTDps
        self._threeTDps = threeTDps
        self._fiveTDps = fiveTDps
        self._tenTDps = tenTDps
    
    
    @property
    def spellName(self) -> float:
        return self._spellName
    @property
    def spellNodeTree(self) -> float:
        return self._spellNodeTree
    @property
    def uniqueNodeCount(self) -> float:
        return self._uniqueNodeCount
    @property
    def linearity(self) -> float:
        return self._linearity
    @property
    def oneTDps(self) -> float:
        return self._oneTDps
    @property
    def threeTDps(self) -> float:
        return self._threeTDps
    @property
    def fiveTDps(self) -> float:
        return self._fiveTDps
    @property
    def tenTDps(self) -> float:
        return self._tenTDps


    def print(self):
        print(f"Name: {self._spellName} Rep: {self._spellNodeTree} Node Count: {self._uniqueNodeCount} Linearity: {self._linearity} 1TargetDamage: {self._oneTDps}")

def get_damage_from_energypacket(energy_packet: EnergyPacket):
    fireDamageChange = max(1+(energy_packet.getSpecificElementalTendency(enum_ElementalType.FIRE)-1)*0.5, 0.1)
    return round(energy_packet.getPower()*fireDamageChange*POWER_TO_DAMAGE)