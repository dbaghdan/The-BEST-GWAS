#main script for pulling infor from entrez
#assumes constant formatting

#TODO: add functionality to read in snp list file and go through the list
#TODO: create classes and SNP objects if applicable

import os
import sys
from Bio import Entrez

os.chdir('C:\\Users\\Annelise\\myRepos\\The-BEST-GWAS')

    
#Will create a SNP dictionary object------------------------------------------------------
def SNP_data(identifier):
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

    return SNP

#MAIN-------------------------------------------------------------------------------------
input_file = sys.argv[1]

##input_file = 'test_snplist.txt'
ifstream = open(input_file, 'r')
filecontent = ifstream.read()
filecontent = filecontent.strip().split('\n')
ifstream.close()


ofstream = open('entrez_output.txt', 'w')

SNP_COLLECTION = []

for s in filecontent:
    SNP = SNP_data(s)
    SNP_COLLECTION.append(SNP)
print 'Writing File'
for c in SNP_COLLECTION:
    for rec in c:
        line = str(rec) + ' = ' + str(c[rec])
        ofstream.write(line + '\n')
    ofstream.write('\n')

ofstream.close()

