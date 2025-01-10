from func import *
from nodeTypes import *
    
# TESTING


basicCastNode1 = BasicCastNode("Cast Node V1")
basicCastNode2 = BasicCastNode("Cast Node V2")
basicCastNode3 = BasicCastNode("Cast Node V3")
aoeNode1 = AOENode("AOE Node 1")
mod50Node = Mod50Node("Mod 50 node")
basicFireball = FireballNode("Fireball1")
basicFireball2 = FireballNode("Fireball2")
basicChainFB = ChainingFireballNode("CFB")
expNode = ExplosionNode("Small one")
bigExpNode = BigExplosionNode("BigOne")
noDmg = NoDamageNode("NDM")
tenChildren = TenChildren("TC")
tenParents = TenParents("TP")

onHitNode = OnHitNode("OnHitTest")

strongFireNode1 = StrongFireNode("StrFire1")
strongWaterNode = StrongWaterNode("StrWtr1")



#aoeSpell = Spell("AOE Spell", [basicCastNode1])
#aoeSpell.simulate_time_period(5)

#BASIC FIREBALL
basicCastNode1.child_nodes.append(basicFireball)
basicFireball.parent_nodes.append(basicCastNode1)
unmodSpell = Spell("Basic fireball", [basicCastNode1])
unmodSpell.simulate_time_period(5, 1)

node = get_node_with_free_slot([basicCastNode1, basicFireball], True)
if node != None:
    print(node.nodeName)
else:
    print("No slot found")

#BASIC FIREBALL WITH DO NOTHING MOD
#tenChildren.child_nodes = [basicFireball]
#basicCastNode2.child_nodes = [tenChildren]
#modNowtSpell = Spell("Basic fireball Blank Mod", [basicCastNode2])
#modNowtSpell.simulate_time_period(5, 1)

#BASIC FIREBALL SPLIT
tenChildren.child_nodes.append([basicFireball, noDmg])
basicFireball.parent_nodes.append(tenChildren)
noDmg.parent_nodes.append(tenChildren)
basicCastNode2.child_nodes.append(tenChildren)
tenChildren.parent_nodes.append(basicCastNode2)
#splitNowt = Spell("Basic fireball split", [basicCastNode2])
#splitNowt.simulate_time_period(5, 1)

#print(splitNowt.get_spell_xml())

node = get_node_with_free_slot([basicFireball, noDmg, tenChildren,basicCastNode2 ], False)
if node != None:
    print(node.nodeName)
else:
    print("No slot found")


#BASIC AOE
#basicChainFB.child_nodes=[aoeNode1]
#basicCastNode1.child_nodes=[basicChainFB]
#aoeSpell = Spell("Basic AOE", [basicCastNode1])
#unmodSpell.simulate_time_period(5, 1)

#AOE WITH STRONG WATER

#strongWaterNode.child_nodes = [aoeNode1]
#basicChainFB.child_nodes=[strongWaterNode]
#basicCastNode1.child_nodes=[basicChainFB]
#aoeSpell = Spell("Basic AOE", [basicCastNode1])
#unmodSpell.simulate_time_period(5, 1)

#print(unmodSpell.get_spell_xml())

#COMBO SPELL

#comboSpell = Spell("Combo", [basicCastNode1, basicCastNode2])
#print(comboSpell.get_spell_xml())

#POWERFUL EXPLOSION
#mod50Node.child_nodes=[bigExpNode]
#basicCastNode2.child_nodes=[mod50Node]
#modSpell = Spell("Explosion",[basicCastNode2])
#modSpell.simulate_time_period(5, 1)

#FIREBALL THAT TRIGGERS OTHER FIREBALLS ON HIT
#onHitNode.child_nodes=[basicFireball2]
#onHitSpell = Spell("On hit only", [basicCastNode1,onHitNode])
#onHitSpell.simulate_time_period(5, 1)


#BASIC FIREBALL WITH STRONG FIRE NODE
#strongFireNode1.child_nodes=[basicFireball]
#basicCastNode2.child_nodes=[strongFireNode1]
#unmodSpell = Spell("Basic fireball", [basicCastNode2])
#unmodSpell.simulate_time_period(5, 1)

#BASIC FIREBALL WITH STRONG WATER NODE
#strongWaterNode.child_nodes=[basicFireball]
#basicCastNode2.child_nodes=[strongWaterNode]
#unmodSpell = Spell("Basic fireball", [basicCastNode2])
#unmodSpell.simulate_time_period(5, 1)


#BASIC FIREBALL WITH 2 CAST INPUTS
#tenParents.child_nodes = [basicFireball]
#basicCastNode1.child_nodes=[tenParents]
#basicCastNode2.child_nodes=[tenParents]
#twocastball = Spell("Basic fireball", [basicCastNode1, basicCastNode2])
#twocastball.simulate_time_period(5, 1)

#BASIC FIREBALL WITH 3 CAST INPUTS
#tenParents.child_nodes = [basicFireball]
#basicCastNode1.child_nodes=[tenParents]
#basicCastNode2.child_nodes=[tenParents]
#basicCastNode3.child_nodes=[tenParents]
#threccastball = Spell("Basic fireball", [basicCastNode1, basicCastNode2, basicCastNode3])
#threccastball.simulate_time_period(5, 1)
#print(threccastball.get_spell_parentheses_not())


#TESTING SPELL GENERATION

pool = generate_node_pool()

selected_pool = select_x_nodes_from_pool(pool, 12)
for node in selected_pool:
    #print(node.nodeName)
    None

genSpell = generate_random_spell(copy_node_list(selected_pool), "Generated Spell")[0]
print(genSpell.get_spell_parentheses_not())
genSpell.simulate_time_period(5, 1)


print(f"Len of pool: { len(selected_pool)}")

bestSpell = gen_best_spell(copy_node_list(selected_pool), "Test Spell", 20, enum_SpellQualityHeuristic.DPS)
print(bestSpell.get_spell_parentheses_not())
bestSpell.simulate_time_period(5, 1)


#testPulse = pt.EnergyPacket(3)
#testPulse.printDetails()
#testPulse.changePower(1.5)
#testPulse.printDetails()
#testPulse.changeTendency(.4, EnergyPacket.FIRE )
#testPulse.printDetails()
