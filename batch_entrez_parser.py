#main script for pulling infor from entrez
#assumes constant formatting

#TODO: add functionality to read in snp list file and go through the list
#TODO: create classes and SNP objects if applicable

import os
from Bio import Entrez

os.chdir('C:\\Users\\Annelise\\myRepos\\The-BEST-GWAS')

    
#Will create a SNP dictionary object------------------------------------------------------
def SNP_data(identifier):
    SNP = {}
    
    Entrez.email = 'atsueda@luc.edu'
    handle = Entrez.efetch(db="snp",id=identifier,rettype= "DocSet",retmode="text")
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
            ACC = r.split('=')[1]
            ACC = ACC.strip().split()
        if r.startswith('CHR') and (r.count('=') == 1):
            CHR = r.split('=')[1]
        if r.startswith('FXN'):
            FXN = r.split('=')[1]
        if r.startswith('POSITION'):
            CHROMOSOME_BASE_POSITION = r.split('=')[1]
        if r.startswith('CONTIGPOS'):
            CONTIGPOS = r.split('=')[1]

    SNP['rsID'] = rsID
    SNP['ORGANISM'] = Organism
    SNP['SNP_ID'] = SNP_ID
    SNP['GENE'] = GENE
    SNP['GENE_ID'] = GENE_ID
    SNP['ACC'] = ACC
    SNP['CHR'] = CHR
    SNP['FXN'] = FXN
    SNP['CHROMOSOME_BASE_POSITION'] = CHROMOSOME_BASE_POSITION
    SNP['CONTIGPOS'] = CONTIGPOS

    return SNP

#MAIN-------------------------------------------------------------------------------------
snpList = ['rs62283056','rs62283057','rs17718958','rs10919728','rs6662178']

SNP_COLLECTION = []

for s in snpList:
    SNP = SNP_data(s)
    SNP_COLLECTION.append(SNP)

for c in SNP_COLLECTION:
    for rec in c:
        print  str(rec) + ' = ' + str(c[rec]);
    print '\n'

