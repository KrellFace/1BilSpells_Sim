from func import *

class BasicCastNode(EnergyNode):
    def __init__(self, nodeName : str):
        super().__init__(nodeName, CAST_POWER, CAST_RATE, True)

    #def setup_EnergyNode(self):
    #    print("Cast node setting up")
    #    pass

class OnHitNode(EnergyNode):
    def __init__(self, nodeName: str):
        super().__init__(nodeName, None, None, False, input_power_mod=0.2, hit_to_trigger_rate=.2)

    #def setup_EnergyNode(self):
    #    #print("Cast node setting up")
    #    pass