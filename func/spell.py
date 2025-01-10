
import random
from .helperFunc import *
from .nodeSuperTypes import *

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

        
        #FIRE ALL AUTOFIRING NODES
        for node in self._energy_nodes:
            
            if (node.is_autofire()==True):
                #node.print_self_details()
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
        

        #FIRE ALL TRIGGERED NODES WITH THE HIT EVENTS 
        for node in self._energy_nodes:
            if(not node.is_autofire()):
                #node.print_self_details()
                for hit_event_set in all_hit_event_sets:
                    #print(hit_event_set)
                    if(random.uniform(0, 1)<node.hit_to_trigger_rate()):
                        #castcount = math.floor(hit_event_set[0] * node.hit_to_trigger_rate())

                        for i in range(hit_event_set[0]):

                            #TO FIX/INVESTIGATE - ELEMENTAL EFFECTS NOT BEING PASSED INTO ONHIT TRIGGERS ETC 

                            triggeredfire_packet_list.extend(node.transmit_energy(EnergyPacket(hit_event_set[1])))


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


        #print("Tot Dir Dmg: " + str(totDirDmg) + ". Tot 3 targ: " + str(tot3targDmg)+ ". Tot 5 targ: " + str(tot5targDmg)+ ". Tot 10 targ: " + str(tot10targDmg))

        return SpellSimData(period, max_targets, totDirDmg)

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

