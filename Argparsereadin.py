import os
import sys
import argparse


def readin( ):
    parser = argparse.ArgumentParser()

    parser.add_argument( 'filename',help="ok")
    parser.add_argument( 'filename2', help= "ok")
    args = parser.parse_args()
    with open(args.filename) as file:
        gene=[]
        for line in file:
            line=line.strip()
            gene.append(line)


    with open(args.filename2) as file:
        snp=[]
        for line in file:
            line= line.strip()
            snp.append(line)

        
    for g in gene:
        print(g)
    for s in snp:
        print(s)


readin()
