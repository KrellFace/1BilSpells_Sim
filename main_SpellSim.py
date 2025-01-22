import os
import sys
from func import *
from nodeTypes import *
    
# TESTING

print(f"getcwd:{os.getcwd()}")
print(f"sys.path:{sys.path}")

basicCastNode1 = BasicCastNode("Cast Node V1")
basicCastNode2 = BasicCastNode("Cast Node V2")
basicCastNode3 = BasicCastNode("Cast Node V3")
wand1 = WandCast("Wand")
dash1 = OnDashEnd("Dash1")
light1 = Lightning("L1")
exp1 = ExplosionNode("Exp1")
aoeNode1 = AreaNode("AOE Node 1")
basicFireball = ProjectileNode("Fireball1")
basicFireball2 = ProjectileNode("Fireball2")
basicChainFB = ProjectileWithOutput("CFB")
expNode = ExplosionNode("Small one")
noDmg = NoDamageNode("NDM")
tenChildren = TenChildren("TC")
tenParents = TenParents("TP")

onHitNode = OnHitNode("OnHitTest")

strongFireNode1 = StrongFireNode("StrFire1")
strongWaterNode = StrongWaterNode("StrWtr1")

crystalNode = CrystalNode("c1")



#aoeSpell = Spell("AOE Spell", [basicCastNode1])
#aoeSpell.simulate_time_period(5)

#BASIC FIREBALL
#basicCastNode1.child_nodes.append(basicFireball)
link_nodes(wand1, basicFireball)
#basicFireball.parent_nodes.append(basicCastNode1)
unmodSpell = Spell("Basic fireball", [wand1])
#unmodSpell.simulate_time_period(5)

#node = get_node_with_free_slot([basicCastNode1, basicFireball], True)
#if node != None:
#    print(node.nodeName)
#else:
#    print("No slot found")

#BASIC CRYSTAL

clean_pool([basicFireball, wand1])
link_nodes(crystalNode, basicFireball)
link_nodes(wand1, crystalNode)

crystalSpell = Spell("Crystal spell", [wand1])
#crystalSpell.simulate_time_period(5)

#DASH CRYSTAL

clean_pool([basicFireball, crystalNode])
link_nodes(crystalNode, basicFireball)
link_nodes(dash1, crystalNode)

crystalSpell2 = Spell("Crystal spell Dash", [dash1])
#crystalSpell2.simulate_time_period(5)


#Cast into explosion:
clean_pool([wand1, basicFireball])

#Lightning into explosion
#
link_nodes(light1, exp1)
#link_nodes(light1, basicFireball)
lightexplode = Spell("Light Explode", [light1])
#lightexplode.simulate_time_period(5)

#Lightning into AOE
clean_pool([light1, wand1])
link_nodes(wand1,aoeNode1)
lightaoe = Spell("LAOE", [wand1])
lightaoe.simulate_time_period(5)

#TESTING CSV GENERATION

#current_directory = os.path.dirname(os.path.abspath(__file__))
# Define the file path for the CSV
#csv_file_path = os.path.join(current_directory, "output", "example.csv")

#os.makedirs(os.path.dirname(csv_file_path), exist_ok=True)


#gen_csv_from_spellsdata([genSpellProperties(genSpell, 5), genSpellProperties(bestSpell, 5)], csv_file_path)


#TESTING FULL RUN POTENTIAL
#current_directory = os.path.dirname(os.path.abspath(__file__))
# Define the file path for the CSV
#csv_file_path = os.path.join(current_directory, "output", "test_run.csv")

#os.makedirs(os.path.dirname(csv_file_path), exist_ok=True)

#full_spell_generation_run(csv_file_path, 100, enum_SpellQualityHeuristic.DPS, 10, 14)



#TESTING ELEMENTAL TUNING

#testPulse = pt.EnergyPacket(3)
#testPulse.printDetails()
#testPulse.changePower(1.5)
#testPulse.printDetails()
#testPulse.changeTendency(.4, EnergyPacket.FIRE )
#testPulse.printDetails()
