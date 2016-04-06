import os
from Bio import Entrez

os.chdir('C:\\Users\\Annelise\\myRepos\\The-BEST-GWAS')

Entrez.email = 'atsueda@luc.edu'

handle = Entrez.efetch(db="gene",id='CTU1',rettype= "gene_table",retmode="text")
records = handle.read()

print len(records)
