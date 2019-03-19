# -*- coding: utf-8 -*-
"""
Created on Fri Feb 15 10:51:15 2019
@Mail: daixuelei2014@163.com
@author:daixuelei
"""

import sys,os,logging,click,gzip

logging.basicConfig(filename='{0}.log'.format(os.path.basename(__file__).replace('.py','')),
                    format='%(asctime)s: %(name)s: %(levelname)s: %(message)s',level=logging.DEBUG,filemode='w')
logging.info(f"The command line is:\n\tpython3 {' '.join(sys.argv)}")

'''
tax_id,superkingdom,phylum,class,order,family,genus,species,
6,Bacteria,Proteobacteria,Alphaproteobacteria,Rhizobiales,Xanthobacteraceae,Azorhizobium,
'''
def Lineages(lineages):
    f = gzip.open(lineages,'rb')
    Dict1 = {}
    for line in f:
        line = line.decode().strip().split(',')
        if line[0] == 'tax_id':
            pass
        else:
            Dict1[line[0]] = line[7]
    return Dict1
#return tax_id  species
'''
>WP_003131952.1 30S ribosomal protein S18 [Lactococcus lactis]
MAQQRRGGFKRRKKVDFIAANKIEVVDYKDTELLKRFISERGKILPRRVTGTSAKNQRKVVN
'''
def NrHead(head):
    Dict2 = {}
    for line in head:
        if not line.startswith('>'):
            pass
        else:
            line0 = line.strip().split()
            name = line0[0][1:]
            line1 = line.strip().split('[')[0]
            info = line1.strip().split()[1:]
            Dict2[name] = '_'.join(info)
    return Dict2
#return    WP_003131952.1 30S_ribosomal_protein_S18
'''
#tax_id GeneID  status  RNA_nucleotide_accession.version        RNA_nucleotide_gi       protein_accession.version       protein_gi      genomic_nucleotide_accession.version    geno
9       1246500 -       -       -       AAD12597.1      3282737 AF041837.1      3282736 -       -       ?       -       -       -       repA1
''' 
def Gene2Accession(gene2accession):
    Dict3 = {}
    for line in gene2accession:
        line = line.strip().split()
        if line[0] == '#tax_id':
            pass
        else:
            protein_accession_version = line[5]
            tax_id = line[0]
            Symbol = line[-1]
            Dict3[protein_accession_version] = [tax_id,Symbol]
    return Dict3

@click.command()
@click.option('-l','--lineages',type=str,help='input the lineages file',required=True)
@click.option('-h','--head',type=click.File('r'),help='input the Nr header file',required=True)
@click.option('-g','--gene2accession',type=click.File('r'),help='input the gene2accession file',required=True)
@click.option('-b','--blastout',type=click.File('r'),help='input the blastout',required=True)
@click.option('-o','--out',type=click.File('w'),help='output the change of blastout',required=True)
def main(lineages,head,gene2accession,blastout,out):
    Dict1 = Lineages(lineages)
    Dict2 =  NrHead(head)
    Dict3 = Gene2Accession(gene2accession)
    out.write(f'qseqID\tsseqID\tgeneID\tGeneDescription\tspecies\tpident\tqlen\tlength\tmismatch\tgapopen\tqstart\tqend\tsstart\tsend\tevalue\tbitscore\tqcovs\n')
    for line in blastout:
        line = line.strip().split()
        if line[1] in Dict3:
            geneID = Dict3[line[1]][1]
            tax_id = Dict3[line[1]][0]
            species = Dict1[tax_id]              
            GeneDescription = Dict2[line[1]]
            out.write('\t'.join(line[:2]) + "\t" + geneID + "\t" + GeneDescription + "\t" + species + "\t" + '\t'.join(line[2:]) + "\n")
        else:
            out.write('\t'.join(line[:2]) + "\t" + "NONE" + "\t" + "NONE" + "\t" + "NONE" + "\t" + '\t'.join(line[2:]) + "\n")
if __name__ == '__main__':
    main()