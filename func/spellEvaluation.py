from func.spell import Spell
from func.nodeSuperTypes import SpellNode
from func.packetTypes import SpellProperties

def genSpellProperties(spell: Spell, simTime: int):
    simData = spell.simulate_time_period(simTime)

    spellRep = spell.get_spell_parentheses_not()

    energy_nodes = spell.energy_nodes
    #nodes_incorporated = set()
    #for node in energy_nodes:
     #   nodes_incorporated.update(recursively_get_child_nodes(node))

    maxChain = 0
    for node in energy_nodes:
        val = recursively_get_longest_chainlength(node, 0)
        if val > maxChain:
            maxChain = val

    #count_nodes = len(nodes_incorporated)
    count_nodes = spell.count_nodes_incorporated
    #branching_factor = count_nodes -spellRep.count(")(") / count_nodes
    #branching_factor = spellRep.count(")(")
    branching_factor = round(maxChain/count_nodes,2)


    simData= spell.simulate_time_period(simTime)
    
    #for val in nodes_incorporated:
    #    print(str(val))

    return SpellProperties(spell.spell_name, spellRep, count_nodes,branching_factor, simData.oneTargDamage, simData.threeTargDamage, simData.fiveTargDamage, simData.tenTargDamage)



def recursively_get_child_nodes(node: SpellNode):
    out = set(node.nodeName)
    for child in node.child_nodes:
        out.update(recursively_get_child_nodes(child))


    return out

def recursively_get_longest_chainlength(node: SpellNode, parentChainlength: int):
    chainLength=parentChainlength+1
    maxChildLength = chainLength
    for child in node.child_nodes:
        val = recursively_get_longest_chainlength(child, chainLength)
        if val >maxChildLength:
            maxChildLength = val
    return maxChildLength


