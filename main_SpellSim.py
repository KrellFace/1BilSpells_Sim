import os
import sys
from func import *
from nodeTypes import *
    

#FULL SPELL GENERATION RUNS

NODES_PER_NODETYPE = 3
ATTEMPTS_PER_SPELL = 20
TOTAL_SPELLS = 100000
SPELL_SIM_LENGTH = 30
RUN_NAME = "FiguresOnly"

current_directory = os.path.dirname(os.path.abspath(__file__))
#Define the file path for the CSV
files_outpath = os.path.join(current_directory, "output", RUN_NAME)

os.makedirs(os.path.dirname(files_outpath), exist_ok=True)

#spell_properties = full_spell_generation_run(csv_file_path, TOTAL_SPELLS, enum_SpellQualityHeuristic.DPS, ATTEMPTS_PER_SPELL, NODES_PER_NODETYPE, SPELL_SIM_LENGTH)


#gen_all_figures(spell_properties, NODES_PER_NODETYPE*3,SPELL_SIM_LENGTH,csv_file_path)

gen_all_figures_from_csv(NODES_PER_NODETYPE*3,SPELL_SIM_LENGTH,"output/100Thousand_FullRun_data.csv", files_outpath)

#x = np.random.randn(100000) 
#y = np.random.randn(100000) 

#gen_heatmap(x, y,20, "xlabel", "ylabel", "funny title", csv_file_path+"_lol")