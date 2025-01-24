from func import *

class BasicCastNode(EnergyNode):
    def __init__(self, nodeName : str):
        super().__init__(nodeName, 1, 0.5, True)

    #def setup_EnergyNode(self):
    #    print("Cast node setting up")
    #    pass

class OnHitNode(EnergyNode):
    def __init__(self, nodeName: str):
        super().__init__(nodeName, None, None, False, input_power_mod=0.2, hit_to_trigger_rate=.2)

class WandCast(EnergyNode):
    def __init__(self, nodeName):
        super().__init__(nodeName, 1, 2, True)

class WandCastSmall(EnergyNode):
    def __init__(self, nodeName):
        super().__init__(nodeName, 0.5, 2, True)


#Assumes constant dashing - maybe not reasonable? Dashes take roughly 0.3 seconds to complete
#Above was wrong, actual in game dash + cooldown is aorund 1 sec

class OnDashStart(EnergyNode):
    def __init__(self, nodeName):
        super().__init__(nodeName, 2, 1, True)

class OnDashEnd(EnergyNode):
    def __init__(self, nodeName):
        super().__init__(nodeName, 2, 1, True)

#Abstracting that ~ 20% of hits will result in a kill. Power of small butterfly is 1 and large is 1.5...lets go 1.5 for now
class OnDeath(EnergyNode):
    def __init__(self, nodeName):
        super().__init__(nodeName, 0, 0, False, 1.5, 0.2)

#On hits use 40% of energy input in the live version
class OnHit(EnergyNode):
    def __init__(self, nodeName):
        super().__init__(nodeName, 0, 0, False, 0.4, 1)

#Basically an on death that only fires 50% of the time
#i.e not v good lol

class OnManaCollect(EnergyNode):
    def __init__(self, nodeName):
        super().__init__(nodeName, 0, 0, False,1, 0.1)

class Lightning(EnergyNode):
    def __init__(self, nodeName):
        super().__init__(nodeName, 3, 1/3, True)

#Hits on Damaged have to outweight hits on healthy by a factor of at least 2:1
#Hits on healthy do 50% of damage
#Hits on damaged do 20% (This is way too low cause regular on hits do 40%)

class OnHitHealthy(EnergyNode):
    def __init__(self, nodeName):
        super().__init__(nodeName, 0, 0, False,0.5, 0.7)

class OnHitDamaged(EnergyNode):
    def __init__(self, nodeName):
        super().__init__(nodeName, 0, 0, False,0.2, 0.3)


    #def setup_EnergyNode(self):
    #    #print("Cast node setting up")
    #    pass