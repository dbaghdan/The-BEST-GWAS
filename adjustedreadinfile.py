
import os
import sys

def readin( ):
    file = open (sys.argv[1], 'r')
    gene=[]
    for line in file:
        line=line.strip()
        gene.append(line)

    file1=open(sys.argv[2], 'r')
    snp=[]
    for line in file1:
        line=line.strip()
        snp.append(line)
    for g in gene:
        print(g)
    for s in snp:
        print(s)

