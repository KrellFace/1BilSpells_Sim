import abc
import math
import random
from abc import ABC, abstractmethod
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


class SpellNode(ABC):
    
    def __init__(self, nodeName: str, nodeType: enum_NodeType, max_parent_nodes: int, max_child_nodes: int):
        self._nodeName = nodeName
        self._nodeType = nodeType
        self._max_parent_nodes = max_parent_nodes
        self._max_child_nodes = max_child_nodes
        self._child_nodes = []

    @property
    def nodeName(self) -> str:
        return self._nodeName

    @property
    def nodeType(self) -> enum_NodeType:
        return self._nodeType

    #@nodeType.setter
    #@abstractmethod
    #def nodeType(self, value: enum_NodeType):
    #    self._nodeType = value

    
    @abstractmethod
    def transmit_energy(self, energy: float):
        #print("Transmitting energy in node " + self._nodeName)
        for child in self._child_nodes:
            child.transmit_energy(energy)

    #@abstractmethod
    #def receive_energy(self, energy: float):
    #    print("Receiving energy in node " + self._nodeName)

    @property
    def max_parent_nodes(self):
        return self._max_parent_nodes

    @property
    def parent_nodes(self):
        return self._parent_nodes
    
    # Setter
    @parent_nodes.setter
    def parent_nodes(self, value):
        #print("Setting name")
        if not is_list_of_class(value, SpellNode):
            raise ValueError("Parent nodes must be list of spell nodes")
        if not len(value) <= self._max_parent_nodes:
            raise ValueError("Parent nodes cannot exceed max set on node")
        self._parent_nodes = value


    @property
    def max_child_nodes(self):
        return self._max_child_nodes

    @property
    def child_nodes(self):
        return self._child_nodes

    # Setter
    @child_nodes.setter
    def child_nodes(self, value):
        #print("Setting name")
        if not is_list_of_class(value, SpellNode):
            raise ValueError("Child nodes must be list of spell nodes")
        if not len(value) <= self._max_child_nodes:
            raise ValueError("Child nodes cannot exceed max set on node")
        self._child_nodes = value

    @abstractmethod
    def print_self_details(self):
        pass


class EnergyNode(SpellNode):
    
    #def __init__(self, nodeType: NodeType):
    #    self._nodeType = nodeType
    def __init__(self, nodeName: str, node_power: float, ticks_per_second: float, is_autofire: bool, input_power_mod: float = None, hit_to_trigger_rate = None):
        super().__init__(nodeName, enum_NodeType.ENERGY, 0, 1) #All Energy nodes have 0 inputs and 1 output
        self._node_power = node_power
        self._ticks_per_second = ticks_per_second
        self._is_autoFire = is_autofire
        self._input_power_mod = input_power_mod
        self._hit_to_trigger_rate = hit_to_trigger_rate
        self.setup_EnergyNode()
    

    #Overloading transmit energy to always use the nodes energy value
    def transmit_energy(self, power_input = None):
        #print("Transmitting energy in node " + self._nodeName)
        packet_list = []
        for child in self._child_nodes:
            if(power_input == None and self._is_autoFire == False):
                print("Triggered energy node triggered with no power input")
            elif(self._is_autoFire == True):
                packet_list.extend(child.transmit_energy(self._node_power))
            else:
                #print("Transmiting energy in triggered node: " + str(power_input*self._input_power_mod))
                packet_list.extend(child.transmit_energy(power_input*self._input_power_mod))
        return packet_list

    def node_power(self) -> float:
        return self._node_power
    
    def ticks_per_second(self) -> float:
        return self._ticks_per_second
    
    def is_autofire(self) -> bool:
        return self._is_autoFire
    
    def input_power_mod(self) -> float:
        return self._input_power_mod
    
    def hit_to_trigger_rate(self) -> float:
        return self._hit_to_trigger_rate
    
    
    @abstractmethod
    def setup_EnergyNode(self):
        pass

    def print_self_details(self):
        if(self._is_autoFire):

            print(self._nodeName + " is an autofiring Energy node which produces ping of strength " + str(self._node_power) + " every " + str(self._ticks_per_second) + " seconds for " + str(self._max_child_nodes) + " output nodes")
        else:
            print(self._nodeName + " is an triggered Energy node with an power mod of " + str(self._input_power_mod) + " with " + str(self._max_child_nodes) + " output nodes")


class ModNode(SpellNode):
    def __init__(self, nodeName: str, max_parent_nodes: int, max_child_nodes: int, power_mod: float):
        super().__init__(nodeName, enum_NodeType.MOD, max_parent_nodes, max_child_nodes)
        self._power_mod = power_mod #All Damage nodes have 1 inputs

    def print_self_details(self):
        print(self._nodeName + " is a mod node with name " + self._nodeName + " with power mod " + str(self._power_mod))

    def transmit_energy(self, energy: float):
        #print("Transmitting energy in node " + self._nodeName)
        packet_list = []

        #TO DO - HANDLING FOR SPLITTING THE POWER BETWEEN OUTPUTS 

        for child in self._child_nodes:
            packet_list.extend(child.transmit_energy(energy*self._power_mod))
        #print("Dealing " + str(energy) + " damage to  " + str(self._aoe_radius) + " max target")
        return packet_list


class DamageNode(SpellNode):

    #I THINK WE WANT TO REPLACE MAX TARGETS WITH AOE SIZE - 0 MEANS SINGLE TARGET, AND THEN WE CAN USE A SEPERATE HEURISTIC TO CONVERT AOE RADIUS TO NUM ENEMIES HIT

    def __init__(self, nodeName: str, max_child_nodes: int, aoe_radius: int, power_mod: float):
        super().__init__(nodeName, enum_NodeType.DMG, 1, max_child_nodes) #All Damage nodes have 1 inputs
        self._aoe_radius = aoe_radius
        self._power_mod = power_mod


    def print_self_details(self):
        print(self._nodeName + " is a damage node with aoe size " + str(self._aoe_radius))

    def transmit_energy(self, energy: float):
        #print("Transmitting energy in node " + self._nodeName)
        packet_list = []
        self_packet = self.generate_info_packet(energy)
        if(self_packet.directDamage>MIN_DAMAGE_THRESHOLD):
            packet_list.append(self_packet)
        
        #packet_list.append(self.generate_info_packet(energy))
        for child in self._child_nodes:
            packet_list.extend(child.transmit_energy(energy))
        #print("Dealing " + str(energy) + " damage to  " + str(self._aoe_radius) + " max target")
        return packet_list

    @abstractmethod
    def generate_info_packet(self, energy: float): 
        pass

class StaticDamageNode(SpellNode):

    def __init__(self, nodeName: str, max_child_nodes: int, aoe_radius: int, ticks_per_power: int, power_mod: float):
        super().__init__(nodeName, enum_NodeType.STATIC, 1, max_child_nodes) #All Damage nodes have 1 inputs
        self._aoe_radius = aoe_radius
        self._ticks_per_power = ticks_per_power
        self._power_mod = power_mod


    def print_self_details(self):
        print(self._nodeName + " is a static damage node that ticks " + str(self.ticks_per_power) + " times for each power input")

    def transmit_energy(self, energy: float):
        #print("Transmitting energy in node " + self._nodeName)
        packet_list = []

        total_ticks = math.floor(energy*self._ticks_per_power)
        print("Total ticks == " + str(total_ticks) +" energy: " + str(energy) + " tpp: " + str(self._ticks_per_power))


        for x in range(total_ticks):
            packet_list.append(self.generate_info_packet(energy))
            for child in self._child_nodes:
                packet_list.extend(child.transmit_energy(energy*self._power_mod))
        #print("Dealing " + str(energy) + " damage to  " + str(self._aoe_radius) + " max target")
        return packet_list

    @abstractmethod
    def generate_info_packet(self, energy: float): 
        pass



class Spell():
    def __init__(self, spell_name: str, energy_nodes):
        self._spell_name = spell_name
        if is_list_of_class(energy_nodes, EnergyNode):
            self._energy_nodes = energy_nodes

    @property
    def spell_name(self) -> str:
        return self._spell_name
    
    @property
    def energy_nodes(self):
        return self._energy_nodes
    
    def simulate_time_period(self, period: float, max_targets: int):
        autofire_packet_list = []

        #WE NEED THIS TO ONLY FIRE ON AUTO FIRING ENERGY NODES

        for node in self._energy_nodes:
            
            if (node.is_autofire()==True):
                node.print_self_details()
                castcount = math.floor(period / node.ticks_per_second())
                #node.transmit_energy()

                #THIS DOES NOT WORK - ITS PINGING EVERY ENERGY NODE AT THE RATE OF THE FASTEST ONE
                #MAYBE WE CAN JUST DO THEM INDIVIDUALY 
                #WE ARE DOING THEN INDIVIDUALLY YOU ADORABLE DOLT <3

                for i in range(castcount):
                    autofire_packet_list.extend(node.transmit_energy())
        
        all_hit_event_sets = []

        triggeredfire_packet_list = []

        for packet in autofire_packet_list:
            all_hit_event_sets.extend([[min(packet.max_targets, max_targets), packet.directDamage]]) 
            #print("Generating hit event set with : " + str(min(packet.max_targets, max_targets)) + " targets and " + str(packet.directDamage) + " damage")
        
        for node in self._energy_nodes:
            if(not node.is_autofire()):
                node.print_self_details()
                for hit_event_set in all_hit_event_sets:
                    #print(hit_event_set)
                    if(random.uniform(0, 1)<node.hit_to_trigger_rate()):
                        #castcount = math.floor(hit_event_set[0] * node.hit_to_trigger_rate())

                        for i in range(hit_event_set[0]):
                            triggeredfire_packet_list.extend(node.transmit_energy(hit_event_set[1]))


        totDirDmg = 0
        tot3targDmg = 0
        tot5targDmg = 0
        tot10targDmg = 0
        #print("Packet list: ")
        #print(packet_list)

        #ITS IN THIS LOOP THAT WE SHOULD CALCULATE TRIGGERED EVENTS, BASED ON TARGETS HIT MODULATED BY A HEURISTIC
        #I.E VANILLA ON HIT EVENTS - TRIGGER FOR ALL HITS - HIT HEALTHY, ONLY 50% OF HITS ETC ETC
        #ADD ALL EVENTS TO A SEPERATE DICT OR SIMILAR STRUCTURE, THEN WE TRIGGER ALL EVENT BASED NODES
        #THEN REPEAT THAT PROCESS UNTIL NO NEW EVENTS 

        for packet in autofire_packet_list:
            totDirDmg+=packet.directDamage
            tot3targDmg+=(packet.directDamage * min(packet.max_targets, 3))
            tot5targDmg+=(packet.directDamage * min(packet.max_targets, 5))
            tot10targDmg+=(packet.directDamage * min(packet.max_targets, 10))

        

        for packet in triggeredfire_packet_list:
            totDirDmg+=packet.directDamage
            tot3targDmg+=(packet.directDamage * min(packet.max_targets, 3))
            tot5targDmg+=(packet.directDamage * min(packet.max_targets, 5))
            tot10targDmg+=(packet.directDamage * min(packet.max_targets, 10))


        print("Tot Dir Dmg: " + str(totDirDmg) + ". Tot 3 targ: " + str(tot3targDmg)+ ". Tot 5 targ: " + str(tot5targDmg)+ ". Tot 10 targ: " + str(tot10targDmg))



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
    
class EnergyPulse():
    def __init__(self, power: float):
        self._power = power
        self._fireTendency = 1.0
        self._waterTendency = 1.0
        self._airTendency = 1.0
        self._earthTendency = 1.0

    def changePower(self, mod):
        self._power = self._power * mod

    def changeTendency(self, mod, type):
        
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
    
    def printDetails(self):
        print("Energy pulse with power: " + str(self._power) + " and elemental tendency: " + str(self._fireTendency) + ", "  + str(self._waterTendency)  + ", "  + str(self._airTendency)   + ", "  + str(self._earthTendency))

    



    
#HELPER FUNCTIONS##---------------------------------------------------------------------
def is_list_of_class(input_data, cls):
    if isinstance(input_data, list):
        return all(isinstance(item, cls) for item in input_data)
    return False

def get_max_targets_for_aoe_radius(radius: float):
    area = math.pi * radius**2
    return max(math.floor(area*AREA_TO_TARGET_FACTOR),1)

#def mod_elemental_tendency(mod, arrayInt, input_vals):



#def calc_avg_packets_per_static(static_duration, time_simulated, ticks_per_second, casts_per_second):
#    max_packs_per_cast = static_duration * ticks_per_second
#    total_packets = (max_packs_per_cast *((time_simulated-static_duration+1)*casts_per_second)) + (((static_duration-1)*casts_per_second)*max_packs_per_cast/2)
#    packets_per_cast = 


#ACTUAL NODES# ----------------------------------------------------------------------------


#ENERGY NODES

class BasicCastNode(EnergyNode):
    def __init__(self, nodeName : str):
        super().__init__(nodeName, CAST_POWER, CAST_RATE, True)

    def setup_EnergyNode(self):
        #print("Cast node setting up")
        pass

class OnHitNode(EnergyNode):
    def __init__(self, nodeName: str):
        super().__init__(nodeName, None, None, False, input_power_mod=0.2, hit_to_trigger_rate=.2)

    def setup_EnergyNode(self):
        #print("Cast node setting up")
        pass

#MOD NODES

class Mod50Node(ModNode):
    def __init__(self, nodeName: str):
        super().__init__(nodeName, 1, 1, 1.5)

#DAMAGE NODES

class FireballNode(DamageNode):
    def __init__(self, nodeName : str):
        super().__init__(nodeName, 0, 1, 1)
    
    def generate_info_packet(self, energy: float): 
        #print("Fireball node creating a spell packet:")
        #print("Creating spell packet with damage: " + str(self._power_mod) + " x " + str(energy))
        return SpellInfoPacket(self._power_mod*energy, get_max_targets_for_aoe_radius(self._aoe_radius))

class ChainingFireballNode(DamageNode):
    def __init__(self, nodeName : str):
        super().__init__(nodeName, 1, 1, 1)
    
    def generate_info_packet(self, energy: float): 
        #print("Fireball node creating a spell packet:")
        return SpellInfoPacket(self._power_mod*energy, get_max_targets_for_aoe_radius(self._aoe_radius))


class ExplosionNode(DamageNode):
    def __init__(self, nodeName : str):
        super().__init__(nodeName, 0, 5, 1)
    
    def generate_info_packet(self, energy: float): 
        #print("Exp node creating a spell packet:")
        return SpellInfoPacket(self._power_mod*energy, get_max_targets_for_aoe_radius(self._aoe_radius))
    
class BigExplosionNode(DamageNode):
    def __init__(self, nodeName : str):
        super().__init__(nodeName, 0, 20, 1)
    
    def generate_info_packet(self, energy: float): 
        #print("Big Exp node creating a spell packet with max targets:"+ str(get_max_targets_for_aoe_radius(self._aoe_radius)))
        return SpellInfoPacket(self._power_mod*energy, get_max_targets_for_aoe_radius(self._aoe_radius))
    
#STATIC DAMAGE NODES

class AOENode(StaticDamageNode):
    def __init__(self, nodeName: str):
        super().__init__(nodeName, 0, 5, 2, 0.5)
    
    
    def generate_info_packet(self, energy: float): 
        #print("Exp node creating a spell packet:")
        return SpellInfoPacket(1*energy,get_max_targets_for_aoe_radius(self._aoe_radius))
    
# TESTING


BasicCastNode1 = BasicCastNode("Cast Node V1")
BasicCastNode2 = BasicCastNode("Cast Node V2")
aoeNode1 = AOENode("AOE Node 1")
mod50Node = Mod50Node("Mod 50 node")
basicFireball = FireballNode("Fireball1")
basicFireball2 = FireballNode("Fireball2")
expNode = ExplosionNode("Small one")
bigExpNode = BigExplosionNode("BigOne")

onHitNode = OnHitNode("OnHitTest")


#aoeSpell = Spell("AOE Spell", [BasicCastNode1])
#aoeSpell.simulate_time_period(5)

BasicCastNode1.child_nodes=[basicFireball]
unmodSpell = Spell("Basic fireball", [BasicCastNode1])
unmodSpell.simulate_time_period(5, 1)

#mod50Node.child_nodes=[bigExpNode]
#BasicCastNode2.child_nodes=[mod50Node]
#modSpell = Spell("Explosion",[BasicCastNode2])
#modSpell.simulate_time_period(5, 1)

onHitNode.child_nodes=[basicFireball2]
onHitSpell = Spell("On hit only", [BasicCastNode1,onHitNode])
onHitSpell.simulate_time_period(5, 1)


testPulse = EnergyPulse(3)

testPulse.printDetails()

testPulse.changePower(1.5)

testPulse.printDetails()

testPulse.changeTendency(.4, enum_ElementalType.FIRE )

testPulse.printDetails()
