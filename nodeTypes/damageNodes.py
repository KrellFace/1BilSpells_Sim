from func import *

#TESTING ONES

class ProjectileNode(DamageNode):
    def __init__(self, nodeName : str):
        super().__init__(nodeName, 0, 1, 1)
    
class ProjectileWithOutput(DamageNode):
    def __init__(self, nodeName : str):
        super().__init__(nodeName, 1, 1, 1)
    
class ExplosionNode(DamageNode):
    def __init__(self, nodeName : str):
        super().__init__(nodeName, 0, 3, 0.3,damage_compensating=True, triggers_on_hits=False, damage_comp_amnt=0.2)

class SlashNode(DamageNode):
    def __init__(self, nodeName : str):
        super().__init__(nodeName, 0, 3, 0.3,damage_compensating=True, triggers_on_hits=False)

class LaserNode(DamageNode):
    def __init__(self, nodeName : str):
        super().__init__(nodeName, 0, 2, .8)

class LaserWithOutputNode(DamageNode):
    def __init__(self, nodeName : str):
        super().__init__(nodeName, 0, 2, .8)

class BalisticProjectileNode(DamageNode):
    def __init__(self, nodeName : str):
        super().__init__(nodeName, 0, 1, 1)

class BubbleNode(DamageNode):
    def __init__(self, nodeName : str):
        super().__init__(nodeName, 0, 1, .5)
    
class NoDamageNode(DamageNode):
    def __init__(self, nodeName):
        super().__init__(nodeName, 0, 0, 0)

#STATIC DAMAGE NODES

class AreaNode(StaticDamageNode):

    #Note - the duration compensation amount is different here than it appears in the actual code (SpellArea.cs line 83). The value here of 0.4 seems to line up well with reality in game though

    def __init__(self, nodeName: str):
        super().__init__(nodeName, 0, 3, 3, 0.1, 0.4, .5, True, 0.2)
    
    def transmit_energy(self, energy_packet: EnergyPacket):
        #print("Transmitting energy in node " + self._nodeName)
        packet_list = []

        #print(f"Packet power: {energy_packet.getPower()} Dur compt amt: {self._duration_comp_amnt}, packet e bonus and duration bonus: {energy_packet.getSpecificElementalTendency(enum_ElementalType.EARTH, self._earth_duration_bonus)}")
        #print(f"Lerped power: {lerp(energy_packet.getPower(), 1, self._duration_comp_amnt)}")


        duration = lerp(energy_packet.getPower(), 1, self._duration_comp_amnt) * 3 * (energy_packet.getSpecificElementalTendency(enum_ElementalType.EARTH, self._earth_duration_bonus))

        #print(f"Duration of node: {self._nodeName} is {duration}")

        #total_ticks = math.floor(energy_packet.getPower()*self._ticks_per_second*energy_packet.getSpecificElementalTendency(enum_ElementalType.EARTH))
        total_ticks = math.floor(duration * self._ticks_per_second)
        
        tot_power = energy_packet.getPower()
        if(self._damage_compensating):
            tot_power = lerp(tot_power, 1, self._damage_comp_amnt)



        #power_per_hit = (tot_power*self._power_mod)/total_ticks

        #Note: Unlike crystals - Areas do not divide input power by number of hits they are doing to do

        power_per_hit = tot_power*self._power_mod

        
        #print(f"Power per hit pre adjustment: {power_per_hit}")

        transmitting_to_children = True
        if(power_per_hit<MIN_POWER_THRESHOLD):
            power_per_hit=0.1
            transmitting_to_children=False

        out_packet = EnergyPacket(power_per_hit, energy_packet.getElementalTendency())

        #print("Total ticks == " + str(total_ticks) +" power per hit: " + str(power_per_hit))

        for x in range(total_ticks):
            packet_list.append(self.generate_info_packet(out_packet))
            if transmitting_to_children:
                for child in self._child_nodes:
                    packet_list.extend(child.transmit_energy(out_packet))
        #print("Dealing " + str(energy) + " damage to  " + str(self._aoe_radius) + " max target")
        return packet_list

    #To fix: Having to add copy node to both areas and crystals to support copying a node with an abstract method
    def copy_node(self):
        return AreaNode(self._nodeName)


class CrystalNode(StaticDamageNode):
    def __init__(self, nodeName: str):
        super().__init__(nodeName, 1, 0, 5, .8, 0.5, 2, False)
    
    def transmit_energy(self, energy_packet: EnergyPacket):
        #print("Transmitting energy in node " + self._nodeName)
        packet_list = []

        duration = lerp(energy_packet.getPower(), 1, self._duration_comp_amnt) * (energy_packet.getSpecificElementalTendency(enum_ElementalType.EARTH)*self._earth_duration_bonus)

        #total_ticks = math.floor(energy_packet.getPower()*self._ticks_per_second*energy_packet.getSpecificElementalTendency(enum_ElementalType.EARTH))
        total_ticks = math.floor(duration * self._ticks_per_second)
        
        tot_power = energy_packet.getPower()
        if(self._damage_compensating):
            tot_power = lerp(tot_power, 1, self._damage_comp_amnt)


        power_per_hit = (tot_power*self._power_mod)/total_ticks

        adjusted_tick_interval = 1/self._ticks_per_second

        #Force a minimum of 0.5 damage per pulse, and force the gap between ticks to adjust for this

        while(power_per_hit <0.4 and total_ticks > 1):
            adjusted_tick_interval+=0.2
            total_ticks = math.floor(duration/adjusted_tick_interval)
            power_per_hit = (tot_power*self._power_mod)/total_ticks

        out_packet = EnergyPacket(power_per_hit, energy_packet.getElementalTendency())

        #print("Total ticks == " + str(total_ticks) +" energy packet power: " + str(power_per_hit))

        for x in range(total_ticks):

            #Dont add a self packet - because crystals dont produce damage

            #packet_list.append(self.generate_info_packet(out_packet))
            for child in self._child_nodes:
                packet_list.extend(child.transmit_energy(out_packet))
        #print("Dealing " + str(energy) + " damage to  " + str(self._aoe_radius) + " max target")
        return packet_list
    
    
    def copy_node(self):
        return CrystalNode(self._nodeName)

    