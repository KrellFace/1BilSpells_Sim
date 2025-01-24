import math
import random
from .nodeSuperTypes import *
from .packetTypes import *
from nodeTypes import *


def generate_node_pool():
    energyNodes = []
    energyNodes.append(WandCast("WandCastNorm"))
    energyNodes.append(OnHitNode("OnHitNode"))
    energyNodes.append(WandCastSmall("WandCastSmall"))
    energyNodes.append(OnDashStart("OnDashStart"))
    energyNodes.append(OnDashEnd("OnDashEnd"))
    energyNodes.append(OnHit("OnHitAll"))
    energyNodes.append(OnDeath("OnDeath"))
    energyNodes.append(OnManaCollect("OnManaCollect"))
    energyNodes.append(Lightning("Lightning"))
    energyNodes.append(OnHitHealthy("OnHitHealthy"))
    energyNodes.append(OnHitDamaged("OnHitDamaged"))

    modNodes = []
    modNodes.append(Accumulator("Accumulator"))
    modNodes.append(Splitter("SplitterBasic"))
    modNodes.append(Splitter45("Splitter45"))
    modNodes.append(FourStarSplitter("FourStarSplitter"))
    modNodes.append(EightStarSplitter("EightStarSplitter"))
    modNodes.append(Splitter345("Splitter345"))
    modNodes.append(SplitterParralel("SplitterParralel"))
    modNodes.append(Repeater2("Repeater2"))
    modNodes.append(Repeater3("Repeater3"))
    modNodes.append(Repeater5("Repeater5"))
    modNodes.append(Alternator2("Alternator2"))
    modNodes.append(Merger("DoubleMerger"))
    modNodes.append(TrippleMerger("TrippleMerger"))
    modNodes.append(Switch("Switch"))
    modNodes.append(Spliter22("Spliter22"))
    modNodes.append(RandomSplitter2("RandomSplitter2"))
    modNodes.append(RandomSplitter3("RandomSplitter3"))

    modNodes.append(StrongFireNode("StrongFireNode"))
    modNodes.append(StrongWaterNode("StrongWaterNode"))
    modNodes.append(StrongAirNode("StrongAirNode"))
    modNodes.append(StrongEarthNode("StrongEarthNode"))

    
    modNodes.append(Homing("Homing"))
    modNodes.append(Slow("Slow"))
    modNodes.append(Rotator10("Rotator10"))
    modNodes.append(Rotator45("Rotator45"))
    modNodes.append(TurnLeft("TurnLeft"))
    modNodes.append(TurnRight("TurnRight"))
    modNodes.append(RandomTurn("RandomTurn"))
    modNodes.append(SineMod("SineMod"))
    modNodes.append(AimAtClosest("AimAtClosest"))
    modNodes.append(Piercing("PiercingFirst"))
    modNodes.append(PiercingAll("PiercingAll"))

    damageNodes = []
    damageNodes.append(ProjectileNode("ProjectileNode"))
    damageNodes.append(ProjectileWithOutput("ProjectileWithOutput"))
    damageNodes.append(ExplosionNode("ExplosionNode"))
    damageNodes.append(SlashNode("SlashNode"))
    damageNodes.append(LaserNode("LaserNode"))
    damageNodes.append(LaserWithOutputNode("LaserWithOutputNode"))
    damageNodes.append(BalisticProjectileNode("BalisticProjectileNode"))
    damageNodes.append(BubbleNode("BubbleNode"))
    damageNodes.append(AreaNode("AreaNode"))
    damageNodes.append(CrystalNode("CrystalNode"))



    return [energyNodes, modNodes, damageNodes]

def select_x_nodes_from_pool(pool, x: int):
    out = []

    #Energy Nodes
    for i in range(x):
        #out.append(pool[random.randint(0, len(pool)-1)])
        out.append(pool[0][random.randint(0, len(pool[0])-1)].copy_node())
    #Mod Nodes
    for i in range(x):
        #out.append(pool[random.randint(0, len(pool)-1)])
        out.append(pool[1][random.randint(0, len(pool[1])-1)].copy_node())
    #Damage Nodes
    for i in range(x):
        #out.append(pool[random.randint(0, len(pool)-1)])
        out.append(pool[2][random.randint(0, len(pool[2])-1)].copy_node())

    return out

def generate_random_spell(input_nodes: list[SpellNode], spell_name: str):

    start_node = input_nodes.pop(random.randint(0, len(input_nodes)-1))
    start_node.nodeName = start_node.nodeName+  "-1"
    nodes_incorporated = [start_node]

    #print(f"Gen random spell from {len(input_nodes)} nodes")

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
            to_add.nodeName = to_add.nodeName + "-"+str(len(nodes_incorporated))
        else:
            failsafe+=1

            #TO FIX - READDING NODES TO THE SELECTABLE POOL IF THEY WERE NOT LINKABLE

            input_nodes.append(to_add)
            #print(f"Readding failed node {to_add.nodeName} to list")
    
    #print("Total nodes added: " + str(len(nodes_incorporated)))

    energy_nodes = []
    #print(f"Genereated spell with {len(nodes_incorporated)} nodes incorporated")
    for node in nodes_incorporated:
        if(node.nodeType ==enum_NodeType.ENERGY):
            energy_nodes.append(node)
    
    return Spell(spell_name, energy_nodes, len(nodes_incorporated))
            
