import abc
import math
from abc import ABC, abstractmethod
from enum import Enum

CAST_RATE = 0.2
CAST_POWER = 1.0


class enum_NodeType(Enum):
    ENERGY= 1,
    MOD = 2,
    DMG = 3


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
        print("Setting name")
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
        print("Setting name")
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
    def __init__(self, nodeName: str, node_energy: float, power_rate: float):
        super().__init__(nodeName, enum_NodeType.ENERGY, 0, 1) #All Energy nodes have 0 inputs and 1 output
        self._node_energy = node_energy
        self._power_rate = power_rate
        self.setup_EnergyNode()
    

    #Overloading transmit energy to always use the nodes energy value
    def transmit_energy(self):
        packet_list = []
        for child in self._child_nodes:
            packet_list.extend(child.transmit_energy(self._node_energy))
        return packet_list

    def node_energy(self) -> float:
        return self._node_energy
    
    def power_rate(self) -> float:
        return self._power_rate
    
    
    @abstractmethod
    def setup_EnergyNode(self):
        pass

    def print_self_details(self):
        print(self._nodeName + " is an Energy node whcih produces ping of strength " + str(self._node_energy) + " every " + str(self._power_rate) + " seconds for " + str(self._max_child_nodes) + " output nodes")

class DamageNode(SpellNode):
    def __init__(self, nodeName: str, max_child_nodes: int, max_targets: int):
        super().__init__(nodeName, enum_NodeType.DMG, 1, max_child_nodes) #All Damage nodes have 1 inputs
        self._max_targets = max_targets


    def print_self_details(self):
        print(self._nodeName + " is a damage node that hits a maximum of " + str(self._max_targets) + " targets")

    #Overloading transmit energy to always use the nodes energy value
    def transmit_energy(self, energy: float):
        packet_list = []
        packet_list.append(self.generate_info_packet(energy))
        for child in self._child_nodes:
            packet_list.extend(child.transmit_energy(energy))
        #print("Dealing " + str(energy) + " damage to  " + str(self._max_targets) + " max target")
        return packet_list

    @abstractmethod
    def generate_info_packet(self, energy: float): 
        pass


class CastNode(EnergyNode):
    def __init__(self, nodeName : str):
        super().__init__(nodeName, CAST_RATE, CAST_POWER)

    def setup_EnergyNode(self):
        print("Cast node setting up")


class FireballNode(DamageNode):
    def __init__(self, nodeName : str):
        super().__init__(nodeName, 0, 1)
    
    def generate_info_packet(self, energy: float): 
        #print("Fireball node creating a spell packet:")
        return SpellInfoPacket(1*energy, 0)

class ChainingFireballNode(DamageNode):
    def __init__(self, nodeName : str):
        super().__init__(nodeName, 1, 1)
    
    def generate_info_packet(self, energy: float): 
        #print("Fireball node creating a spell packet:")
        return SpellInfoPacket(1*energy, 0)


class ExplosionNode(DamageNode):
    def __init__(self, nodeName : str):
        super().__init__(nodeName, 0, 1)
    
    def generate_info_packet(self, energy: float): 
        #print("Exp node creating a spell packet:")
        return SpellInfoPacket(1*energy, 1*energy)

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
    
    def simulate_time_period(self, period: float):
        packet_list = []
        for node in self._energy_nodes:
            castcount = math.floor(period / node.power_rate())
            #node.transmit_energy()
            for i in range(castcount):
                packet_list.extend(node.transmit_energy())

        totDirDmg = 0
        totaoeDmg = 0
        print("Packet list: ")
        print(packet_list)
        for packet in packet_list:
            totDirDmg+=packet.directDamage
            totaoeDmg+=packet.multiTargDamage

        print("Tot Dir Dmg: " + str(totDirDmg) + ". Tot AOE dmg: " + str(totaoeDmg))



class SpellInfoPacket():
    def __init__(self, directDamage: float, multiTargDamage: float):
        self._directDamage = directDamage
        self._multiTargDamage = multiTargDamage
        #print("Spell packet created: " + str(self._directDamage) + "," + str(self._multiTargDamage))

    @property
    def directDamage(self) -> float:
        return self._directDamage

    @property
    def multiTargDamage(self) -> float:
        return self._multiTargDamage
    
#Helper Functions

def is_list_of_class(input_data, cls):
    if isinstance(input_data, list):
        return all(isinstance(item, cls) for item in input_data)
    return False


    
# Usage
castNode1 = CastNode("Cast Node V1")
castNode2 = CastNode("Cast Node V2")
castNode3 = CastNode("Cast Node V3")
castNode3 = CastNode("Cast Node V4")
#castNode.print_self_details()

fireballNode = FireballNode("Fireball v1")
expNode = ExplosionNode("Explosion v1")
chainingFBNode = ChainingFireballNode("Chaining Ball V1")
fireballNode2 = FireballNode("Fireball v2")
#fireballNode.print_self_details()

castNode1.child_nodes = [fireballNode]
#castNode.print_self_details()
#fireballNode.print_self_details()

castNode2.child_nodes = [expNode]

chainingFBNode.child_nodes = [expNode]
castNode3.child_nodes = [chainingFBNode]






#test_spell = Spell("Fireball+Explosion", [castNode1, castNode2])
#test_spell.simulate_time_period(3)

test_chain = Spell("Chain", [castNode3])
test_chain.simulate_time_period(5)

test_non_Chain = Spell("Nonchain", [castNode1])
test_non_Chain.simulate_time_period(5)