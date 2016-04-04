
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


***parseargparse.ArguementParser()

***Arg prse
**** Arg parse names the argumenents and need to specify - file name path
***look into them
If the user the download and 
