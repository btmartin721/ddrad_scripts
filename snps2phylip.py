#!/usr/bin/env python

import re
import argparse
import sys

def Get_Arguments():

    parser = argparse.ArgumentParser(description="Converts pyRAD .snps file to phylip format")
    
    parser.add_argument("-f", "--file", type=str, required=True, help="Input filename (.snps)")
    parser.add_argument("-o", "--outfile", type=str, required=False, 
                        help="Output filename; Default = out.phy", nargs="?", default="out.phy")
                           
    args = parser.parse_args()
    
    return args
    
def read_snpsfile(infile):

    check_if_exists(infile)
            
    with open(infile, "r") as fin:
        fin.readline()
        samples = dict(line.rstrip().split(None, 1) for line in fin if not line.isspace())
        
    return samples
        
def check_if_exists(filename):

    try:
        file = open(filename, "r")
    except IOError:
        print("\nError: The file " + filename + " does not exist.\n")
        sys.exit(1)

def write_to_file(dictionary, file, val_length):
         
    with open(file, "w") as fout:
        fout.write(str(len(dictionary.keys())) + " " + str(val_length) + "\n")
        for key, val in dictionary.iteritems():
            fout.write(key + "\t" + val + "\n")
            
        fout.write("\n")

################################################################################################################################
#####################################################MAIN#######################################################################
################################################################################################################################


args = Get_Arguments()

data = read_snpsfile(args.file)

for id, seq in data.iteritems():
    data[id] = "".join(seq.split(" _ "))

seq_length = len(data[id])
    
write_to_file(data, args.outfile, seq_length)







