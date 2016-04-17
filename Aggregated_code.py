import os
import csv
from Bio import Entrez
from tabulate import tabulate

os.chdir('C:\\Users\\Annelise\\myRepos\\The-BEST-GWAS')

##dbSNP ENTRY CLASS-------------------------------------------------------------

class dbSNP_Entry():

##super ugly but entrez updated retrieval methods and records are no longer
##consistently formated so we are grabbing data by the "tag" in the records
    def set_self(self,records):
        for r in records:
            if r == records[0]:
                self.identifier = r.split(' ')[0]
                self. organsm = r.split(' ')[1]
            if r.count('=') != 0:
                data = r.split('=')
                if len(data) > 1:
                    if data[0] == 'GLOBAL_MAF':
                        self.MAF = data[2]
                    if data[0] == 'GENE':
                        self.gene = data[1]
                    if data[0] == 'GENE_ID':
                        self.geneID = data[1]
                    if data[0] == 'ACC':
                        self.ACC = data[1]
                    if data[0] == 'CHR':
                        self.CHR = data[1]
                    if data[0] == 'FXN_CLASS':
                        self.FXN = data[1]
                    if data[0] == 'ALLELE':
                        self.allele = data[1]
                    if data[0] == 'CHROMOSME BASE POSITION':
                        self.CHR_B_POS = data[1]
                    if data[0] == 'CONTIGPOS':
                        self.contig_POS = data[1]

                        
##init method creates all variables needed and sets them to empty strings
    def __init__(self,records):
        self.identifier = ''
        self.organism = ''
        self.MAF = ''
        self.gene = ''
        self.geneID = ''
        self.ACC = ''
        self.CHR = ''
        self.FXN = ''
        self.allele = ''
        self.CHR_B_POS = ''
        self.contig_POS = ''

        self.set_self(records)

##TODO: Make to_string method for real
    def to_string(self):
        data = '\t'.join(self.__dict__.values())
        return data


##GWAS ENTRY CLASS--------------------------------------------------------------

class GWAS_Entry:

    def __init__(self,data):   
##      want indeces: {7,8},{13-16},{21,24-30}
        self.trait = data[7]
        self.initial_sample_description = data[8]
        self.genes = data[13]
        self.mapped_genes = data[14]
        self.UgeneID = data[15]
        self.DgeneID = data[16] 
        self.identifier = data[21]
        self.context = data[24]
        self.intergenic = data[25]
        self.risk_allele_freq = data[26]
        self.p_value = data[27]
        self.p_value_mlog = data[28]
        self.p_value_text = data[29]
        self.OR_or_BETA = data[30]
        
    def to_string(self):
        data = '\t'.join(self.__dict__.values())

        return str(data)

def dbSNP_gen(infile,email):
    ifstream = open(infile, 'r')
    filecontent = ifstream.read()
    filecontent = filecontent.strip().split('\n')
    ifstream.close()

    dbSNP = {}
    
    Entrez.email = email
    for rsID in filecontent:
        records = []
        handle = Entrez.efetch(db="snp",id=rsID,rettype= "DocSet",retmode="text")
        records = handle.read()
        records = records.strip().split('\n')
        dbSNP[str(rsID)] = dbSNP_Entry(records)

    return dbSNP,filecontent

def GWAS_gen(db_file,infile):
    GWAS = {}

    ifstream = open(infile, 'r')
    filecontent = ifstream.read()
    filecontent = filecontent.strip().split('\n')
    ifstream.close()

    with open(db_file, 'r') as tsvin:
        tsvin = list(csv.reader(tsvin, delimiter = '\t'))
        for row in tsvin:
            if row != tsvin[0] and len(row) != 0:
                if len(row[21]) != 0:
                    if row[21] not in GWAS:
                        GWAS[row[21]] = []
                        GWAS[row[21]].append(GWAS_Entry(row))
                    else:
                        GWAS[row[21]].append(GWAS_Entry(row))
            elif row == tsvin[0]:
                GWAS['HEADER'] = GWAS_Entry(row)
    return GWAS

    
def SNP_output(outfile,GWAS,dbSNP,infile):
    ifstream = open(infile, 'r')
    filecontent = ifstream.read()
    filecontent = filecontent.strip().split('\n')
    ifstream.close()
    
    ofstream = open(outfile, 'w')

    gHeader = '\t'.join(GWAS['HEADER'].__dict__.values())
    sHeader = list(dbSNP.values()[0].__dict__.keys())
    sHeader = '\t'.join(sHeader)

    ofstream.write('rsID' + '\t' + str(gHeader) + '\t' + str(sHeader) + '\n')

    for rsID in filecontent:
        if str(rsID) in GWAS:
            for item in GWAS[rsID]:
                ofstream.write(rsID + '\t' + item.to_string() + '\t')
                if rsID in dbSNP:
                    ofstream.write(dbSNP[rsID].to_string())
                ofstream.write('\n')
    ofstream.close()


##MAIN________________________________________________________________________________________
##infile = raw_input('Input File Name: ')
##outfile = raw_input('Output File Name: ')
##email = raw_input('Email:(needed for Entrez access ')
##GWAS_db_file= raw_input('Please enter file name for downloaded GWAS catalogue: ')
                
infile = 'sample_snp.txt' #or use test_snplist.txt--only has 1 result
genefile = 'test_genelist.txt'
outfile = 'agg_snp_test.txt'
email = 'atsueda@luc.edu'
GWAS_db_file = 'gwas_catalog_v1.0-downloaded_2016-03-10.tsv'

dbSNP = dbSNP_gen(infile,email)[0]
queries = dbSNP_gen(infile,email)[1]
GWAS = GWAS_gen(GWAS_db_file,infile)
SNP_output(outfile,GWAS,dbSNP,infile)







