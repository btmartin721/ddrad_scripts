#!/usr/bin/env python3

import argparse
import csv
import sys

def main():
    
    arguments = get_arguments()        
    
    sample_list = list()
    
    with open(arguments.stats, "r") as fin:
        loci_count, sample_list = get_sample_block(fin)
        
    max_missing = get_loci_proportion(loci_count, sample_list, arguments.proportion)
    
    
    with open(arguments.outfile, "w") as fout:
        write_excluded_loci(max_missing, sample_list, fout, arguments.outfile, arguments.proportion, loci_count)
    
    
def get_arguments():

    parser = argparse.ArgumentParser(description="Writes CSV of samplesIDs from pyRAD stats file for individuals fewer loci than specified proportion")

    parser.add_argument("-s", "--stats", type=str, required=True, help="pyRAD .stats file")
    parser.add_argument("-o", "--outfile", type=str, required=False,
                        help="Output filename; Default = out.csv", nargs="?", default="out.csv")
    parser.add_argument("-p", "--proportion", type=float, required=True, help="Exclude samples with fewer loci than specified proportion; must be float value")
    
    args = parser.parse_args()

    return args
    
    
def get_sample_block(infile):
    
    my_lst = list()
    
    for line in infile:
        line = line.rstrip()     
        if line.strip().startswith('taxon'):
            break
            
    for line in infile:
        line = line.rstrip()
        if line.strip().startswith('##'):
            break
        if line.strip():
            columns = line.split()
            my_tuple = (columns[0], columns[1])
            my_lst.append(my_tuple)
            
            
    for line in infile:
        if line.strip().startswith('sampled unlinked SNPs'):
            line = line.rstrip()
            snps = line.split("=")
            numloci = snps[1].strip()
            
    return numloci, my_lst
     
def get_loci_proportion(number, lst_of_tuples, proportion):
    
    percentage = float(proportion) * float(number)
    percentage = int(percentage)
    
    return percentage
    
def write_excluded_loci(missing, samples, ofile, filename, proportion, num_loci):

    excluded = [ind[0] for ind in samples if int(ind[1]) < int(missing)]
    number_excluded = len(excluded)
    
    percent = int(100 * proportion)
    amount_missing = 100 - percent
        
    print("\n{} excluded individuals containing more than {} percent missing data (less than {} loci) were written to {}\n\n".format(number_excluded, amount_missing, missing, filename))
    ofile.write(",".join(excluded))
        
        
############################################################################################################################################################
    
main()