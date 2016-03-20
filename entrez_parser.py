#main script for pulling info from entrez for a single id
#assumes constant formatting
#gets correct information
import os
from Bio import Entrez

os.chdir('C:\\Users\\Annelise\\myRepos\\The-BEST-GWAS')

Entrez.email = 'atsueda@luc.edu'
handle = Entrez.efetch(db="snp",id="rs62283056",rettype= "DocSet",retmode="text")
records = handle.read()

records = records.strip().split()

rsID = str(records[0])
Organism = records[1] + ' ' + records[2]
SNP_ID = ''
GENE = ''
GENE_ID = ''
ACC = []
CHR = ''
FXN = ''
CHROMOSOME_BASE_POSITION = ''
CONTIGPOS = ''

for r in records:
    if r.startswith('SNP_ID'):
        SNP_ID = r.split('=')[1]
    if r.startswith('GENE') and r.count('ID')==0:
        GENE = r.split('=')[1]
    if r.startswith('GENE_ID'):
        GENE_ID = r.split('=')[1]
    if r.startswith('ACC'):
        ACC = r.strip().split()
    if r.startswith('CHR') and (r.count('=') == 1):
        CHR = r.split('=')[1]
    if r.startswith('FXN'):
        FXN = r.split('=')[1]
    if r.startswith('POSITION'):
        CHROMOSOME_BASE_POSITION = r.split('=')[1]
    if r.startswith('CONTIGPOS'):
        CONTIGPOS = r.split('=')[1]

print rsID;
print Organism;
print SNP_ID;
print GENE;
print GENE_ID;
print ACC;
print CHR;
print FXN;
print CHROMOSOME_BASE_POSITION;
print CONTIGPOS;
    

