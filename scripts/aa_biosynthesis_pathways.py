import matplotlib.pyplot as plt
import numpy as np
import csv
import src.download_aa_sequences as ds
from matplotlib.backends.backend_pdf import PdfPages

AA_LETTERS = sorted("ACEDGFIHKMLNQPSRTWVY")
AA_PATH = sorted(['P_'+ x for x in AA_LETTERS])

aa_biosythesis_reader = csv.reader(open('aa_biosynthesis_pathways_genes.csv'), delimiter='\t')
genes_in_path = {}
for i, row in enumerate(aa_biosythesis_reader):
     bnumbers= filter(None, row[1:])
     UPIDs = ds.convert_bnumbers_to_UPID(bnumbers, 'all_ecoli_genes.txt')
     genes_in_path[AA_LETTERS[i]] = UPIDs

UPID_to_aa_dist = ds.load_UPID_to_aa_dist('aa_dist_by_UP_ID.csv')
aa_dist_in_path = {}
aa_dist_in_path_for_cond_normed = {}

for i, aa in enumerate(AA_LETTERS):
    for UPID in genes_in_path[aa]:
        aa_dist_in_path[UPID] = UPID_to_aa_dist[UPID]
    k = ds.calculate_aa_dist_per_proteome('Ecoli_19_Conditions_Proteomics.csv', 
                                      aa_dist_in_path)    
    k = ds.normalize_aa_dist(k, 19)         
    aa_dist_in_path_for_cond_normed[AA_PATH[i]] = k    

proteomics_csv_reader = csv.reader(open('Ecoli_19_Conditions_Proteomics.csv', 'r'), delimiter='\t')
proteomics_csv_reader.next()
conditions = proteomics_csv_reader.next()[10:29]

aa_dist_in_proteome = ds.calculate_aa_dist_per_proteome('Ecoli_19_Conditions_Proteomics.csv'
                                                        ,UPID_to_aa_dist)
aa_dist_in_proteome_normed = ds.normalize_aa_dist(aa_dist_in_proteome, 19)
pp = PdfPages('heat_maps_for_aa_dist_in_aa_pathways.pdf')
for j, condition in enumerate(conditions):
    print j+1, "generating aa_dist heatmap for:  ", condition
    condi = np.zeros((len(AA_LETTERS), len(AA_LETTERS)))
    for i, P_aa in enumerate(AA_PATH):
        condi[i] = np.log(aa_dist_in_path_for_cond_normed[P_aa][j] / aa_dist_in_proteome_normed[j])
    plt.clf()
    plt.imshow(condi, interpolation="nearest")
    plt.colorbar()
    plt.clim(vmin = -0.6, vmax = 0.6)
    #plt.show()
    N = len(AA_LETTERS)
    ind = np.arange(N)  # the x locations for the groups
    width = 0.1        # the width of the bars
    ax = plt.axes()
    ax.set_ylabel('Log(aa_P(aa) / aa_proteome')
    ax.set_title('aa_dist in aa biosyn path    ' + condition)
    ax.set_xticks(ind+width)
    ax.set_xticklabels((AA_LETTERS))
    ax.set_yticks(ind+width)
    ax.set_yticklabels((AA_PATH))
    pp.savefig()
pp.close()
