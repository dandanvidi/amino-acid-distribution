import numpy as np
import matplotlib.pyplot as plt
import csv
import src.download_aa_sequences as ds
from matplotlib.backends.backend_pdf import PdfPages

AA_LETTERS = sorted("ACEDGFIHKMLNQPSRTWVY")

UPID_to_aa_dist = ds.load_UPID_to_aa_dist('aa_dist_by_UP_ID.csv')
aa_dist_per_genome = ds.calculate_aa_dist_per_genome(UPID_to_aa_dist)
aa_dist_per_proteome = ds.calculate_aa_dist_per_proteome('Ecoli_19_Conditions_Proteomics.csv', UPID_to_aa_dist)    
aa_dist_per_genome_normed = ds.normalize_aa_dist(aa_dist_per_genome, 1)
aa_dist_per_proteome_normed = ds.normalize_aa_dist(aa_dist_per_proteome, 19)

pp = PdfPages('genome vs proteome aa_dist.pdf')
N = len(AA_LETTERS)
ind = np.arange(N)  # the x locations for the groups
width = 0.35        # the width of the bars

proteomics_csv_reader = csv.reader(open('Ecoli_19_Conditions_Proteomics.csv', 'r'), delimiter='\t')
proteomics_csv_reader.next()
conditions = proteomics_csv_reader.next()[10:29]

for i, condition in enumerate(conditions):
    print i+1, "generating aa_dist barplot for:  ", condition
    plt.figure()
    ax = plt.axes()
    rects1 = ax.bar(ind, aa_dist_per_genome_normed.T, width, color='r')
    rects2 = ax.bar(ind+width,aa_dist_per_proteome_normed[i, :].T , width, color='y')
    # add some
    ax.set_ylabel('Relative abundance')
    ax.set_title(condition)
    ax.set_xticks(ind+width)
    ax.set_xticklabels((AA_LETTERS))
    ax.legend( (rects1[0], rects2[0]),('Genome','Proteome'))
    pp.savefig()
    plt.close()
pp.close()
   
    
