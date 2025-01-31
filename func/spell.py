
import random
from func.helperFunc import *
from func.nodeSuperTypes import *

class Spell():
    def __init__(self, spell_name: str, energy_nodes, count_nodes_incorporated: int = None):
        self._spell_name = spell_name
        if is_list_of_class(energy_nodes, EnergyNode):
            self._energy_nodes = energy_nodes
        self._count_nodes_incorporated = count_nodes_incorporated
    @property
    def spell_name(self) -> str:
        return self._spell_name
    
    @property
    def energy_nodes(self):
        return self._energy_nodes

    @property
    def count_nodes_incorporated(self):
        return self._count_nodes_incorporated
    
    #def simulate_time_period(self, period: float, max_targets: int):
    def simulate_time_period(self, period: float, verbose = False):
        autofire_packet_list = []

        
        #FIRE ALL AUTOFIRING NODES
        for node in self._energy_nodes:
            
            if (node.is_autofire()==True):
                #node.print_self_details()
                castcount = math.floor(period * node.ticks_per_second())

                for i in range(castcount):
                    autofire_packet_list.extend(node.transmit_energy())
        
        all_hit_event_sets = []

        triggeredfire_packet_list = []

        for packet in autofire_packet_list:
            #if packet.triggers_on_hits:
                #print("Triggered event firing")
            all_hit_event_sets.extend([[packet.max_targets, packet.directDamage/POWER_TO_DAMAGE, packet.triggers_on_hits]]) 


            #print("Generating hit event set with : " + str(min(packet.max_targets, max_targets)) + " targets and " + str(packet.directDamage) + " damage")
        

        #FIRE ALL TRIGGERED NODES WITH THE HIT EVENTS 
        for node in self._energy_nodes:
            if(not node.is_autofire()):
                #node.print_self_details()
                for hit_event_set in all_hit_event_sets:
                    #print(f"Hit event set: {hit_event_set} nodeName: {node.nodeName}, {node.triggers_with_all_hits}")

                    #Handling for only triggering if either its a node that triggers always (on deaths) or if its an event that triggers on hit events (non aoe nodes mainly)

                    if(random.uniform(0, 1)<node.hit_to_trigger_rate() and (node.triggers_with_all_hits or hit_event_set[2])):
                        for i in range(hit_event_set[0]):

                            triggeredfire_packet_list.extend(node.transmit_energy(EnergyPacket(hit_event_set[1])))


        totDirDmg = 0
        tot3targDmg = 0
        tot5targDmg = 0
        tot10targDmg = 0
        #print("Packet list: ")
        #print(packet_list)

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

        if(verbose):
            print(f"Tot Dir Dmg: {totDirDmg} Tot 3 targ: {tot3targDmg}. Tot 5 targ: {tot5targDmg} Tot 10 targ: {tot10targDmg}")

        return SpellSimData(self._spell_name, period, totDirDmg, tot3targDmg, tot5targDmg, tot10targDmg)

    def get_spell_xml(self):

        out = "<Spell: "+self._spell_name+">"
        for node in self._energy_nodes:
            out+="\n\t"
            out+=node.get_node_xml(2)
        
        out += "\n</Spell: "+self._spell_name+">"
        
        return out

    def get_spell_parentheses_not(self):
        out=f"Spell: {self._spell_name}"
        for node in self._energy_nodes:
            out+=f"({node.get_spell_parentheses_not()})"
        return out

