import csv
from func.packetTypes import SpellProperties

def gen_csv_from_spellsdata(data: list[SpellProperties], outpath: str):
    assembledData = [["Spell Name", "Spell Rep", "Unique Node Count", "Linearity", "1dps", "3dps", "5dps", "10dps"]]
    for sp in data:
        assembledData.append([sp.spellName, sp.spellNodeTree, sp.uniqueNodeCount, sp.linearity, sp.oneTDps, sp.threeTDps, sp.fiveTDps, sp.tenTDps])

    out_csv = outpath

    with open(out_csv, mode="w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        for d in assembledData:
            writer.writerow(d)

    