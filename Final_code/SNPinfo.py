import os
import sys
import argparse
import csv
from Bio import Entrez
from sets import Set
import time

os.chdir('C:\\Users\\Annelise\\myRepos\\The-BEST-GWAS')

##dbSNP ENTRY CLASS-------------------------------------------------------------

class dbSNP_Entry():
## Makes sure any inconsistent formatting does not make the program crash    
    def set_self(self,records):
        for r in records:
            if r == records[0]:
                z = r.split()
                self.identifier = z[0]
                self. organism = ' '.join(z[1:3])
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

    def to_string(self):
        data = '\t'.join(self.__dict__.values())
        return str(data)

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

##Builds a dictionary of SNP data with rsIDs as keys
def dbSNP_gen(rsIDs,email):
    dbSNP = {}
    myTime = 0
    i = 0
    Entrez.email = email
    for r in rsIDs:
        i+=1
        timeA = time.time()
        records = []
        handle = Entrez.efetch(db="snp",id = r,rettype= "DocSet",retmode="text")
        records = handle.read()
        records = records.strip().split('\n')
        dbSNP[str(r)] = dbSNP_Entry(records)
        timeB = time.time()
        myTime += (timeB - timeA)
    print 'Average dbSNP time: '+ str(float(myTime/i));
    return dbSNP

##Builds a dictionary from the GWAS catalogue based on either gene name or rsID.
def GWAS_gen(db_file,infile,filetype):
    GWAS = {}
    rsIDs = []

    ifstream = open(infile, 'r')
    filecontent = ifstream.read()
    filecontent = filecontent.strip().split('\n')
    ifstream.close()

    gk = Set(filecontent)
                            
    ## BUILT using RSIDs as keys
    if filetype == True:
        rsIDs = filecontent
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
    ##BUILT using the genes as keys
    else:
        
        with open(db_file, 'r') as tsvin:
            tsvin = list(csv.reader(tsvin, delimiter = '\t'))
            for row in tsvin:
                if row != tsvin[0] and len(row) != 0:
                    if len(row[21]) != 0:
                        all_genes = row[13] + ',' + row[14]
                        genes = []
                        x = all_genes.split(' ')
                        for i in range(0,len(x)):
                            y = x[i].split(',')
                            genes += y
                        if '-' in genes:
                            genes.remove('-')
                        genes = Set(genes)
                        if len(genes.intersection(gk)) != 0:
                            rsIDs.append(row[21])  
                        if all_genes not in GWAS:
                            GWAS[all_genes] = []
                            GWAS[all_genes].append(GWAS_Entry(row))
                        else:
                            GWAS[all_genes].append(GWAS_Entry(row))
                elif row == tsvin[0]:
                    GWAS['HEADER'] = GWAS_Entry(row)
    rsIDs = Set(rsIDs)
    print 'rsID list lenght = ' + str(len(rsIDs))    
    return GWAS,rsIDs

def Setup(db_file,infile,email,filetype):
    ifstream = open(infile)
    filecontent = ifstream.read()
    filecontent = filecontent.strip().split('\n')

    x = GWAS_gen(db_file,infile,filetype)
    GWAS = x[0]
    rsIDs = x[1]

    dbSNP = dbSNP_gen(rsIDs,email)
    ifstream.close()

    return GWAS,dbSNP,rsIDs,filecontent

def rsID_output(GWAS,dbSNP,queries,outfile):
    ofstream = open(outfile, 'w')

    gHeaders = GWAS.values()[0][0].__dict__.keys()
    gHeaders = '\t'.join(gHeaders)
    dbHeaders = dbSNP.values()[0].__dict__.keys()
    dbHeaders = '\t'.join(dbHeaders)

    ofstream.write('rsID' + '\t' + gHeaders + '\t' + dbHeaders + '\n')

    for rsID in queries:
        if (rsID in GWAS) and (rsID in dbSNP):
            for item in GWAS[rsID]:
                ofstream.write(str(rsID) + '\t' + item.to_string() + '\t' + dbSNP[rsID].to_string())
                ofstream.write('\n')
        elif (rsID not in GWAS) and (rsID in dbSNP):
            for i in range(0,14):
                ofstream.write('NA\t')
            ofstream.write('\t' + dbSNP[rsID].to_string() + '\n')
        elif (rsID not in dbSNP) and (rsID in GWAS):
            for element in GWAS[rsID]:
                ofstream.write(rsID + '\t' + element.to_string())
            for i in range(15,27):
                ofstream.write('\t')
            ofstream.write('\n')
        else:
            print "SNP data not found\n"
    ofstream.close()

def gene_output(GWAS,dbSNP,queries,outfile):
    ofstream = open(outfile, 'w')
    gk = Set(GWAS.keys())

    gHeaders = GWAS.values()[0][0].__dict__.keys()
    gHeaders = '\t'.join(gHeaders)
    dbHeaders = dbSNP.values()[0].__dict__.keys()
    dbHeaders = '\t'.join(dbHeaders)

    ofstream.write(gHeaders + '\t' + dbHeaders + '\n')
    
    for element in GWAS:
        ##getting a list of genes from the gene (string) key
        genes = []
        x = element.split(' ')
        for i in range(0,len(x)):
            y = x[i].split(',')
            genes += y
        if '-' in genes:
            genes.remove('-')
        genes = Set(genes)
        if len(genes.intersection(queries)) != 0:
            for item in GWAS[element]:
                rsID = item.__dict__['identifier']
                ofstream.write(item.to_string())
                if rsID in dbSNP:
                    entry = dbSNP[rsID]
                    ofstream.write('\t' + entry.to_string())
                ofstream.write('\n')    
    ofstream.close()

def header_gen(GWAS,dbSNP):
    gHeader = '\t'.join(GWAS['HEADER'].__dict__.values())
    sHeader = list(dbSNP.values()[0].__dict__.keys())
    sHeader = '\t'.join(sHeader)
    return gHeader,sHeader

def SNP_output(db_file,infile,email,filetype,outfile):
    
    (GWAS,dbSNP,rsIDs,queries) = Setup(db_file,infile,email,filetype)
    (gHeader,sHeader) = header_gen(GWAS,dbSNP) 

    ofstream = open(outfile, 'w')
    ofstream.write('rsID' + '\t' + str(gHeader) + '\t' + str(sHeader) + '\n')
    ofstream.close()   
    
    ## USING SNP LIST
    if filetype == True:
        rsID_output(GWAS,dbSNP,queries,outfile)
        
    ## USING GENE LIST
    elif filetype == False:
        gene_output(GWAS,dbSNP,queries,outfile)

    return len(queries)

def run_main():
##
##    infile = 'Test_SNP_List_lengths\\snp_2500.txt' #or use test_snplist.txt--only has 1 result
##    genefile = 'input_files\\test_genelist.txt'
##    outfile = 'test_SNP_2500.txt'
##    email = 'atsueda@luc.edu'
##    GWAS_db_file = 'input_files\\GWAS_DB_info.tsv'
##
##    myBool = True

    parser = argparse.ArgumentParser()
    parser.add_argument('input_file',help = 'ok')
    parser.add_argument('db_file',help = 'ok')
    parser.add_argument('output_file',help = 'ok')
    parser.add_argument('email',help = 'ok')
    
    parser.add_argument('-rs',action = 'store_true', dest = 'myBool', help = 'ok')
    parser.add_argument('-g',action = 'store_false', dest = 'myBool', help = 'ok')

    

    args = parser.parse_args()

    print args.myBool;
    print args.input_file;
    print args.db_file;
    print args.email;
    print args.output_file;


    time1 = time.time()
    length = SNP_output(args.db_file,args.input_file,args.email,args.myBool,args.output_file)
    
##    length = SNP_output(GWAS_db_file,infile,email,myBool,outfile)
    time2 = time.time()

    print str((time2-time1)) + ': ' + str(length)

##MAIN________________________________________________________________________________________


run_main()











