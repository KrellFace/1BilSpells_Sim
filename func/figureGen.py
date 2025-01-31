import numpy as np
import matplotlib.pyplot as plt

def gen_heatmap(x_vals, y_vals, bucket_count, x_label, y_label, title, out_path):
    # Define bin edges
    x_bins = np.linspace(0, max(x_vals), bucket_count)  
    y_bins = np.linspace(0, max(y_vals), bucket_count) 

    # Compute 2D histogram
    heatmap, xedges, yedges = np.histogram2d(x_vals, y_vals, bins=[x_bins, y_bins])

    # Plot heatmap
    plt.imshow(heatmap.T, origin='lower', aspect='auto',
            extent=[x_bins[0], x_bins[-1], y_bins[0], y_bins[-1]],
            cmap='hot')

    plt.colorbar(label='Count')
    plt.xlabel(x_label)
    plt.ylabel(y_label)
    plt.title(title)
    plt.savefig(out_path+".png")
    #plt.show()


def gen_all_figures(spell_properties, max_nodes_per_spell: int, sim_length: int, outpath):
    
    #Generate linearity vs 1dps image
    x_vals = []
    y_vals = []
    for sp in spell_properties:
        if (sp.uniqueNodeCount == max_nodes_per_spell):
            x_vals.append(sp.linearity)
            y_vals.append(sp.oneTDps/sim_length)          
    gen_heatmap(x_vals, y_vals, 20, "Linearity", "1DPS", "Spell Linearity vs DPS", outpath+"linvsdps")
