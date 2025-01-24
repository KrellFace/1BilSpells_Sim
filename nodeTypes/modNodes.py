from func import *

#FLOW MOD NODES

class Mod50Node(ModNode):
    def __init__(self, nodeName: str):
        super().__init__(nodeName, 1, 1, 1.5)

class TenChildren(ModNode):
    def __init__(self, nodeName):
        super().__init__(nodeName, 1, 10, 1)

class TenParents(ModNode):
    def __init__(self, nodeName):
        super().__init__(nodeName, 10, 1, 1)


class Accumulator(ModNode):
    def __init__(self, nodeName):
        super().__init__(nodeName, 1, 1, 1)

class Splitter(ModNode):
    def __init__(self, nodeName):
        super().__init__(nodeName, 1, 2, 1)

class Splitter45(ModNode):
    def __init__(self, nodeName):
        super().__init__(nodeName, 1, 1, 1, pulses_per_child=2)

class FourStarSplitter(ModNode):
    def __init__(self, nodeName):
        super().__init__(nodeName, 1, 1, 1, pulses_per_child=4)

class EightStarSplitter(ModNode):
    def __init__(self, nodeName):
        super().__init__(nodeName, 1, 1, 1, pulses_per_child=8)

class Splitter345(ModNode):
    def __init__(self, nodeName):
        super().__init__(nodeName, 1, 1, 1, pulses_per_child=3)

class SplitterParralel(ModNode):
    def __init__(self, nodeName):
        super().__init__(nodeName, 1, 1, 1, pulses_per_child=2)

class Repeater2(ModNode):
    def __init__(self, nodeName):
        super().__init__(nodeName, 1, 1, 1, pulses_per_child=2)

class Repeater3(ModNode):
    def __init__(self, nodeName):
        super().__init__(nodeName, 1, 1, 1, pulses_per_child=3)

class Repeater5(ModNode):
    def __init__(self, nodeName):
        super().__init__(nodeName, 1, 1, 1, pulses_per_child=5)

class Alternator2(ModNode):
    def __init__(self, nodeName):
        super().__init__(nodeName, 1, 2, 1)

class Merger(ModNode):
    def __init__(self, nodeName):
        super().__init__(nodeName, 2, 1, 1)

class TrippleMerger(ModNode):
    def __init__(self, nodeName):
        super().__init__(nodeName, 3, 1, 1)

class Switch(ModNode):
    def __init__(self, nodeName):
        super().__init__(nodeName, 1, 1, 1)

class Spliter22(ModNode):
    def __init__(self, nodeName):
        super().__init__(nodeName, 2, 2, 1)

class RandomSplitter2(ModNode):
    def __init__(self, nodeName):
        super().__init__(nodeName, 1, 2, 1)

class RandomSplitter3(ModNode):
    def __init__(self, nodeName):
        super().__init__(nodeName, 1, 3, 1)




#TO DO - ACCUMULATORS

class TimedAccumulator(ModNode):
    def __init__(self, nodeName):
        super().__init__(nodeName, 1, 1, 1)

class fiveSecCooldown(ModNode):
    def __init__(self, nodeName):
        super().__init__(nodeName, 1, 1, 0.5)

class tenSecCooldown(ModNode):
    def __init__(self, nodeName):
        super().__init__(nodeName, 1, 1, 0.5)

class accumulatorThree(ModNode):
    def __init__(self, nodeName):
        super().__init__(nodeName, 1, 1, 0.5)

#ELEMENTAL NODES

class WeakFireNode(ModNode):
    def __init__(self, nodeName):
        super().__init__(nodeName, 1, 1, 1, enum_ElementalType.FIRE, .4)

class StrongFireNode(ModNode):
    def __init__(self, nodeName):
        super().__init__(nodeName, 1, 1, 1, enum_ElementalType.FIRE, .8)

class WeakWaterNode(ModNode):
    def __init__(self, nodeName):
        super().__init__(nodeName, 1, 1, 1, enum_ElementalType.WATER, .4)

class StrongWaterNode(ModNode):
    def __init__(self, nodeName):
        super().__init__(nodeName, 1, 1, 1, enum_ElementalType.WATER, .8)

class WeakAirNode(ModNode):
    def __init__(self, nodeName):
        super().__init__(nodeName, 1, 1, 1, enum_ElementalType.AIR, .4)

class StrongAirNode(ModNode):
    def __init__(self, nodeName):
        super().__init__(nodeName, 1, 1, 1, enum_ElementalType.AIR, .8)
        
class WeakEarthNode(ModNode):
    def __init__(self, nodeName):
        super().__init__(nodeName, 1, 1, 1, enum_ElementalType.EARTH, .4)

class StrongEarthNode(ModNode):
    def __init__(self, nodeName):
        super().__init__(nodeName, 1, 1, 1, enum_ElementalType.EARTH, .8)

#Direction Modes


class Homing(ModNode):
    def __init__(self, nodeName):
        super().__init__(nodeName, 1, 1, 1)


class Slow(ModNode):
    def __init__(self, nodeName):
        super().__init__(nodeName, 1, 1, 1)


class Rotator10(ModNode):
    def __init__(self, nodeName):
        super().__init__(nodeName, 1, 1, 1.2)

class Rotator45(ModNode):
    def __init__(self, nodeName):
        super().__init__(nodeName, 1, 1, 1.4)


class TurnLeft(ModNode):
    def __init__(self, nodeName):
        super().__init__(nodeName, 1, 1, 1.2)


class TurnRight(ModNode):
    def __init__(self, nodeName):
        super().__init__(nodeName, 1, 1, 1.2)
    

class RandomTurn(ModNode):
    def __init__(self, nodeName):
        super().__init__(nodeName, 1, 1, 1.4)


class SineMod(ModNode):
    def __init__(self, nodeName):
        super().__init__(nodeName, 1, 1, 1.4)


class AimAtClosest(ModNode):
    def __init__(self, nodeName):
        super().__init__(nodeName, 1, 1, .5)


class Piercing(ModNode):
    def __init__(self, nodeName):
        super().__init__(nodeName, 1, 1, 1)


class PiercingAll(ModNode):
    def __init__(self, nodeName):
        super().__init__(nodeName, 1, 1, .8)
