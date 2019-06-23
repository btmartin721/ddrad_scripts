#!/usr/bin/env python3

### This script was written by Bradley T. Martin, PhD candidate,
### University of Arkansas, Dept. of Biological Sciences
### Please submit any issues or bug reports to: btm002@email.uark.edu

import argparse
import sys

import numpy as np
import pandas as pd

from functools import reduce

def main():

    args = Get_Arguments()

    pop = args.popmap
    batch = args.batch
    species = args.species
    subspecies = args.subspecies

    validate_file_exists(pop)
    poplist = read_popmap(pop)
    popdf = pd.DataFrame.from_records(poplist, columns = ["Individual", "popID"])

    batchdf = pd.DataFrame()
    spdf = pd.DataFrame()
    subspdf = pd.DataFrame()

    if batch is not None:
        validate_file_exists(batch)
        batchlist = read_popmap(batch)
        batchdf = pd.DataFrame.from_records(batchlist, columns = ["Individual", "batch"])

    if species is not None:
        validate_file_exists(species)
        splist = read_popmap(species)
        spdf = pd.DataFrame.from_records(splist, columns = ["Individual", "speciesID"])

    if subspecies is not None:
        validate_file_exists(subspecies)
        subsplist = read_popmap(subspecies)
        subspdf = pd.DataFrame.from_records(subsplist, columns = ["Individual", "subspeciesID"])

    tmpdfs = [batchdf, popdf, spdf, subspdf]

    dfs = list()
    for df in tmpdfs:
        if not df.empty:
            dfs.append(df)

    if not dfs:
        print("Error: Was not able to join files. Make sure each individualID is present in all files.")

    df_final = merge_dataframes(dfs)
    df_final.to_csv(args.outfile, sep = " ", header = True, index = False)

    return 0

def merge_dataframes(dfs):

    df_final = reduce(lambda left, right: pd.merge(left, right, on="Individual"), dfs)
    return df_final

def read_popmap(file):
    """
    Function to read a population map file in the format: indID\tpopID
    Input:
        filename (string)
        Returns:
        list of tuples containing (indID, popID) (list)
        """
    list_of_tuples = list()
    with open(file, "r") as fin:
        for line in fin:
            line = line.strip()
            if not line:
                continue
            cols = line.split()
            my_tuple = (cols[0], cols[1])
            list_of_tuples.append(my_tuple)
    return list_of_tuples



def validate_file_exists(filename):
    """
    Function to validate that an input file exists.
    Input:
        filename (string)
    Returns:
        None
    """
    try:
        file = open(filename, "r")
        file.close()
    except IOError:
        print("\nError: The file " + filename + " does not exist or could not be read.\n")
        sys.exit(1)

def Get_Arguments():
    """
    Parse command-line arguments. Imported with argparse.
    Returns: object of command-line arguments.
    """
    parser = argparse.ArgumentParser(description="Adds batch, species, subspecies "
                                    "columns to popmap file for summarizing ExDFOIL output",
                                    add_help=False)

    required_args = parser.add_argument_group("Required Arguments")
    optional_args = parser.add_argument_group("Optional Arguments")

    ## Required Arguments
    required_args.add_argument("-p", "--popmap",
                                type=str,
                                required=True,
                                help="String; Tab-separated popmap file: indID\tpopID")

    ## Optional Arguments
    optional_args.add_argument("-b", "--batch",
                                type=str,
                                required=False,
                                default=None,
                                nargs="?",
                                help="Filename containing batchIDs")
    optional_args.add_argument("-S", "--species",
                                type=str,
                                required=False,
                                default=None,
                                nargs="?",
                                help="Filename containing speciesIDs")
    optional_args.add_argument("-s", "--subspecies",
                                type=str,
                                required=False,
                                default=None,
                                nargs="?",
                                help="Filename containing subspeciesIDs")
    optional_args.add_argument("-o", "--outfile",
                                type=str,
                                required=False,
                                default="mysampleinfo.txt",
                                nargs="?",
                                help="Specify output filename")
    optional_args.add_argument("-h", "--help",
                                action="help",
                                help="Displays this help menu")


    args = parser.parse_args()

    return args


if __name__ == "__main__":

    rtrn_code = main()
    print("\nProgram finished with exit status " + str(rtrn_code) + "\n")
    sys.exit(rtrn_code)
