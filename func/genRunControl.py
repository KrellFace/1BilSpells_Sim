from .spellGen import *


class enum_SpellQualityHeuristic(Enum):
    NODES_INCORPED = 1,
    DPS = 2

def gen_best_spell(pool: list[SpellNode], spellName: str, attempts: int, heuristic: enum_SpellQualityHeuristic):

    bestSpell = None
    bestScore = None
    for i in range(attempts):
        spell, nodeCount = generate_random_spell(copy_node_list(pool), spellName)
        if(heuristic is enum_SpellQualityHeuristic.NODES_INCORPED):
            if bestScore is None or nodeCount>bestScore:
                bestSpell= spell
                bestScore = nodeCount
        
        elif(heuristic is enum_SpellQualityHeuristic.DPS):

            #TO DO - DECIDE ON SIM PERIOD, MAX TARGETS AND WHERE TO STORE

            simData = spell.simulate_time_period(5, 3)
            if bestScore is None or simData.oneTargDamage > bestScore:
                bestSpell= spell
                bestScore = simData.oneTargDamage
        
        clean_pool(pool)

    return bestSpell


def clean_pool(pool: list[SpellNode]):
    for node in pool:
        node.clear_family()