import math
import random
from .nodeSuperTypes import *
from .packetTypes import *
from nodeTypes import *


def generate_node_pool():
    out = []
    out.append(BasicCastNode("A1"))
    out.append(BasicCastNode("A2"))
    out.append(BasicCastNode("A3"))
    out.append(BasicCastNode("A4"))
    out.append(AOENode("B"))
    out.append(Mod50Node("C"))
    out.append(FireballNode("D"))
    out.append(ChainingFireballNode("E"))
    out.append(ExplosionNode("F"))
    out.append(BigExplosionNode("G"))
    out.append(NoDamageNode("H"))
    out.append(TenChildren("I"))
    out.append(TenParents("J"))
    out.append(OnHitNode("K"))
    out.append(StrongFireNode("L"))
    out.append(StrongWaterNode("M"))
    return out

def select_x_nodes_from_pool(pool: list[SpellNode], x: int):
    out = []
    for i in range(x):
        #out.append(pool[random.randint(0, len(pool)-1)])
        out.append(pool.pop(random.randint(0, len(pool)-1)))

    return out

def generate_random_spell(input_nodes: list[SpellNode], spell_name: str):

    start_node = input_nodes.pop(random.randint(0, len(input_nodes)-1))
    nodes_incorporated = [start_node]

    failsafe = 0
    while(len(input_nodes)>0 and failsafe < 100):
        to_add = input_nodes.pop(random.randint(0, len(input_nodes)-1))
        if(to_add==None):
            ValueError("Found no nodes remained in input, unexpectedly")
            break
        to_add_has_free_parent_slots = to_add.max_parent_nodes>0
        to_add_has_free_child_slots = to_add.max_child_nodes>0



        #If node to add could be attached anywhere, coin flip, else look only where relevant
        #Also note, if we only have free parent slots we must be added as a child and visa versa
        #to_add = None
        adding_as_parent = None
        if to_add_has_free_parent_slots and to_add_has_free_child_slots:
            if (random.random()>0.5):
                adding_as_parent = False
            else:
                adding_as_parent = True
        elif to_add_has_free_parent_slots:
            adding_as_parent = False
        elif to_add_has_free_child_slots:
            adding_as_parent = True

        #This check should never be needed, otherwise the node found does not allow children or parents
        node_to_add_to = None
        if(adding_as_parent is not None):
            #print("Free slots rightly found, now hunting for a mate")
            node_to_add_to = get_node_with_free_slot(nodes_incorporated, adding_as_parent)

        if(node_to_add_to is not None):
            #print("Found linkable nodes")
            #print(f"Toadd {to_add.nodeName}: Parent nodes available: {len(to_add.parent_nodes)}/{to_add.max_parent_nodes}. ChildNodes available:{len(to_add.child_nodes)}/{to_add.max_child_nodes}")
            
            #print(f"node_to_add_to {node_to_add_to.nodeName}: Parent nodes available: {len(node_to_add_to.parent_nodes)}/{node_to_add_to.max_parent_nodes}. ChildNodes available:{len(node_to_add_to.child_nodes)}/{node_to_add_to.max_child_nodes}")
            if adding_as_parent:
                link_nodes(to_add, node_to_add_to)
            else:
                link_nodes(node_to_add_to, to_add)
            nodes_incorporated.append(to_add)
        else:
            failsafe+=1

            #TO FIX - READDING NODES TO THE SELECTABLE POOL IF THEY WERE NOT LINKABLE

            input_nodes.append(to_add)
            #print(f"Readding failed node {to_add.nodeName} to list")
    
    #print("Total nodes added: " + str(len(nodes_incorporated)))

    energy_nodes = []
    for node in nodes_incorporated:
        if(node.nodeType ==enum_NodeType.ENERGY):
            energy_nodes.append(node)
    
    return Spell(spell_name, energy_nodes),len(nodes_incorporated)
            
