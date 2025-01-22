from abc import ABC, abstractmethod
from .configAndEnums import *
from .helperFunc import *
from .packetTypes import *

class SpellNode(ABC):
    
    def __init__(self, nodeName: str, nodeType: enum_NodeType, max_parent_nodes: int, max_child_nodes: int):
        self._nodeName = nodeName
        self._nodeType = nodeType
        self._max_parent_nodes = max_parent_nodes
        self._max_child_nodes = max_child_nodes
        self._child_nodes = []
        self._parent_nodes = []

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
    def transmit_energy(self, energy_packet: EnergyPacket):
        #print("Transmitting energy in node " + self._nodeName)
        for child in self._child_nodes:
            child.transmit_energy(energy_packet)

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

    def get_node_xml(self, depth: int):
        out = ""
        if len(self._child_nodes)>0:
            out = "<"+self._nodeName+">"
            #out+="\n\t"
            for node in self._child_nodes:
                out+="\n"
                for x in range(depth):
                    out+="\t"
                out+=node.get_node_xml(depth+1)
            
            out+="\n"
            for x in range(depth-1):
                out+="\t"
            out+="</"+self._nodeName+">"
        else:
            out = "<"+self._nodeName+" />"
        return out

    def get_spell_parentheses_not(self):
        out=self._nodeName
        if len(self._child_nodes)>0:
            for node in self._child_nodes:
                out+=f"({node.get_spell_parentheses_not()})"
        return out

    def has_free_slot(self, checking_parent_spaces: bool):
        out = False
        if checking_parent_spaces and self._max_parent_nodes>len(self._parent_nodes):
            out = True
        elif not checking_parent_spaces and self._max_child_nodes>len(self._child_nodes):
            out = True
        return out


    
    def clear_family(self):
        self._child_nodes = []
        self._parent_nodes = []

    @abstractmethod
    def copy_node(self):
        return SpellNode(self._nodeName, self._nodeType, self._max_parent_nodes, self._max_child_nodes, self._child_nodes,self._parent_nodes)



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
        #self.setup_EnergyNode()
    

    #Overloading transmit energy to always use the nodes energy value
    def transmit_energy(self, energy_packet = None):
        #print("Transmitting energy in node " + self._nodeName)
        packet_list = []
        for child in self._child_nodes:
            if(energy_packet == None and self._is_autoFire == False):
                print("Triggered energy node triggered with no power input")
            elif(self._is_autoFire == True):
                packet_list.extend(child.transmit_energy(EnergyPacket(self._node_power)))
                print(f"Transmitting : {self._node_power} in {self._nodeName}")
            else:
                #print("Transmiting energy in triggered node: " + str(energy_packet.getPower()*self._input_power_mod))
                packet_list.extend(child.transmit_energy(EnergyPacket(self._input_power_mod*energy_packet.getPower())))
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
    
    
    #@abstractmethod
    #def setup_EnergyNode(self):
    #    pass

    def copy_node(self):
        #return EnergyNode(self._nodeName, self._nodeType, self._max_parent_nodes, self._max_child_nodes, self._child_nodes,self._parent_nodes)
        return EnergyNode(self._nodeName, self._node_power, self._ticks_per_second, self._is_autoFire, self._input_power_mod, self._hit_to_trigger_rate)

    def print_self_details(self):
        if(self._is_autoFire):

            print(self._nodeName + " is an autofiring Energy node which produces ping of strength " + str(self._node_power) + " every " + str(self._ticks_per_second) + " seconds for " + str(self._max_child_nodes) + " output nodes")
        else:
            print(self._nodeName + " is an triggered Energy node with an power mod of " + str(self._input_power_mod) + " with " + str(self._max_child_nodes) + " output nodes")

class ModNode(SpellNode):
    def __init__(self, nodeName: str, max_parent_nodes: int, max_child_nodes: int, power_mod: float, elemental_type: enum_ElementalType = None, elemental_mod: float = None, pulses_per_child = 1):
        super().__init__(nodeName, enum_NodeType.MOD, max_parent_nodes, max_child_nodes)
        self._power_mod = power_mod #All Damage nodes have 1 inputs
        self._elemental_type = elemental_type
        self._elemental_mod = elemental_mod
        self._pulses_per_child = pulses_per_child

    def print_self_details(self):
        print(self._nodeName + " is a mod node with name " + self._nodeName + " with power mod " + str(self._power_mod))

    def transmit_energy(self, energy_packet: EnergyPacket):
        #print("Transmitting energy in node " + self._nodeName)
        packet_list = []

        #TO DO - HANDLING FOR DIFFERENT SPLITTING TYPES OF THE POWER BETWEEN OUTPUTS 
        if len(self._child_nodes)>0:
            out_packet = EnergyPacket((energy_packet.getPower()*self._power_mod)/(len(self._child_nodes)*self._pulses_per_child), energy_packet.getElementalTendency())
            if(self._elemental_type!=None):
                out_packet.changeTendency(self._elemental_type, self._elemental_mod)
            for child in self._child_nodes:
                packet_list.extend(child.transmit_energy(out_packet))
            #print("Dealing " + str(energy) + " damage to  " + str(self._aoe_radius) + " max target")
            return packet_list
        else:
            return []
    
    
    def copy_node(self):
        return ModNode(self._nodeName, self._max_parent_nodes, self._max_child_nodes, self._power_mod, self._elemental_type, self._elemental_mod)


class DamageNode(SpellNode):

    def __init__(self, nodeName: str, max_child_nodes: int, aoe_radius: int, power_mod: float, damage_compensating = False, damage_comp_amnt = 0.8):
        super().__init__(nodeName, enum_NodeType.DMG, 1, max_child_nodes) #All Damage nodes have 1 inputs
        self._aoe_radius = aoe_radius
        self._power_mod = power_mod
        self._damage_compensating = damage_compensating
        self._damage_comp_amnt = damage_comp_amnt


    def print_self_details(self):
        print(self._nodeName + " is a damage node with aoe size " + str(self._aoe_radius))

    def transmit_energy(self, energy_packet: EnergyPacket):
        #print("Transmitting energy in node " + self._nodeName)
        packet_list = []

        power = energy_packet.getPower()
        print(f"Input power {energy_packet.getPower()} to node {self._nodeName}")
        if(self._damage_compensating and power>1):
            power = lerp(power, 1, self._damage_comp_amnt)
            print(f"Lerped power {power} to node {self._nodeName}")
        power *= self._power_mod
        print(f"Adjusted power {power} to node {self._nodeName}")

        #ONLY CHILDREN IF POWER IS HIGH ENOUGH
        transmitting_to_children = True
        if(power<MIN_POWER_THRESHOLD):
            power=0.1
            transmitting_to_children=False

        adjusted_energy_packet = EnergyPacket(power, energy_packet.getElementalTendency())

        self_packet = self.generate_spelleffect_packet(adjusted_energy_packet)
        packet_list.append(self_packet)

        if(transmitting_to_children):
            #packet_list.append(self_packet)
        
            #outPacket = EnergyPacket(energy_packet.getPower()*self._power_mod, energy_packet.getElementalTendency())
            for child in self._child_nodes:
                
                packet_list.extend(child.transmit_energy(adjusted_energy_packet))
        print("Dealing " + str(self_packet.directDamage) + " damage to  " + str(self._aoe_radius) + " max target")
        return packet_list

    #@abstractmethod
    def generate_spelleffect_packet(self, energy_packet: EnergyPacket): 


        return SpellEffectPacket(get_damage_from_energypacket(energy_packet), get_max_targets_for_aoe_radius(self._aoe_radius))
    
    
    def copy_node(self):
        #return DamageNode(self._nodeName, self._nodeType, self._max_parent_nodes, self._max_child_nodes, self._child_nodes,self._parent_nodes)
        return DamageNode(self._nodeName, self._max_child_nodes, self._aoe_radius, self._power_mod, self._damage_compensating, self._damage_comp_amnt)

class StaticDamageNode(SpellNode):

    def __init__(self, nodeName: str, max_child_nodes: int, base_aoe_radius: int, ticks_per_second: int, power_mod: float, duration_comp_amnt: float, earth_duration_bonus: float, damage_compensating: bool = False, damage_comp_amnt:float = 0.8):
        super().__init__(nodeName, enum_NodeType.STATIC, 1, max_child_nodes) #All Damage nodes have 1 inputs
        self._base_aoe_radius = base_aoe_radius
        self._ticks_per_second = ticks_per_second
        self._power_mod = power_mod
        self._duration_comp_amnt = duration_comp_amnt
        self._earth_duration_bonus = earth_duration_bonus
        self._damage_compensating = damage_compensating
        self._damage_comp_amnt = damage_comp_amnt


    def print_self_details(self):
        print(self._nodeName + " is a static damage node that ticks " + str(self.ticks_per_power) + " times for each power input")

    @abstractmethod
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

        out_packet = EnergyPacket(power_per_hit, energy_packet.getElementalTendency())

        print("Total ticks == " + str(total_ticks) +" energy packet power: " + str(power_per_hit))

        for x in range(total_ticks):
            packet_list.append(self.generate_info_packet(out_packet))
            for child in self._child_nodes:
                packet_list.extend(child.transmit_energy(out_packet))
        #print("Dealing " + str(energy) + " damage to  " + str(self._aoe_radius) + " max target")
        return packet_list

    #@abstractmethod
    def generate_info_packet(self, energy_packet: EnergyPacket): 
        #print("Fireball node creating a spell packet:")
        #print("Creating spell packet with damage: " + str(self._power_mod) + " x " + str(energy))
        #return SpellInfoPacket(self._power_mod*energy_packet.getPower()*energy_packet.getSpecificElementalTendency(enum_ElementalType.FIRE), get_max_targets_for_aoe_radius(self._aoe_radius))
        return SpellEffectPacket(get_damage_from_energypacket(energy_packet), get_max_targets_for_aoe_radius(self._base_aoe_radius))
    
    
    def copy_node(self):
        return StaticDamageNode(self._nodeName, self._max_child_nodes, self._base_aoe_radius, self._ticks_per_second, self._power_mod)
