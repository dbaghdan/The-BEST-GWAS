##NOTES: This script parses the downloaded GWAS Catalogue (.tsv file formatting)
##Only parses part of the data available for now. Will refine at later date.
import os
import csv

os.chdir('C:\\Users\\Annelise\\myRepos\\The-BEST-GWAS')



    
# this function will open the catalogue file and pull information for each snp
# the infomration for each snp is put into a dictionary object
# each dictionary object is put into a list which the function returns--------------------
def catalogue_parser(filename):
    with open(filename, 'rb') as tsvin:
        tsvin = list(csv.reader(tsvin, delimiter = '\t'))

        snpList = []

        for row in tsvin:
            if row != tsvin[0]:
                dicName = {
                    "name": row[21],
                    "trait": row[7],
                    "region": row[10],
                    "Chr_ID": row[11],
                    "Chr_Pos": row[12],
                    "Reported_Gene": row[13],
                    "Mapped_Gene": row[14],
                    "UGene_ID": row[15],
                    "DGene_ID": row[16],
                    "Snp_Gene_ID": row[17],
                    "UGene_Dis": row[18],
                    "DGene_Dis": row[19]
                    }
                snpList.append(dicName)

    return snpList

#retrieves any dictionary items that contain the given rsID-------------------------------
def data_retrieval(rsID,snpList):
    
    snpDic = [d for d in snpList if d['name'] == str(rsID)]

    return snpDic

#retrieves any dictionary items that contain the given gene name-------------------------
def data_gene_ret(gene, snpList):

    geneDic = [d for d in snpList if d['Reported_Gene'].count(gene) != 0]

    return geneDic



#Main-------------------------------------------------------------------------------------

filename = 'gwas_catalog_v1.0-downloaded_2016-03-10.tsv'

snpList = catalogue_parser(filename)

rsID = 'rs73635312'

snpDic = data_retrieval(rsID, snpList)

if len(snpDic) != 0:
    for element in snpDic:
        print element
        print '\n'
else:
    print 'SNP not found'


geneDic = data_gene_ret('RP11-428L9.1',snpList)

if len(geneDic) != 0:
    for element in geneDic:
        print element
        print '\n'
else:
    print 'Gene not found'

    


