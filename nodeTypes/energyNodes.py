from func import *

class BasicCastNode(EnergyNode):
    def __init__(self, nodeName : str):
        super().__init__(nodeName, 1, 0.5, True)

class OnHitNode(EnergyNode):
    def __init__(self, nodeName: str):
        super().__init__(nodeName, None, None, False, input_power_mod=0.2, hit_to_trigger_rate=.2)

class WandCast(EnergyNode):
    def __init__(self, nodeName):
        super().__init__(nodeName, 1, 2, True)

class WandCastSmall(EnergyNode):
    def __init__(self, nodeName):
        super().__init__(nodeName, 0.5, 2, True)


#Assumes constant dashing - maybe not reasonable? Dashes take roughly 1 second to complete

class OnDashStart(EnergyNode):
    def __init__(self, nodeName):
        super().__init__(nodeName, 2, 1, True)

class OnDashEnd(EnergyNode):
    def __init__(self, nodeName):
        super().__init__(nodeName, 2, 1, True)

#Abstracting that ~ 20% of hits will result in a kill
class OnDeath(EnergyNode):
    def __init__(self, nodeName):
        super().__init__(nodeName, 0, 0, False, 1.5, 0.2, True)

#On hits use 40% of energy input in the live version
class OnHit(EnergyNode):
    def __init__(self, nodeName):
        super().__init__(nodeName, 0, 0, False, 0.4, 1)

#Basically an on death that only fires 50% of the time

class OnManaCollect(EnergyNode):
    def __init__(self, nodeName):
        super().__init__(nodeName, 0, 0, False,1, 0.1, True)

class Lightning(EnergyNode):
    def __init__(self, nodeName):
        super().__init__(nodeName, 3, 1/3, True)

#Hits on Damaged have to outweight hits on healthy by a factor of at least 2:1
#Hits on healthy do 50% of damage
#Hits on damaged do 20%

class OnHitHealthy(EnergyNode):
    def __init__(self, nodeName):
        super().__init__(nodeName, 0, 0, False,0.5, 0.7)

class OnHitDamaged(EnergyNode):
    def __init__(self, nodeName):
        super().__init__(nodeName, 0, 0, False,0.2, 0.3)

