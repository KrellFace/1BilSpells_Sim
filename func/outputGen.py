import csv
from func.packetTypes import SpellProperties
from func.nodeSuperTypes import SpellNode

def gen_csv_from_spellsdata(data: list[SpellProperties], outpath: str, limit_to_x_nodes = False, x_nodes: int = None):
    assembledData = [["Spell Name", "Spell Rep", "Unique Node Count", "Linearity", "1dps", "3dps", "5dps", "10dps"]]
    for sp in data:
        if (limit_to_x_nodes is False or sp.uniqueNodeCount == x_nodes):
            assembledData.append([sp.spellName, sp.spellNodeTree, sp.uniqueNodeCount, sp.linearity, sp.oneTDps, sp.threeTDps, sp.fiveTDps, sp.tenTDps])

    if (limit_to_x_nodes):
        out_csv = outpath +str(x_nodes)+"only_data.csv"
    else:
        out_csv = outpath +"_data.csv"

    with open(out_csv, mode="w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        for d in assembledData:
            writer.writerow(d)

def gen_csv_from_nodelist(nested_nodelist, outpath: str):
    assembledData = [["#","NodeName", "NodeType"]]
    num = 1
    for row in nested_nodelist:
        for n in row:
            assembledData.append([str(num),n.nodeName,n.nodeType])
            num+=1

    out_csv = outpath+"_nodes.csv"

    with open(out_csv, mode="w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        for d in assembledData:
            writer.writerow(d)
    