from func import *

#MOD NODES

class Mod50Node(ModNode):
    def __init__(self, nodeName: str):
        super().__init__(nodeName, 1, 1, 1.5)

class TenChildren(ModNode):
    def __init__(self, nodeName):
        super().__init__(nodeName, 1, 10, 1)

class TenParents(ModNode):
    def __init__(self, nodeName):
        super().__init__(nodeName, 10, 1, 1)


#ELEMENTAL NODES

class StrongFireNode(ModNode):
    def __init__(self, nodeName):
        super().__init__(nodeName, 1, 1, 1, enum_ElementalType.FIRE, .5)

class StrongWaterNode(ModNode):
    def __init__(self, nodeName):
        super().__init__(nodeName, 1, 1, 1, enum_ElementalType.WATER, .5)