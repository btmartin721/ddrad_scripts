#!/usr/bin/env python3

import argparse
import csv
import operator
import sys


def main():

    arguments = Get_Arguments()
    file = arguments.file
    outfile = arguments.out
    stats = arguments.stats
    phylip = arguments.phylip
    start = arguments.start
    end = arguments.end
    to_keep = arguments.keep
    
    if stats and phylip:
        raise Exception("Error: Only one input file type can be specified")
        return 1
    
    if stats:
        try:
            with open(file, "r") as fin:
                total_loci, sample_lst = read_stats(fin)
        except IOError:
            print("\nError: The file " + file + " does not exist.\n")
            return 1
            
        sorted_lst = sort_list_of_tuples(sample_lst, start, end)
        keepers, excluded = get_first_n_samples(sorted_lst, start, end, to_keep)
        
        print(keepers)
        
        keep_count = len(keepers)
        excluded_count = len(excluded)
        
        try:
            keep_ext = (outfile + ".keepers.csv")
            excl_ext = (outfile + ".excluded.csv")
            with open(keep_ext, "w") as fout:
                wr = csv.writer(fout, delimiter=",")
                wr.writerows([keepers])
                print("\n\nSamples to keep written to: " + keep_ext)
                print("Number of samples kept: " + str(keep_count) + "\n")
            with open(excl_ext, "w") as fout:
                wr = csv.writer(fout, delimiter=",")
                wr.writerows([excluded])
                print("Samples to exclude written to: " + excl_ext)
                print("Number of samples excluded: " + str(excluded_count) + "\n\n")

        except IOError:
            print("Error: Could not write output to files; aborting program")
            return 1
        
    return 0
    
def Get_Arguments():

    parser = argparse.ArgumentParser(description="Picks best N samples from pyRAD stats or PHYLIP file",
                                    add_help=False)

    required_args = parser.add_argument_group("Required Arguments")
    choose_one = parser.add_argument_group("Choose one of the following options")
    optional_args = parser.add_argument_group("Optional Arguments")

    required_args.add_argument("-k", "--keep", type=int, required=True,
                        help="Number of samples to keep for each taxon")
    required_args.add_argument("-f", "--file", type=str, required=True,
                        help="Input file name")
    choose_one.add_argument("-p", "--phylip", action="store_true",default=False,
                        help="Boolean; Toggles PHYLIP input format; default=True")
    choose_one.add_argument("-S", "--stats", action="store_true", default=False,
                            help="Boolean; Toggles pyRAD stats file for sample weights; default=False")
    optional_args.add_argument("-h", "--help", action="help",
                        help="Displays this help menu")
 
    optional_args.add_argument("-s", "--start", type=int, required=False, nargs="?", default="1",
                        help="Specify first character of sample ID to be used as pattern for population ID; default=1")
    optional_args.add_argument("-e", "--end", type=int, required=False, nargs="?", default="4",
                        help="Specify last character of sample ID to be used as pattern for population ID; default=4")
    optional_args.add_argument("-o", "--out", type=str, required=False, nargs="?", default="out",
                        help="Specify output file prefix for samples to keep (best samples); default=out")
    args = parser.parse_args()

    return args
    
def read_stats(infile):
    
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
            my_tuple = (columns[0], int(columns[1]))
            my_lst.append(my_tuple)
            

    for line in infile:
        if line.strip().startswith('sampled unlinked SNPs'):
            line = line.rstrip()
            snps = line.split("=")
            numloci = snps[1].strip()
            
    return numloci, my_lst

def sort_list_of_tuples(my_tpl_lst, start, end):

    sorted_tpl = sorted(sorted(my_tpl_lst, key = lambda x: x[1], reverse = True), key = lambda x: x[0][start-1:end])
    return sorted_tpl

def get_first_n_samples(my_lst, start, end, keep_val):

    keep_lst = list()
    exclusions = list()
    counter = 0
    exclude_counter = 0
    previous_ind = None
    previous_pattern = None

    
    for ind in my_lst:
    
        pattern = str(ind[0][start-1:end])
        
        if pattern == previous_pattern:
           
            if counter < keep_val and keep_val != 1:
                counter += 1
                keep_lst.append(ind[0])
            elif counter >= keep_val:
                exclude_counter += 1
                exclusions.append(ind[0])
           # print(pattern + "\t" + str(counter))
        elif previous_pattern == None:
            counter += 1
            keep_lst.append(ind[0])
            #print(pattern + "\t" + str(counter))

        elif pattern != previous_pattern:
            if counter < keep_val and counter == 1:
                keep_lst.append(ind[0])
                print("Warning: Population " + previous_pattern + " only contains " + str(counter) + " individuals (fewer than -k option)")

            elif counter < keep_val and counter > 1:
                print("Warning: Population " + previous_pattern + " only contains " + str(counter) + " individuals (fewer than -k option)")
            
            elif counter == keep_val and counter == 1:
                keep_lst.append(ind[0])
            else:
                keep_lst.append(ind[0])
            #print(pattern + "\t" + str(counter))
            counter = 1
            
        previous_pattern = pattern
        previous_ind = ind[0]
        
    return keep_lst, exclusions

        
if __name__ == "__main__":
    rtrn_code = main()
    print("Program finished with exit status " + str(rtrn_code) + "\n")
    sys.exit(rtrn_code)
