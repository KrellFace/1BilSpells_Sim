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
clean_pool([light1, wand1,dash1])
link_nodes(dash1,aoeNode1)
lightaoe = Spell("LAOE", [dash1])
#lightaoe.simulate_time_period(5)

cast1 = WandCast("W1")
cast2 = WandCast("W2")
merger1 = Merger("M1")
rep5 = Repeater5("Rep5-1")
proj1 = ProjectileNode("PN1")
rot45 = Rotator45("R45")
fireBig = StrongFireNode("SF1")
link_nodes(fireBig, proj1)
link_nodes(rot45, fireBig)
link_nodes(rep5,rot45)
link_nodes(merger1, rep5)
link_nodes(cast1, merger1)
link_nodes(cast2, merger1)
mSPell = Spell("MSpell", [cast1, cast2])
#mSPell.simulate_time_period(5)

w1 = WandCast("W1")
aoe1 = AreaNode("A1")
aoe2 = AreaNode("A2")
aoe3 = AreaNode("A3")
aoe4 = AreaNode("A4")
split1 = Splitter("S1")
split2 = Splitter("S2")
split3 = Splitter("S3")
link_nodes(split1, aoe1)
link_nodes(split1, aoe2)
link_nodes(w1, split1)
aoesPELL = Spell("aoe test", [w1])
#aoesPELL.simulate_time_period(5)


w1 = WandCast("W1")
proj1 = ProjectileNode("PN1")
onhit1 = OnHit("OH1")
merge1 = Merger("M1")
link_nodes(merge1, proj1)
link_nodes(w1, merge1)
link_nodes(onhit1, merge1)
sp1 = Spell("On hit", [w1, onhit1])
#sp1.simulate_time_period(5)


w1 = WandCast("W1")
proj1 = ProjectileNode("PN1")
splitter2 = Splitter("Splitter")
link_nodes(splitter2, proj1)
link_nodes(w1, splitter2)
sp = Spell("Blah", [w1])
#sp.simulate_time_period(5, True)

dashEnd = OnDashEnd("d1")
rep5 = Repeater5("R5")
onhit1 = OnHit("OH1")
onhitH = OnHitHealthy("OHH")
tripM = TrippleMerger("TM")
crys1 = CrystalNode("C1")
alt1 = Alternator2("A2")
lazor = LaserNode("LN")
aoe1 = AreaNode("an")

link_nodes(alt1, lazor)
link_nodes(alt1, aoe1)
link_nodes(crys1, alt1)
link_nodes(tripM, crys1)
link_nodes(rep5, tripM)
link_nodes(dashEnd, rep5)
link_nodes(onhit1, tripM)
link_nodes(onhitH, tripM)

testSpell = Spell("B",[dashEnd, onhit1, onhitH])
#testSpell.simulate_time_period(5, True)

w1 = WandCast("")
aoe2 = AreaNode("")
link_nodes(w1,aoe2)
c1 = Spell("", [w1])
#c1.simulate_time_period(5, True)

proj = ProjectileNode("")
de = OnDashEnd("")
de2 = OnDashEnd("")
onhit3 = OnHit("")
trip = TrippleMerger("")
ro10 = Rotator10("")
arean = AreaNode("")

link_nodes(ro10, arean)
link_nodes(trip, ro10)
link_nodes(de,trip)
link_nodes(de2, trip)
link_nodes(onhit3, trip)
sp = Spell("", [de,de2,onhit3])
#sp.simulate_time_period(5, True)

wan1 = WandCast("")
dash1 = OnDashEnd("")
aoe = AreaNode("")
bigEarth = StrongEarthNode("")
link_nodes(bigEarth, aoe)
link_nodes(dash1, bigEarth)
sp = Spell("",[dash1])
#sp.simulate_time_period(5, True)


#TESTING CSV GENERATION

#current_directory = os.path.dirname(os.path.abspath(__file__))
# Define the file path for the CSV
#csv_file_path = os.path.join(current_directory, "output", "example.csv")

#os.makedirs(os.path.dirname(csv_file_path), exist_ok=True)


#gen_csv_from_spellsdata([genSpellProperties(genSpell, 5), genSpellProperties(bestSpell, 5)], csv_file_path)


#TESTING FULL RUN POTENTIAL
current_directory = os.path.dirname(os.path.abspath(__file__))
#Define the file path for the CSV
csv_file_path = os.path.join(current_directory, "output", "10000-DPS-Targ.csv")

os.makedirs(os.path.dirname(csv_file_path), exist_ok=True)

full_spell_generation_run(csv_file_path, 10000, enum_SpellQualityHeuristic.DPS, 20, 3)



#TESTING ELEMENTAL TUNING

#testPulse = pt.EnergyPacket(3)
#testPulse.printDetails()
#testPulse.changePower(1.5)
#testPulse.printDetails()
#testPulse.changeTendency(.4, EnergyPacket.FIRE )
#testPulse.printDetails()
