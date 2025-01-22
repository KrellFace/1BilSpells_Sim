from .spellGen import *
from .spellEvaluation import genSpellProperties
from func.outputGen import *


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

            simData = spell.simulate_time_period(5)
            if bestScore is None or simData.oneTargDamage > bestScore:
                bestSpell= spell
                bestScore = simData.oneTargDamage
        
        clean_pool(pool)

    return bestSpell


def clean_pool(pool: list[SpellNode]):
    for node in pool:
        node.clear_family()


def full_spell_generation_run(out_path, spells_to_gen: int, qual_heuristic: enum_SpellQualityHeuristic, attempts_per_set: int, pool_size_per_spell: int):

    overall_pool = generate_node_pool()

    #TO DO - OUTPUT OVERALL POOL AS CSV

    spell_properties = []

    for i in range(spells_to_gen):

        selected_pool = select_x_nodes_from_pool(copy_node_list(overall_pool), pool_size_per_spell)

        sp = gen_best_spell(selected_pool, f"Spell {i}", attempts_per_set, qual_heuristic)

        spell_properties.append(genSpellProperties(sp, 5))
    
    gen_csv_from_spellsdata(spell_properties, out_path)
    

