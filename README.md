SNPinfo
=========

SNPinfo is a data aggregation tool that pools SNP data from the GWAS Catalogue and NCBI's dbSNP

##Instructions

__To run SNPinfo you will need:__  

Software Requirements:  
* Python 2.7  
  * numPy package  
  
  Scripts:  
  * SNPinfo.py  
  
  Downloaded Files:  
  * GWAS Catalogue (GWAS Catalogue can be downloaded from EBI [here](https://www.ebi.ac.uk/gwas/docs/downloads)).
  
  Input Files:  
  * gene list or rsID list (each gene name or rsID should be on a single line. An example gene list can
be found [here]()).  
  * GWAS Catalogue tsv file
  * Output File
  
  Other Input:  
  * email (needed to access dbSNP via the Entrez library).
  
##Using SNPinfo  

To pool SNP data for a given list of rsIDs, include the '­rs' flag when running SNPinfo.py. To pool SNP
data for a given list of gene names, include the '­g' flag when running SNPinfo.py. Other arguments that
need to be specified are:  
  1. input file: list of genes or rsIDs  
  2. GWAS Catalogue file: tsv file of the GWAS Catalogue  
  3. output file: path to desired output file  
  4. email: needed to access dbSNP  
  
###Output File Format  

Columns  

1. *rsID*: rsID of for the SNP  
2. *p_value_mlog*: log of the p­value  
3. *p_value*: reported p­value for the strongest SNP risk allele  
4. *Downstream Gene ID*: Entrez Gene ID for nearest downstream gene  
5. *p_value_text*: information describing the context of the p­value  
6. *trait*: description of the disease/trait under study  
7. *intergenic*: denotes if an SNP is in an intergenic region (0=no;1=yes)  
8. *genes*: gene(s) reported by the author  
9. *OR_or_Beta*: reported odds ration or beta­coefficient associated with strongest SNP risk allele  
10. *mapped genes*: genes mapped to the strongest SNP  
11. *context*: SNP functional class  
12. *initial sample description*: sample size and ancestry description for stage 1 of GWAS  
13. *Upstream Gene ID*: Entrez Gene ID for nearest upstream gene  
14. *identifier*: rsID (from the GWAS Catalogue)  
15. *risk allele frequency*: reported risk allele frequency associated with the strongest SNP in controls  
16. *accession number*: Accession number associated with the SNP from dbSNP  
17. *identifier*: rsID (from dbSNP)  
18. *chromosome base position*: Base position in the chromosome where the SNP is located  
19. *contig position*: Chromosome accession number and base number  
20. *chromosome*: chromosome in which the SNP is located  
21. *function*: function associated withe the SNP  
22. *MAF*: minor allele frequency  
23. *allele*: which allele the SNP is associated with  
24. *gene*: gene the SNP is associated with  
25. *organism*: organism under study  
26. *geneID*: geneID in NCBI Gene database  

###Usage  

Gene List:  
./SNPinfo.py ­g input_file db_file output_file email

rsID List:  
./SNPinfo.py ­rs input_file db_file outPut_file email
