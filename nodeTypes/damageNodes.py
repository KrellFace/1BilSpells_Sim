from func import *

class FireballNode(DamageNode):
    def __init__(self, nodeName : str):
        super().__init__(nodeName, 0, 1, 1)
    
class ChainingFireballNode(DamageNode):
    def __init__(self, nodeName : str):
        super().__init__(nodeName, 1, 1, 1)
    
class ExplosionNode(DamageNode):
    def __init__(self, nodeName : str):
        super().__init__(nodeName, 0, 5, 1)
    
class BigExplosionNode(DamageNode):
    def __init__(self, nodeName : str):
        super().__init__(nodeName, 0, 20, 1)
    
class NoDamageNode(DamageNode):
    def __init__(self, nodeName):
        super().__init__(nodeName, 0, 0, 0)
#STATIC DAMAGE NODES

class AOENode(StaticDamageNode):
    def __init__(self, nodeName: str):
        super().__init__(nodeName, 0, 5, 2, 0.5)
    