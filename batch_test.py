import os
from Bio import Entrez

os.chdir('C:\\Users\\Annelise\\myRepos\\The-BEST-GWAS')

identifier = 'rs62283057'

SNP = {}
    
Entrez.email = 'atsueda@luc.edu'
handle = Entrez.efetch(db="snp",id=identifier,rettype= "DocSet",retmode="text")
records = handle.read()
records = records.strip().split('\n')

for r in records:
    r.strip()
    if r.count('=') !=0:
        key = r.split('=')[0]
        value = r.split('=')[1]
        SNP[key] = value
    else:
        SNP['rsID'] = r.split('  ')[0]
        SNP['organism'] = r.split('  ')[1]
        

for key in SNP:
    print str(key) + ': ' + str(SNP[key])
