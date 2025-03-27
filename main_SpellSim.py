import os
import sys
from func import *
from nodeTypes import *
    

#FULL SPELL GENERATION RUNS

NODES_PER_NODETYPE = 5
ATTEMPTS_PER_SPELL = 20
TOTAL_SPELLS = 1000
SPELL_SIM_LENGTH = 30
RUN_NAME = "NEW_HEATMAP"

current_directory = os.path.dirname(os.path.abspath(__file__))
#Define the file path for the CSV
files_outpath = os.path.join(current_directory, "output", RUN_NAME)

os.makedirs(os.path.dirname(files_outpath), exist_ok=True)

#spell_properties = full_spell_generation_run(files_outpath, TOTAL_SPELLS, enum_SpellQualityHeuristic.DPS, ATTEMPTS_PER_SPELL, NODES_PER_NODETYPE, SPELL_SIM_LENGTH)


#gen_all_figures(spell_properties, 8,SPELL_SIM_LENGTH,files_outpath)

gen_all_figures_from_csv(9,SPELL_SIM_LENGTH,"output/1HundredThousandSpells-30 SecondSim_data.csv", files_outpath)