import math
import random
#from func.nodeSuperTypes import *
from func.configAndEnums import *

def is_list_of_class(input_data, cls):
    if isinstance(input_data, list):
        return all(isinstance(item, cls) for item in input_data)
    return False

def get_max_targets_for_aoe_radius(radius: float):
    area = math.pi * radius**2
    return max(math.floor(area*AREA_TO_TARGET_FACTOR),1)

def get_node_with_free_slot(nodes_to_check, looking_for_parent_slot):
    out = None
    #print("Checking set of nodes, first node in list: " + nodes_to_check[0].nodeName + " and LFP: " + str(looking_for_parent_slot))
    for x in range(10):
        #print("Looping")
        node_to_check = nodes_to_check[random.randint(0, len(nodes_to_check)-1)]
        #print("Checking node: " + node_to_check.nodeName)
        #print(f"Parent nodes available: {len(node_to_check.parent_nodes)}/{node_to_check.max_parent_nodes}. ChildNodes available:{len(node_to_check.child_nodes)}/{node_to_check.max_child_nodes}")
        if ((looking_for_parent_slot and node_to_check.max_parent_nodes > len(node_to_check.parent_nodes))) or (not looking_for_parent_slot and node_to_check.max_child_nodes > len(node_to_check.child_nodes)):
            #print("Found node to link")
            out = node_to_check
            break
    
    return out

def check_if_link_viable(parent, child):
    out = True
    
    if(len(parent.child_nodes))>=parent.max_child_nodes:
        out = False
    elif (len(child.parent_nodes))>=child.max_parent_nodes:
        out = False
    
    return out

def link_nodes(parent, child):
    if(len(parent.child_nodes))>=parent.max_child_nodes:
        raise ValueError("Parent has too many children")
    elif (len(child.parent_nodes))>=child.max_parent_nodes:
        raise ValueError("Child has too many parents")
    else:
        parent.child_nodes.append(child)
        child.parent_nodes.append(parent)

def copy_node_list(toCopy):
    out = []
    for node in toCopy:
        out.append(node.copy_node())
    return out

def lerp(a, b, t):
    return a + (b - a) * t